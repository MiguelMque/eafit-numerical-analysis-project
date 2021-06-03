import pandas as pd
import numpy as np
import sympy as sym
from pylab import mpl
import math

class Interpolation_Methods:

    def __init__(self, data : pd.DataFrame):

        self.data = data
        self.x = np.arange(0,self.data.shape[0],1)
        self.y = self.data.tolist()
        self.xx=self.x.tolist()

        k=len(self.y)
        i=0
        self.lista_x=[]
        self.lista_y=[]
        while (i<k):
          if pd.isna(self.y[i]):
            self.lista_y.append(self.y.pop(i))
            self.lista_x.append(self.xx.pop(i))
            k=len(self.y)
            i=0
          else:
            i+=1
        
    def newton_interpolation(self,X,Y,x):

        sum=Y[0]
        temp=np.zeros((len(X),len(X)))

        # Asignar la primera línea
        for i in range(0,len(X)):
            temp[i,0]=Y[i]

        temp_sum=1.0

        for i in range(1,len(X)):

            #x polinomio
            temp_sum=temp_sum*(x-X[i-1])

            # Calcular diferencia de medias
            for j in range(i,len(X)):
                temp[j,i]=(temp[j,i-1]-temp[j-1,i-1])/(X[j]-X[j-i])

            sum+=temp_sum*temp[i,i] 

        return sum

    def lagrange_interpolation(self,xi,fi):

        n = len(xi)
        x = sym.Symbol('x')
        polinomio = 0
        divisorL = np.zeros(n, dtype = float)

        for i in range(0,n,1):
            
            # Termino de Lagrange
            numerador = 1
            denominador = 1
            for j  in range(0,n,1):
                if (j!=i):
                    numerador = numerador*(x-xi[j])
                    denominador = denominador*(xi[i]-xi[j])
                    
            terminoLi = numerador/denominador

            polinomio = polinomio + terminoLi*fi[i]
            divisorL[i] = denominador

        # simplifica el polinomio
        polisimple = polinomio.expand()

        # para evaluación numérica
        px = sym.lambdify(x,polisimple)

        # Puntos para la gráfica
        muestras = 101
        a = np.min(xi)
        b = np.max(xi)
        pxi = np.linspace(a,b,muestras)
        pfi = px(pxi)

        return polisimple