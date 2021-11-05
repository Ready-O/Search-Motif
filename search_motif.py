from input import *
from graph import *
from algorithm import *

import igraph as ig

#RIN 8
motif8 = [['1','5','1','cSS'],['2','3','1','tSS'],['3','2,4','1','tSS,cWW'],['4','3','1','cWW'],['5','1','1','cSS']]


#RIN 198
motif198 = [['1','3,4','2','cWS,cHS'],['2','4','1','cWW'],['3','1','1','cSW'],['4','1,2','2','cSH,cWW']]


# Renvoie les interactions rares (qui ne sont pas cWW ou squeleton) contenues dans le graph 
#    *Cette fonction sera utilisée pour extraire les interactions du motif
def getRare(subgraph):
    interactions = []
    common = ["squeleton","cWW"]
    for interaction in subgraph.es["interaction"]:
        if interaction not in common and interaction not in interactions :
            interactions.append(interaction)
    return interactions

# Applique l'algorithme de recherche sur une arn à partir d'un graphe de motif
def arnCheck(arn,subgraph,rare_interactions):
    graph = getGraphARN(arn)
    b = search_algorithm(graph,subgraph,rare_interactions)
    return b

# à partir d'un nom d'ARN et d'une liste d'ARNs, la fonction extraie l'ARN avec le nom 
# désigné et vérifie s'il contient le motif
#   *La fonction renvoie aussi la liste des nucléotides formant le motif dans le graphe
def oneCheck(arnList,motif,name):
    if (motif == 198):
        subgraph = getGraphARN(motif198)
    else:
        subgraph = getGraphARN(motif8)
    arn = getARN(arnList,name)
    return arnCheck(arn,subgraph,getRare(subgraph))

# On renvoie la liste des arns contenant dans le motif à partir d'une liste initial d'ARNs
def arnsCheck(arnList,motif):
    if (motif == 198):
        subgraph = getGraphARN(motif198)
    else:
        subgraph = getGraphARN(motif8)
    rare_interactions = getRare(subgraph)
    yes = []
    cnt = 0
    for arn in arnList :
        if arnCheck(arn[1],subgraph,rare_interactions)[0] == True:
            cnt += 1
            print(str(cnt)+" ARNs trouvées", end='\r') 
            yes.append(arn[0])
    return yes




