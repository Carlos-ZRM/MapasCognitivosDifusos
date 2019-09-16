import numpy as np 
import math
import pygraphviz as pgv
import functools 
from PIL import Image
import matplotlib.pyplot as plt


def fuzzy( vector , mapa , t ):
    '''
        Funcion que calcula el mapa difuso y retorna el valor  
        de la funcion f en f(t)

        Parameters
        ----------
        vector : array_like
            Vector numpy que representa el arreglo de pesos
        mapa  : array_like
            Matriz de adyacencia que representa el mapa
        t : int
            Numero de iteraciones de la funcion 

        Returns
        -------
        new vector : array_like
            Vector de pesos resultante f(t)
    '''
    soluciones = [vector]
    vector_aux = vector
    # Se itera la funcion t veces
    for i in range( t ):
        #Multiplicacion vector de estados y matriz
        vector_aux = np.dot(vector_aux, mapa)
        #Aplicacion de la normalizacion o parametrizacion
        sigmoide(vector_aux)
        soluciones.append(vector_aux)
    saveHistograma(soluciones)
    return vector_aux, soluciones


def sigmoide ( vector ):
    for i in range (len(vector )):
        x = vector[i]
        vector[i] = 1/(1+math.exp(-1*x)) 

def outDegree(graph):
    resultado = np.absolute(graph)
    resultado = np.sum(resultado, axis = 1)
    return resultado
def inDegree(graph):
    resultado = np.absolute(graph)
    resultado = np.sum(resultado, axis = 0)
    return resultado
def density(graph):
    d = np.count_nonzero(graph)
    n = len(graph)
    d = d/(n*(n-1))
    return d 
def hierarchy (outdegree):
    acumulate = 0.
    n = len(outdegree)
    suma = 0.
    suma = np.sum(outdegree)

    for i in outdegree :
        #suma += i
        x = (i - suma)/(n)
        x = x**2
        acumulate = acumulate + x
    acumulate = (12/(n**3-n))*acumulate
    return acumulate

def saveDot(grafo, label, name):
    tf = open(name, 'w')
    tf.write("digraph G {\n")
    # imprime nodos 
    # A [label="King Arthur"]
    for i in range(len(label)):
        tf.write( "A"+str(i)+ " [label=\""+label[i]+"\"];\n" )
    tf.write("\n")
    for i in range (len(grafo)):
        for j in range (len(grafo)):
            if grafo[i][j]!=0:
                tf.write("A"+str(i)+" -> A"+ str(j)+" [label=\""+str(grafo[i][j]) +"\"];\n" )
    
    tf.write("\n}")
    tf.close()

def saveHistograma(vector):
    vec = np.transpose(vector)
    x = np.size(vec,0)
    y =np.size(vec,1)
    t = range(y) 
     #for i in range(x):

    #print(vec[0],np.size(vec,0) , np.size(vec,1))

    for i in range( x ):
        #plt.subplot(x, 1, i+1)
        plt.plot(t, vec[i], '-', lw=1)
        plt.grid(True)
        plt.ylim( 0, 1 )
    plt.tight_layout()
    plt.show()

def loadGraph(path):
    B = pgv.AGraph(path)
    B.layout(prog = 'circo') # layout with default (neato)
    B.draw(path[:-3]+'png') # draw png


label = ["AoF","FP","P","L","EoL"]
file = "Fuzzy"
C = np.array([1,1,1,1,1])
B = np.array([[ 0.0 , 1.0 ,-0.1, 0.8 , 0.0 ],
              [ 0.0 , 0.0 , 0.0, 1.0 , 0.0 ],
              [-0.2 ,-1.0 , 0.0,-0.2 , 0.0 ],
              [ 0.0 , 0.0 , 0.0, 0.0 , 0.0 ],
              [ 0.2 , 0.5 ,-0.5,-0.2 , 0.0 ]
            ])

C , soluciones = fuzzy( C ,B , t = 10 )
od = outDegree(B)
id = inDegree(B)
cd = od+id
den = density(B)
hier = hierarchy(od)

saveDot(B, label, name = file+".dot")
loadGraph(file+".dot")
print("\nInput : Mapa Cognitivo Difuso ")
print(B)
print("Output : Dregrees ")

print("Out Degree", od)
print("In Degree", id)
print("Centrality Degree", cd )
print("Density ", den )
print("Hierarchy ", hier )
print("\n\n Vector de estados",C)
im = Image.open(file+".png")
im.show()
