import numpy as np 
import math
import networkx as nx
import pygraphviz as pgv
from PIL import Image
import matplotlib.pyplot as plt

"""Example NumPy style docstrings.

This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.

Example
-------
Examples can be given using either the ``Example`` or ``Examples``
sections. Sections support any reStructuredText formatting, including
literal blocks::

    $ python example_numpy.py


Section breaks are created with two blank lines. Section breaks are also
implicitly created anytime a new section starts. Section bodies *may* be
indented:

Notes
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.

If a section is indented, then a section break is created by
resuming unindented text.

Attributes
----------
module_level_variable1 : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.


.. _NumPy Documentation HOWTO:
   https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

"""


class FuzzyMap:
    def fuzzy(self,  vector , mapa , t, function=None ):
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
            if function is None :
                sigmoide(vector_aux)
            else :
                vector_aux = function(vector_aux)
            soluciones.append(vector_aux)
        
        return vector_aux, soluciones

    def sigmoide ( self, vector ):
        for i in range (len(vector )):
            x = vector[i]
            vector[i] = 1/(1+math.exp(-1*x)) 

    def outDegree(self, graph):
        resultado = np.absolute(graph)
        resultado = np.sum(resultado, axis = 1)
        return resultado
    def inDegree(self, graph):
        resultado = np.absolute(graph)
        resultado = np.sum(resultado, axis = 0)
        return resultado
    def density(self, graph):
        d = np.count_nonzero(graph)
        n = len(graph)
        d = d/(n*(n-1))
        return d 
    def hierarchy (self, outdegree):
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

    def saveDot(self,  grafo, label, name):
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

    def saveHistograma(self, vector, labels):
        vec = np.transpose(vector)
        x = np.size(vec,0)
        y =np.size(vec,1)
        t = range(y) 
        #for i in range(x):

        fig, ax = plt.subplots()
        #print(vec[0],np.size(vec,0) , np.size(vec,1))
        #fig, ax = plt.subplots()
        for i in range( x ):
            #plt.subplot(x, 1, i+1)
            ax.plot(t, vec[i], '-', lw=.5 , label=labels[i]  )
            plt.grid(True)
            plt.ylim( 0, 1 )
        plt.legend()
        plt.tight_layout()
        plt.show()


    def loadGraph(self, path):
        #G = nx.Graph(nx.drawing.nx_agraph.read_dot(path))
        B = pgv.AGraph(path)
        B.layout(prog = 'circo') # layout with default (neato)
        B.draw(path[:-3]+'png') # draw png
     
    def makeSquashFunction(self, lambdaU):
        vfunc = np.vectorize(lambdaU)
        return vfunc

    def __init__(self, proyect,label, vector_array, map_array, lambdas = None  ):
        t = 10
        self.proyect=proyect
        self.label = label 
        self.vector_array = vector_array
        self.map_array = map_array
        if lambdas is None:
            
            self.vector_array, soluciones = self.fuzzy( self.vector_array , self.map_array , t )
        
        else :
            f = self.makeSquashFunction(  l )
                
            self.vector_array, soluciones = self.fuzzy( self.vector_array , self.map_array , t , f)
            
        
        od = self.outDegree( self.map_array )
        id = self.inDegree(self.map_array )
        cd = od+id
        den = self.density(self.map_array )
        #hier = hierarchy(od)
        print("\nInput : Mapa Cognitivo Difuso ")
        print(self.map_array )
        print("Output : Dregrees ")
        print("Out Degree", od)
        print("In Degree", id)
        print("Centrality Degree", cd )
        print("Density ", den )
        #print("Hierarchy ", hier )
        print("\n\n Vector de estados",self.vector_array)
        
        self.saveDot(self.map_array , self.label, name = self.proyect +".dot")
        self.loadGraph(self.proyect+".dot")
        
        im = Image.open(self.proyect+".png")
        im.show()
        self.saveHistograma(soluciones, self.label )


label = ["AoF","FP","P","L","EoL"]
proyect  = "Proyecto1"
vector_array = np.array([1,1,1,1,1])
map_array = np.array([[ 0.0 , 1.0 ,-0.1, 0.8 , 0.0 ],
                [ 0.0 , 0.0 , 0.0, 1.0 , 0.0 ],
                [-0.2 ,-1.0 , 0.0,-0.2 , 0.0 ], 
                [ 0.0 , 0.0 , 0.0, 0.0 , 0.0 ],
                [ 0.2 , 0.5 ,-0.5,-0.2 , 0.0 ]
            ])
l = lambda x : 1/(1+math.exp(-1*x)) 
    
f =  FuzzyMap(  proyect,label, vector_array, map_array, lambdas = l)
