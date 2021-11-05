import igraph as ig

# Renvoie le graphe modélisant la chaine d’ARN
def getGraphARN(arn_without_name):

    # liste des interactions acceptées 
    list_interactions = ['cWW','tWW','cWH','cHW','tWH','tHW','cWS','cSW',
    'tWS','tSW','cHH','tHH','cHS','cSH','tHS','tSH','cSS','tSS']

    g = ig.Graph(directed=True)        # Le graphe est orienté
    indexes = []
    for properties in arn_without_name:
        paired = properties[1]
        pair_type = properties[3]
        if properties[2] == '0':            # si le nb_interact = 0 on ajoute uniquement le noeud
            g.add_vertex(properties[0])
            indexes.append(properties[0])
        else :
            #Lorsque l'on parcourt une nucléotide on stocke son index dans une liste mémoire
            #pour éviter d'ajouter le nucléotide plusieurs fois au graphe
            pair_types = [p for p in pair_type.split(',')]
            n = 0
            for pair in paired.split(','):     
                if not(properties[0] in indexes):
                    indexes.append(properties[0])
                    g.add_vertex(name=properties[0])

                # Si le noeud en lien est '0' (probablement inexistant) ou que l'interaction ne fait pas parmi des interactions qu'on veut traiter,
                # on les ignore
                if not((pair == '0') or (pair_types[n] not in list_interactions)):             
                    if pair not in indexes:
                        indexes.append(pair)
                        g.add_vertex(name=pair)
                        g.add_edge(properties[0],pair,interaction = pair_types[n])
                    else :
                        v = [v for v in g.vs if v["name"] == properties[0]][0]
                        if pair not in g.vs(g.neighbors(v,mode="all"))["name"]:
                            g.add_edge(properties[0],pair,interaction = pair_types[n])
                n+=1

    #Pour ajouter les aretes "squelettes", on trie la liste des nucleotides et on ajoute
    #une arete "squelette" entre chaque deux noeuds successifs s'il n'y a aucune arete entre eux
    int_indexes = [int(index) for index in indexes]
    int_indexes.sort()
    indexes = [str(index) for index in int_indexes]
    for i in range (0,len(indexes)-1):
        if not(g.are_connected(indexes[i],indexes[i+1])):
            g.add_edge(indexes[i],indexes[i+1],interaction = 'squeleton')
    return g


# Visualiser le graphe
def visualizeGraph(graph):
    graph.vs["label"] = graph.vs["name"]
    color_dict = {'cWW': "red",'tWW':"orange",'cWH':"blue",'cHW':"blue",'tWH':"lightblue",
    'tHW':"lightblue",'cWS':"green",'cSW':"green",'tWS':"lightgreen",'tSW':"lightgreen",'cHH':"yellow",'tHH':"gray",
    'cHS':"magenta",'cSH':"magenta",'tHS':"darkmagenta",'tSH':"darkmagenta",'cSS':"brown",'tSS':"cyan",'squeleton': "black"}
    graph.es["color"] = [color_dict[e] for e in graph.es["interaction"]]
    graph.vs["size"] = 23
    graph.vs["color"] = ["#f4ecf7"]
    layout = graph.layout("kk")

    class colors:
        CWW = '\033[31m'
        TWW = '\033[91m'
        CWH = '\033[36m'
        TWH = '\033[94m'
        CWS = '\033[32m'
        TWS = '\033[92m'
        CHH = '\033[93m'
        THH = '\033[37m'
        CHS = '\033[95m'
        THS = '\033[35m'
        CSS = '\033[16m'
        TSS = '\033[96m'
        ENDC = '\033[0m'

    print("\nLégende du graphe : ")
    print(f"{colors.CWW}CWW : red ------>{colors.ENDC}")
    print(f"{colors.TWW}TWW : orange ------>{colors.ENDC}")
    print(f"{colors.CWH}CWH / CHW: blue ------>{colors.ENDC}")
    print(f"{colors.TWH}TWH / THW: lightblue ------>{colors.ENDC}")
    print(f"{colors.CWS}CWS / CSW: green ------>{colors.ENDC}")
    print(f"{colors.TWS}TWS / TSW: lightgreen ------>{colors.ENDC}")
    print(f"{colors.CHH}CHH : yellow ------>{colors.ENDC}")
    print(f"{colors.THH}THH : gray ------>{colors.ENDC}")
    print(f"{colors.CHS}CHS / CSH: magenta ------>{colors.ENDC}")
    print(f"{colors.THS}THS / TSH: darkmagenta ------>{colors.ENDC}")
    print(f"{colors.CSS}CSS : brown ------>{colors.ENDC}")
    print(f"{colors.TSS}TSS : cyan ------>{colors.ENDC}")
    print("Squeleton : black ------>")

    ig.plot(graph,layout = layout)
