import os
import csv

# Construit des ARN sous forme de liste pour chaque fichier csv dans un dossier.
# Le format d'une ARN : [nom de l'ARN, [index_chain,paired,nb_interact,pair_type_LW]]
def getAllARN():
    all_arn = []
    path_input = input("Entrer le chemin vers les fichers csv à traiter : ")    # On récupère le dossier où se trouve les fichiers csv
    files_names = os.listdir(path_input)
    for filename in files_names:
        with open(os.path.join(path_input,filename), 'r') as arnFile:
            reader = csv.reader(arnFile, delimiter=',')
            next(reader)                    # on saute la 1ère ligne
            nucleotides=[]                  # liste qui contiendra tous les nucléotides avec leurs interactions
            for ligne in reader:
                nucleotides.append([ligne[0],ligne[12],ligne[13],ligne[14]])
            all_arn.append([filename,nucleotides])
    return all_arn


# Renvoie une ARN (sous forme de liste) à partir d'une liste d'ARN
def getARN(arnList,name):
    for arn in arnList :
        if arn[0]==name:
            return arn[1]
