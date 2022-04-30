"""[simpleCleanV0]
    Scipts de préparation de données à partir d'un export textuel d'une bdd postgresql avec les attributs id, text(string), date(string)
    Note sur la procédure:
        Comme le cleaning utilise un lexique il enlèvera la majorité des mots mal orthographiés ce qui n'est pas forcément idéal, autres pistes:
            - ne pas utiliser de lexique
            - compléter le lexique
            - procéder à un calcul de distance avec les mots du lexique et admettre une marge d'erreur
            - lemmatiser le lexique et comparer seulement avec des tokens eux mêmes lématisés
            - Appliquer une correction automatisée (lib blob)
        Autres:
            Les noms propres ne pouvant pas faire l'objet d'une comparaison lexicale:
            - ne pas les conserver
            - Etablire une Liste de noms propres les plus courants (Marque, Nom de famille, prénom)
            Procéder à l'étiquetage:
            - POS
            - Shallow parsing

    Info lexique:
        Auteur: Christophe Pallier
        Nom: liste.de.mots.francais.frgut.txt
        Url:  http://www.pallier.org/liste-de-mots-francais.html
        Contenu:  liste à partir du dictionnaire Francais-Gutenberg de Christophe Pythoud.
"""
import spacy
import re
import os

from pathlib import Path
from tqdm import tqdm
from nltk.corpus import stopwords

def load_data(f, d=0):
        """
        Load data file and with option d tweet like id \t text \t date
        :param f: name of the file
        :return: array of array
        """
        with open(f, 'r', encoding="utf-8") as f:
                dt = f.read().splitlines()
        if d:
            for idx, e in enumerate(dt):
                dt[idx] = e.split('\t')
        return dt

def rligature(w):
    """
    normalise les ligatures en lettres distinctes, à utiliser en fonction des lexiques et bibliothèques de mots utilisés
    :param w: une chaîne de caractères
    :return: une chaîne de caractères sans œ et/ou æ
    """
    if "œ" in w:
        w = w.replace("œ","oe")
    if "æ" in w:
        w = w.replace("æ", "ae")
    return w

def countline(f):
    """
    return le nombre de lignes dans un document
    :param f: file
    :return: int
    """
    with open(f, 'r', encoding="utf-8") as f:
        dt = f.read().splitlines()
    return len(dt)

def decoupe_phrases(s, nlp):
    """
    Découpe un text en liste de phrases
    :param s: texte
    :return: liste de chaînes de caractères
    """
    temp = nlp(s)
    return [X.text for X in temp.sents]

def decoupe_mots(s, nlp):
    """
    Découpe une phrase en mots
    :param s:  texte
    :return:  liste de chaînes de caractères
    """
    temp = nlp(s)
    return [X.text for X in temp]

def nom_propre(s):
    """
    Vérifie si un mot commence par une majuscule et ne contient que des minuscules pour les autres caractères.
    :param s: un mots
    :return: booléen
    """
    return bool(re.match("[A-Z]{1}[^A-Z]{" + str(len(s) - 1) + "}", s))

def main(data ="OneMillionsTweetsFR.sql", lex="liste.de.mots.francais.frgut.txt"):
    """
    Fonction principale du nettoyage
    :param data: Jeu de données initiales
    :param lex: Lexique de contrôle
    :return: fichier.txt
    """
    lexique_fr = load_data(lex)
    """
    Le tokeniseur d'après la lib chargée 
    (execute in environement "python -m spacy download fr_core_news_sm")
    """
    nlp = spacy.load("fr_core_news_sm")
    dataset = load_data(data, 1)
    stopWords = set(stopwords.words('french'))
    nbl = countline("OneMillionsTweetsFR.sql")
    new_id = 0
    outf = f"{data[:-4]}_simpleCleanV0.txt"
    outtp = f"{outf[:-4]}_tmp.txt"
    p = Path.cwd()
    mode = 'w'
    offset = 0

    # On vérifie si le travail avec ses paramètres ont déjà été commencé
    if ((p.joinpath(p, outf).exists()) and (p.joinpath(p, outtp).exists())):
        mode = 'a'
        with open(outtp, "r") as f:
            r = f.read().split("\t")
            offset = int(r[0])
            new_id = int(r[1])

    rec = open(outf, mode)

    #main loop
    for i in tqdm(range(offset, nbl)):
        with open(outtp,"w") as f:
            f.write(f"{i}\t{new_id}")
        line = dataset[i]

        #I sélection des lignes de données grâce l'ID
        if line[0].isalnum():
            #1 Attribution ID de traitement
            line[0] = new_id
            line.remove('\\N')
            #2 Diviser le texte en phrases:
            line[1] = decoupe_phrases(line[1], nlp)
            #3 Diviser les phrases en liste de mots:
            for idx, e in enumerate(line[1]):
                line[1][idx] = decoupe_mots(e, nlp)

            #II traitement avec re-vérification à chaque modification (verifying)
            err = 1
            while err != 0:
                err = 0
                for idx, p in enumerate(line[1]):
                    for idx2, w in enumerate(p):

                        #1 retrait d'url (majoritairement inutile en cas de traitement alphanumérique + lexique)
                        if w.startswith("http"):
                            err += 1
                            line[1][idx].remove(w)
                            continue

                        #2 retrait caractères spéciaux (travail sur minuscule si les noms propres sont à évacuer)
                        temp = re.sub('[^a-zA-Z0-9àâäéèëêïîôöùûüÿç]+', '', w)
                        if (temp != w):
                            line[1][idx][idx2] = temp
                            err+=1
                            continue

                        #3 retrait des chaînes vides
                        if w == '':
                            err+=1
                            line[1][idx].remove(w)
                            continue

                        #4 vérifications lexicales
                        if w.lower() not in lexique_fr:
                            if not nom_propre(w):
                                err += 1
                                line[1][idx].remove(str(w))
                                continue
                        elif w.lower() != w:
                            line[1][idx][idx2] = w.lower()
                            err += 1
                            continue

                        #5 filtrage des stopwords
                        if w in stopWords:
                            err += 1
                            line[1][idx].remove(w)
                            continue

                        #6 Monocaractère en majuscule
                        if len(w) == 1:
                            err += 1
                            line[1][idx].remove(w)
                            continue

                        #7 Lemmatisation des résultats
                        if err == 0:
                            lemma = [X.lemma_ for X in nlp(w)]
                            line[1][idx][idx2] = lemma[0]

                    #8 retrait phrases trop courtes
                    if len(p) < 3:
                        err += 1
                        line[1].remove(p)
                        continue
            #III finalisation
            if len(line[1]) != 0:
                # écriture des résultats
                rec.write(f"{line[0]}\t {line[1]}\t {line[2]}\n")
                new_id += 1

    rec.close()
    os.remove(outtp)

if __name__ == "__main__":
    #ajouter la possibilité de controller depuis la ldc main(source, lexique, new)
    main()