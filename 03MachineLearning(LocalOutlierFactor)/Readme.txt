01Nettoyage:
TestsNettoyage: test initiaux de nettoyages :
 |_ simpleCleanV0 : 		Utilisation d'un dictionnaire pour valider les mots retenu et lemmatisation
 |_ simpleCleanV0_min:		Nettoyage minimal avec lemmatisation
 |_ OneMillionTweetsFr.sql: 	Dataset avec toutes les features d'enregistrement

LexHaine.txt:			Ensemble de liste de mot relatifs au domaine de l'instulte afin d'effecturer un renforcement ciblé de correction orthographique.
				(d'après https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Insultes_en_fran%C3%A7ais)
LibClean.py:			Ensemble de fonction python pour nettoyer, normaliser et formatter les jeux de données.
MillionTweets.txt: 		Scrap de plus d'un million de tweets au hasard brut
MillionTweets_NEF.txt:		Scrap de plus d'un million de tweets au hasard brut sans les lignes vides de MillionTweetsMin
MillionTweetsMin.txt: 		Les données ont été nettoyées
MillionTweetsMin_NEF.txt: 	Les données ont été nettoyées sans ligne vide
MillionTweetsStd.txt: 		Les données ont été filtrées avec des stopwords et sont passées par une procédure de stemming
MillionTweetsStd_NEF.txt: 	Les données ont été filtrées avec des stopwords et sont passées par une procédure de stemming sans les lignes vides de 
Nettoyage.ipynb:		Notebook Jupyter présentant les fonctions de normalisation et de nettoyage
stopW.txt:			Liste de stop wors comprenant des variantes orthographique et amalgamer à partir de la liste de stop words de nltk.corpus et différentes sources
				(https://referencement-gratuit.and-co.ch/liste-stopwords-francais/ ,
				 https://countwordsfree.com/stopwords/french ,
				 https://github.com/stopwords-iso/stopwords-fr )
