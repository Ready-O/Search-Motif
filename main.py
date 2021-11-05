from input import *
from graph import *
from algorithm import *
from search_motif import *
import igraph as ig

# Ce fichier représente l'interface communiquant avec l'utilisateur

arnList = getAllARN()
print(str(len(arnList))+" ARNs chargées\n")
print("Pour afficher le graphe modélisant une ARN : entrer 1\nPour la recherche de motif : entrer 2\nPour arrêter : entrer 0")
command = input("Votre commande : ")

def apply_command(command):
	if (str(command) == str(1)):
		print("\n--------Affichage de graphe--------\n")
		name = input("Entrez le nom de l'ARN que vous souhaitez afficher : ")
		visualizeGraph(getGraphARN(getARN(arnList,name)))
		command = input("\nEntrer 1 si vous voulez afficher le graphe d'une autre ARN.\nEntrer 2 pour la recherche de motif.\nEntrer 0 pour arrêter.\nVotre commande :")
		apply_command(command)
	elif (str(command) == str(2)):
		print("\n--------Recherche de motif--------\n")
		print("Choisissez un de ces motifs en entrant son numéro")
		print("Les motifs disponibles : 8 - 198")
		motif = input("Votre choix : ")
		if (str(motif) != str(198) and str(motif) != str(8)):
			print("Motif indisponible !\n")
			print("Entrer 2 si vous voulez recommencer la recherche de motif")
			print("Entrer 1 si vous afficher un graphe d'une ARN")
			print("Entrer 0 pour quitter")
			command = input("Votre commande : ")
			apply_command(command)
		else:
			print("\nPour vérifier si une certaine ARN contient le motif séléctionné, entrer 1")
			print("Pour identifier les structures d’ARN contenant le motif séléctionné, entrer 2")
			command2 = input("Votre commande : ")
			apply_command_search(command2,int(motif))
			print("Entrer 2 si vous voulez recommencer la recherche de motif")
			print("Entrer 1 si vous afficher un graphe d'une ARN")
			print("Entrer 0 pour quitter")
			command = input("Votre commande : ")
			apply_command(command)
	elif (str(command) == str(0)):
		print("Au revoir !")
	else :
		print('Commande invalide !\n')
		print("Pour afficher le graphe modélisant une ARN : entrer 1\nPour la recherche de motif : entrer 2\nPour arrêter : entrer 0")
		command = input("Votre commande : ")
		apply_command(command)


def apply_command_search(command,motif):
	if (str(command) == str(1)):
		name = input("Entrez le nom de l'ARN pour vérifier s'il contient RIN#"+str(motif)+" : ")
		check = oneCheck(arnList,motif,name)
		print("Réponse : "+str(check[0])+"\n")
		print("Entrer 3 si vous voulez voir les nucléotides constituant le motif dans l'ARN\n")
		print("Entrer 2 si vous voulez identifier les structures d’ARN contenant le motif")
		print("Entrer 1 si vous voulez vérifier si une certaine ARN contient le motif séléctionné")
		print("Entrer 0 pour revenir au menu principal")
		command = input("Votre commande : ")
		if (str(command) == str(3)):
			print("Détails (le nucléotide à droite du tuple appartient au motif et son correspondant dans l'ARN est celui à gauche) : ")
			print(check[1])
			print("\nEntrer 2 si vous voulez identifier les structures d’ARN contenant le motif")
			print("Entrer 1 si vous voulez vérifier si une certaine ARN contient le motif séléctionné")
			print("Entrer 0 pour revenir au menu principal")
			command = input("Votre commande : ")
			apply_command_search(command,motif)
		apply_command_search(command,motif)
	elif (str(command) == str(2)):
		print("Recherche des structures d’ARN contenant le motif ... ")
		list = arnsCheck(arnList,motif)
		print("La liste des ARNs où le motif est identifié :" )
		print(list)
		print("Le nombre d'occurences est :" + str(len(list))+"\n\n")
		print("Entrer 2 si vous voulez identifier les structures d’ARN contenant le motif")
		print("Entrer 1 si vous voulez vérifier si une certaine ARN contient le motif séléctionné")
		print("Entrer 0 pour revenir au menu principal")
		command = input("Votre commande : ")
		apply_command_search(command,motif)
	elif (str(command) == str(0)):
		print("\n")
	else :
		print('Commande invalide !\n')
		print("Entrer 2 si vous voulez identifier les structures d’ARN contenant le motif")
		print("Entrer 1 si vous voulez vérifier si une certaine ARN contient le motif séléctionné")
		print("Entrer 0 pour revenir au menu principal")
		command = input("Votre commande : ")
		apply_command_search(command,motif)

apply_command(command)