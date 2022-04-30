"""
    Lib de fonctions pour vérifier les occurences de mots/expression clef dans un dataset
"""
resultat = {}

def loadDataset(file, dico):
    """Charge un fichier keywords et le transforme en dictionnaire

    Args:
        file (fichier): fichier keywords correspondant
        dico (dictionnaire): dictionnaire vide
    """
    with open(file, 'r') as file:
        for line in file:
            resultat[line.split("\n")[0]] = 0

def recordic(file, dico):
    """Parcours un dataset et vérifie le nombre d'occurence des clefs d'un dictionnaire 

    Args:
        file (fichier): dataset
        dico (dictionnaire): dictionnaire de mot clés
    """
    dico["LINE"] = 0
    with open(file, 'r') as file:
        for e in file:
            dico["LINE"] += 1
            for k in dico.keys():
                if(k in e):
                    dico[k] +=1

def rapportR(dico, out):
    """représente le rapport sur un dataset en fonction des mots clés relatif ou constitutif de sa formation

    Args:
        dico (dictionnaire): dictionnaire des mots clés
        out (fichier): fichier de sortie
    """
    with open(out, 'a') as file:
        for k in dico.keys():
            if(k != "LINE"):
                file.write(f"{k}:{dico[k]}/{round(dico[k]/dico['LINE']*100, 4)}%\n")
