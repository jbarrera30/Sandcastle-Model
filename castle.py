'''
Created on 26 May 2020

@author: Petros Laptop
'''
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def createCastle(w,l,h,shape):
    
    base = np.ones((l,w))
    
    showCastle(base,h,shape)

def showCastle(base,h,shape):
    
    x = base[0]
    y = base[:,0]
    
    for i in range(0,len(x)):
        x[i] = x[i] + i 

    for i in range(0,len(y)):
        y[i] = y[i] + i 
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x,y,z,ax = shapeCastle(x,y,h,ax,shape)
        
    axes = plt.gca()
    plt.title("Sandcastle")
    dim = max(len(x), len(y), len(z))
    axes.set_xlim(0,dim)
    axes.set_ylim(0,dim)
    axes.set_zlim(0,dim)
    axes.set_xticks(x)  
    axes.set_yticks(y) 
    axes.set_zticks(z) 
    ax.set_xlabel("Width")
    ax.set_ylabel("Length")
    ax.set_zlabel("Height")
    plt.show()

def shapeCastle(x,y,h,ax,shape):
    
    z = []
    
    if(shape=="rectangular"):
        
        for i in range(0,h):
            Z = i
            z.append(Z)
            X, Y = np.meshgrid(x, y)
            ax.scatter(X,Y,Z, c='y', marker= "s", s=100)
    
    if(shape=="pyramid"):
        
        for i in range(0,h):
            x[i] = None
            x[len(x)-1-i]= None
            y[i] = None
            y[len(y)-1-i]=None
            Z = i
            z.append(Z)
            X, Y = np.meshgrid(x, y)
            ax.scatter(X,Y,Z, c='y', marker= "s", s=100)
            
    return x,y,z,ax
        
def main():
    
    '''
    study other shapes and include them
    '''
    createCastle(15,30,10,"rectangular")
    createCastle(20,20,10,"pyramid")
      
main()
