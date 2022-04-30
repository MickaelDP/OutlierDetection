"""
    Lib pour le nettoyage de jeux de données
"""

import spacy
import re
from nltk.stem.snowball import SnowballStemmer

# chargement du modèle grammaticale
nlp = spacy.load("fr_core_news_sm") 
lexique = loadlex("LexHaine.txt")
stop = loadstop("stopW.txt")
stemmer = SnowballStemmer(language='french')

def DataClean(data, lexique, nlp):
    """ Corrige et normalise un dataset
    Args:
        data (fichier): fichier (1 tweet par ligne)
        correction (fichier): lexique de correction des expressions haineuses
    """
    outmin = str(data.split(".")[0]) + "Min.txt"
    min = open(outmin, 'a')
    with open(data, 'r') as data:
        for line in data:
            lineClean = ""
            words = decoupeMots(line, nlp)
            for word in words:
                word = rplace(rexochar(rhttp(rligature(word))).lower(), lexique)
                if len(lineClean) == 0 or word in ".,!?:;.":
                    lineClean = lineClean + str(word)
                elif lineClean[-1] in "'-’#":
                    lineClean = lineClean + str(word)
                elif word[0] in "-":
                    lineClean = lineClean + str(word)
                else:
                    lineClean = lineClean + " " + str(word)
            min.write(lineClean + "\n")
    min.close()

def DataStd(data, nlp, stop):
    """Filtre a l'aide d'une liste de stop words et stemmatise les restes.

    Args:
        data (fichier): données (1 tweet par ligne)
        nlp (organisation grammaticale): objet spacy en fonction de la langue
        stop (liste): liste de stop words
    """
    outstd = outmin = str(data.split(".")[0][:-3]) + "Std.txt"
    std = open(outstd, 'a')
    with open(data, 'r') as data:
        for line in data:
            lineStd = ""
            words = decoupeMots(line, nlp)
            for word in words:
                if word in stop:
                    pass
                elif len(lineStd)==0 or word in ".,!?:;." or  word[0] in "-" or lineStd[-1] in "'-’#":
                    lineStd = lineStd + word
                else:
                    lineStd = lineStd + " " + word
            result = [stemmer.stem(X.text) for X in nlp(lineStd)]
            std.write(str(result)+"\n")
    std.close()

def noemptyframe(original, min, std):
    """prend les fichiers créés par les fonctions précédentes afin de retirer dans chacun d'eux les lignes vides de la version nettoyée "*min" afin de conserver une correspondance ligne à ligne

    Args:
        original (fichier): fichier de données brut original
        min (fichier): fichier avec les mêmes données nettoyées
        std (fichier): fichier avec les mêmes données mais "standardisées"
    """
    Or = loadline(original) 
    Std = loadline(std)
    indexMin = 0
    outOr = open(str(original.split('.')[0]) + "_NEF.txt", 'a')
    outStd = open(str(std.split('.')[0]) + "_NEF.txt", 'a')    
    outMin = open(str(min.split('.')[0]) + "_NEF.txt", 'a')
    with open(min, 'r') as data:
        for line in data:
            if line != "\n":
                outOr.write(Or[indexMin])
                outStd.write(Std[indexMin])
                outMin.write(line)
            indexMin += 1
    outOr.close()
    outStd.close()
    outMin.close()

def loadlex(lex):
    """Charge un lexique: liste de listes

    Args:
        lex (fichier): fichier de listes de mots séparé par des ','

    Returns:
        liste: liste de listes de mots
    """
    with open(lex, 'r') as data:
        lexique = []
        for line in data:
            lineR = []
            temp = line.split(", ")
            for e in temp:
                lineR.append(e.split("\n")[0])
            lexique.append(lineR)
        return lexique

def loadstop(stop):
    """charge une liste de mots

    Args:
        stop (fichier): fichier comprenant un mot par ligne

    Returns:
        liste: liste de mots
    """
    with open(stop, 'r') as data:
        stop = []
        for line in data:
            stop.append(line.split('\n')[0])
        return stop

def loadline(file):
    """chargement de ligne

    Args:
        file (fichier): fichier de données

    Returns:
        liste: liste des lignes
    """
    with open(file, 'r') as data:
        temp = []
        for line in data:
            temp.append(line)
        return temp

def decoupeMots(s, nlp):
    """Découpe une ligne en mots
    Args:
        s (string): ligne
        nlp (nlp): objet nlp de lib spacy
    """
    temp = nlp(s)
    return [X.text for X in temp]

def rligature(w):
    """
    normalise les ligatures en lettres distinctes, à utiliser en fonction des lexiques et bibliothèques de mots utilisés
    :param w: une chaîne de caractères
    :return: une chaîne de caractères sans œ et/ou æ
    """
    if "œ" in w:
        w = w.replace("œ","oe")
    if "Œ" in w:
        w = w.replace("Œ","oe")
    if "æ" in w:
        w = w.replace("æ", "ae")
    if "Æ" in w:
        w = w.replace("Æ", "ae")
    return w

def rhttp(w):
    """
    normalise les urls
    :param w: une chaîne de caractères
    :return: une chaîne de caractères sans url
    """
    if w.startswith("http"):
        w = ''
    return w

def rexochar(w):
    """
    normalise en retirant tous les caractères exotiques du point de vue de la langue française
    :param w: une chaîne de caractères
    :return: une chaîne de caractères sans caractères spéciaux
    """
    temp = re.sub('[^a-zA-Z0-9àÀâÂäÄéÉèÈëËêÊïÏîÎôÔöÖùÙûÛüÜÿçÇ ;:.,?!+-/*=\'`()€#’&]+', '', w)
    if (temp != w):
        w = temp
    return w

def rplace(w, liste):
    """test si un mot est dans une liste et le cas échéant le remplace par le mot en position 0 de la liste où il est présent

    Args:
        w (string): un mot
        liste (liste de string)): liste de mot

    Returns:
        string: le mot modifé ou non
    """
    for e in liste:
        if w in e:
            w = e[0] 
    return w

def countL(data):
    """ compter le nombre de lignes d'un fichier
    Args:
        data (fichier): un fichier

    Returns:
        int : nombre de lignes
    """
    result = 0
    with open(data, 'r') as file:
        for line in file:
            result +=1
        return result
