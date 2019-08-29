import numpy as np 
import math
import pygraphviz as pgv
import functools 
from PIL import Image

def fuzzy( A , B , t):
    C = A
    for i in range( t ):
        C = np.dot(C,B)
        C = np.array([ 1/(1+math.exp(-1*x)) for x in C ])
    return C
def outDegree(graph):
    result = []
    for i in graph: 
        od = functools.reduce(lambda x,y: abs(x) + abs(y), i  )
        result.append(od)
    return result 
def inDegree(graph):
    result = np.zeros((1,len(graph)))
    for i in graph:
        result = np.absolute(result)+np.absolute(i)
    return result

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

C = fuzzy( C ,B , t = 20 )
saveDot(B, label, name = file+".dot")
loadGraph(file+".dot")
print("\nInput : Mapa Cognitivo Difuso ")
print(B)
print("Output : Dregree ")
od = outDegree(B)
id = inDegree(B)
cd = od+id
print("Out Degree", od)
print("In Degree", id)
print("Centrality Degree", cd)
print("\n\n Vector de estados",C)
im = Image.open(file+".png")
im.show()
#C2 = np.array( map(lambda x: 1/(1+math.exp(-x)), C)) 


