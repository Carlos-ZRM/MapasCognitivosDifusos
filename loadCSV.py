import csv 
import numpy as np 
from os import listdir
from os.path import isfile, join

def load_one_CSV(file):
    adyacence= {}
    vector = []
    nodes = []
    csv.register_dialect('myDialect',
    delimiter = ',',
    skipinitialspace=True)
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            d = dict(row)
            n = d['node']
            n = n.replace(" ","")
            n = n.lower()
            #v = d['vector']
            d.pop('node')
            adyacence[n]= d
    csvfile.close()

    #print("\n**",adyacence,"\n**")
    return adyacence

def load_multiple_CSV(path):
    files = [ f for f in listdir(path) if isfile (join(path,f)) ]
    matriza={}
    for f in files :
    
        if f[-4:] == ".csv" or f[-4:] == ".CSV":
            matrizb = load_one_CSV(f)
            addMatriz(matriza,matrizb)
            
    return matriza
def addMatriz(matriza, matrizb):
    for i, elements in matrizb.items():
        i = i.replace(" ","")
        i = i.lower()
        if i in matriza:
            # Si esta en el vector original se recupera
            va = matriza[i]
            
            for j, k  in elements.items():
                
                # se recorren los elementos del vector b
                # se verifica si j el indice esta en el vector a
                # Si esta se suman 
                if j in va:
                    #print(va[j])
                    x = float(va[j])
                    y = float(elements[j])
                    
                    va[j]= str(x+y)
                # si no se agrega 
                else :
                    va[j]=k
            
        else :
            matriza[i]=elements
    return matriza
def adyacence_to_matrx(dict ):
    # dict 
    key_list =list( dict.keys() )
    #key_list = list(map(lambda x : x.replace(" ",""),key_list))
    vector = []
    #print(key_list)
    l = len(key_list)
    mat = np.zeros( (l,l) ,dtype=float)
    for i, elements in dict.items():
        # x --> y mät¨[x][y]
        
        x = key_list.index(i)
        v = elements['vector']
        elements.pop('vector')
        vector.append(v)
        for j, k in elements.items():
            j = j.replace(" ","")
            j = j.lower()
            y = key_list.index(j)
            mat[x][y] = float (k)


    return key_list , mat , vector 

def fuzzy_from_csv( path, opc = 'f' ):
    if opc == 'f':
        adyacence = load_one_CSV(path)
    elif opc == 'd':
        adyacence = load_multiple_CSV(path)
    ##print(adyacence)
    key_list , mat , vector = adyacence_to_matrx(adyacence)
    
    return key_list , mat , np.array(vector,dtype=float)

#matriz = fuzzy_from_csv(".", 'd' )
#print(matriz)