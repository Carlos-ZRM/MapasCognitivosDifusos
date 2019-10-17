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
    return adyacence

def load_multiple_CSV(path):
    files = [ f for f in listdir(path) if isfile (join(path,f)) ]
    matriza={}
    for f in files :
    
        if f[-4:] == ".csv" or f[-4:] == ".CSV":
            matrizb = load_one_CSV(f)
            matriza = addMatriz(matriza,matrizb)
    print(matriza)
    return matriza
def addMatriz(matriza, matrizb):
    for i, j in matrizb.items():
        i = i.replace(" ","")
        i = i.lower()
        if i in matriza:
            pass
        else :
            matriza[i]=j
    return matriza
def adyacence_to_matrx(dict ):
    # dict 
    key_list =list( dict.keys() )
    vector = []
    print(key_list)
    l = len(key_list)
    mat = np.zeros( (l,l) )
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


    return mat 

def fuzzy_from_csv( path, opc = 'f' ):
    if opc == 'f':
        adyacence = load_one_CSV(path)
    elif opc == 'd':
        adyacence = load_multiple_CSV(path)
    #print(adyacence)
    
    mat = adyacence_to_matrx(adyacence)
    print(mat)
    return None

matriz = fuzzy_from_csv(".", 'd' )
