from graph import *

import igraph as ig


#Vérfie si les interactions dans le graphe contient les types d'interactions dans list_interactions 
#Dès qu'il y a un type d'interaction qui n'appartient au graphe, la fonction renvoie False
#Sinon si tous les types sont passés, la fontion renvoie True
def check_rare(graph,list_interactions):
    if list_interactions == []:
         return False
    else :
        for interaction in list_interactions :
            if interaction not in graph.es["interaction"]:
                    return True
        return False

# Cette fonction permet de soustraire des aretes de la liste des aretes sans 
# soustraire ces aretes du graphe lui-meme
def edges_substract (graph,to_delete):
    es = graph.es
    edges_indexes=[e.index for e in es]
    new_indexes=[index for index in edges_indexes if index not in to_delete]
    return ig.EdgeSeq(graph, new_indexes)


# Fonction qui prend la première arete sur le motif (le sous-graphe)
# et cherche une arete similaire (de meme type) dans le graphe 
# Si aucun tel arete n'existait dans le graphe, la fonction renvoie Faux
# sinon elle renvoie l'arete en question
def check_first(graph,subgraph,visited):
    sub_es_indexes = subgraph.incident(subgraph.vs[0],mode="all")
    sub_es = ig.EdgeSeq(subgraph, sub_es_indexes)
    es= edges_substract(graph,visited)
    try:
        e = es.find(interaction=sub_es[0]["interaction"])
        return e
    except ValueError:
        return False


# Retourne les index des noeuds dans la liste de tuples
def index_vertex(tupleList):
    list_indexes = []
    for tuple in tupleList:
        list_indexes.append((tuple[0]["name"],tuple[1]["name"]))
    return list_indexes


            
# A partir d'un noeud du sous-graphe et son similaire dans le graphe, la fonction vérifie
# si leurs aretes sont semblables et les retient dans des listes.
# Renvoie False si ses aretes ne sont semblables
def check_match_edges(graph,subgraph,vertex,v,tuple_vertex_visited,vertex_visited,subvertex_visited):

    es = ig.EdgeSeq(graph, graph.incident(vertex,mode="all"))
    sub_es = ig.EdgeSeq(subgraph, subgraph.incident(v,mode="all"))

    if (vertex,v) not in tuple_vertex_visited :
        tuple_vertex_visited.append((vertex,v))
        vertex_visited.append(vertex)
        subvertex_visited.append(v)

    visited=[]
    for s_edge in sub_es:
        n=0
        while (((s_edge["interaction"] != es[n]["interaction"]) ) or (n in visited)):
            n+=1
            if(n == len(es)):
                return False
        visited.append(n)

        if not((es[n].target_vertex,s_edge.target_vertex) in tuple_vertex_visited):
            if not((es[n].target_vertex in vertex_visited) or (s_edge.target_vertex in subvertex_visited)):
                tuple_vertex_visited.append((es[n].target_vertex,s_edge.target_vertex))
                vertex_visited.append(es[n].target_vertex)
                subvertex_visited.append(s_edge.target_vertex)

        if not((es[n].source_vertex,s_edge.source_vertex) in tuple_vertex_visited):
            if not((es[n].source_vertex in vertex_visited) or (s_edge.source_vertex in subvertex_visited)):
                tuple_vertex_visited.append((es[n].source_vertex,s_edge.source_vertex))
                vertex_visited.append(es[n].source_vertex)
                subvertex_visited.append(s_edge.source_vertex)



# A partir d'un arete choisi dans le graphe, on réalise des itérations
# où on avance noeud par noeud et on vérifie si un tel motif existe dans le graphe
# Renvoie True si le graphe contient le graphe, False sinon
def iterations(graph,subgraph,edge_chosen):
    tuple_vertex_visited =[]
    vertex_visited=[]
    subvertex_visited=[]
    sub_vs = subgraph.vs
    for v in sub_vs:
        if len(subvertex_visited) == 0:
            vertex = edge_chosen.source_vertex
        else:
            n=0
            while v != tuple_vertex_visited[n][1]:
                n+=1
                if n == len(vertex_visited):
                    return (False,[])
            vertex = tuple_vertex_visited[n][0]
        if vertex.degree() < v.degree():
            return (False,[])
        if check_match_edges(graph,subgraph,vertex,v,tuple_vertex_visited,vertex_visited,subvertex_visited) == False:
            return (False,[])
    return (True,index_vertex(tuple_vertex_visited))


# La fonction choisit un arete du graphe et réalise des itérations 
# pour rechercher le motif.
# Si la recherche échoue, la fonction commence par un autre arete et 
# effectue la recherche.
# Si la fonction ne trouve plus d'aretes de départ valables, la fonction
# renvoie False, sinon True
def search_algorithm(graph,subgraph,list_interactions):
    to_delete = []
    if check_rare(graph,list_interactions) == True:
        return (False,[])
    edge_chosen = check_first(graph,subgraph,to_delete)
    if edge_chosen == False:
        return (False,[])
    b = iterations(graph,subgraph,edge_chosen)
    while b[0] == False:
        to_delete.append(edge_chosen.index)
        edge_chosen = check_first(graph,subgraph,to_delete)
        if edge_chosen == False:
            return (False,[])
        b = iterations(graph,subgraph,edge_chosen)
    return b

