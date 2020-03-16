#!/usr/bin/env python3
#sudo cp ex1 /usr/local/bin

import fileinput
import re
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def getTexto():
    texto = ""

    for line in fileinput.input():
        texto += line

    return texto

def frases(texto): 
    exp1 = r'(\n\n+\s*)([A-Z])' 
    exp2 = r'([a-z][.?!]+[\s]*)([A-Z])' 

    texto = re.sub(exp1,r'\1@\2',texto)
    texto = re.sub(exp2,r'\1@\2',texto)
    return texto


def entidades(texto):
    maius = r'(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.|[IVXLCDM]+)'
    de = r'(?:de|da|dos|das)' 
  
    s = r'\s+'
    ent = f"([^@\w])({maius}(?:{s}{maius}|{s}{de}{s}{maius})*)"

    texto = re.sub(ent, r'\1{\2}', texto)
    return texto


def getPairs(texto):
    frs = [] 
    pares = []
    frs = texto.split('@')
    for fr in frs:
        aux = re.findall('{[\w|\s]+}', fr)
        ents = []
        for e in aux:
            e = e[1:-1]
            ents.append(e)

        if len(ents) > 1:
            for pair in itertools.combinations(ents,2): 
                pares.append(pair)
    return pares    
        

def cleanupPairs(pares):
    pairs = []

    terms = ["I", "We", "Us", "They", "He", "Her", "Them", "It", "You", "Your", "My", "His", "And", "But", "Still", "Then", 
    "There", "That", "This", "The", "How","Now", "So", "Are", "Not", "Or", "What", "Where", "Which", "Why", "Well", "See", 
    "Something", "Thanks", "Stop", "Yes", "Yeah", "No", "In", "Oh", "Mrs", "Mr", "An", "All", "Just","Go","Good","If I",
    "If","Do","KILL HIM","She","D","Professor","Invisibility", "GRYFFINDORS SCORE", "Of","Want","Say","Mirror","OUCH","Listen",
    "Who","Page","Can","Christmas","Shut","Magic","Ministry","Er","Nothing","Right","Never","London","Yeh","House","Come",
    "Dark Arts","Look","Lucky"]

    for p in pares:
        if p[0] not in terms and p[1] not in terms and p[0] != p[1]:
            pairs.append(p)
    
    return pairs


def groupAndRemove(pairs):
    pairOccur = {}
    for p in pairs:
        if p in pairOccur:
            occ = pairOccur.get(p)
            occ += 1
            pairOccur.update({p : occ})
        else:
            if (p[1],p[0]) in pairOccur:
                inv = (p[1],p[0])
                occ = pairOccur.get(inv)
                occ += 1
                pairOccur.update({inv : occ})
            else:
                pairOccur[p] = 1

    for k,v in list(pairOccur.items()):
        if v < 5:
            pairOccur.pop(k)

    return pairOccur
    

def interpretador(pairOccur):
    char = input("Enter character from Harry Potter: ")
    top = input("Top K relationships: ")
    rels = {}
    i = 0
    for k,v in pairOccur.items():
        if k[0] == char or k[1] == char:
            rels[k] = v

    if len(rels) == 0:
        print("No relevant relationships found...")

    for w,v in sorted(rels.items(),key= lambda x : x[1], reverse=True):
        if i < int(top):
            print(w," --> ",v, "occurrences.")
            i+=1


def criaGrafo(pairs):
    lista_pares=[];
    g= nx.DiGraph()
   
    node_sizes=[]
    
    for k,v in pairs.items():
         lista_pares.append(k)

    resposta =  input("Do you want to see all the relationships? (yes|no)")

    if(resposta=="yes"):

        for i in  lista_pares: 
          g.add_edge(i[0],i[1]);
    
    elif(resposta == "no"): 
            nome = input("Enter character from Harry Potter: ")
            for i in  lista_pares:
                 if (i[0]==nome or i[1] ==nome): 
                     g.add_edge(i[0],i[1]);
    else:
        print("Error: follow the instructions!!!")

    for n in g:
        node_sizes.append(1000)


    print(nx.info(g))
   

    plt.figure()
    nx.draw_networkx(g,pos=nx.spring_layout(g,dim=2,k=1.5),node_size=node_sizes)
    plt.show()    



p = getPairs(entidades(frases(getTexto())))
occur = groupAndRemove(cleanupPairs(p))
interpretador(occur)
criaGrafo(occur)














