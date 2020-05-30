'''
Created on 26 May 2020

@author: Petros Laptop
'''
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import *
from mpl_toolkits.mplot3d import Axes3D 
import mpl_toolkits.mplot3d.art3d as art3d

def createCastle(w,l,height,shape):
    
    if(shape=="rectangular" or shape =="pyramid"):
        base = np.ones((l,w))
    if(shape=="rhombus"):
        base = np.zeros((l,w))
        midL= int( (len(base)-1) /2)
        midR = np.ceil( (len(base)-1) /2)
        for i in range(0,int(np.ceil(len(base)/2))):
            for j in range(0,len(base[i])):
                if(j>= (midL - i) and j <= (midR + i) ):
                    base[i][j]=1
                    base[len(base)-i-1][j]=1
                    
    if(shape=="cylinder"):
        base = np.zeros((l+1,w+1))
        radius = w/2
        thetas = np.linspace(0, 2*math.pi)
        for theta in thetas:
            x= (radius * (math.cos(theta))) + w/2
            y= (radius * (math.sin(theta))) + w/2
            xlow = min(x,radius)
            xhi = max(x,radius)
            ylow = min(y,radius)
            yhi = max(y,radius)
            
            for i in range(round(xlow),round(xhi)):
                for j in range(round(ylow),round(yhi)):
                    base[i][j]=1
                    
    showCastle(base,height,shape)

def showCastle(base,height,shape):
    
    fig = plt.figure()
    ax=fig.gca(projection='3d')
    
    layers=1
    
    for h in range(0,height):
        base = shapeCastle(base,h,shape)
        for i in range(0,len(base)):
            for j in range(0,len(base[0])):
                if(base[i][j]==1):
                    for k in range(0,layers):
                        thickness = k/layers
                        rect = Rectangle((i, j), 1, 1)
                        rect.set_facecolor("y")
                        ax.add_patch(rect)
                        art3d.pathpatch_2d_to_3d(rect, h+thickness, zdir="z")
                    
    ax.set_xlim3d(0,len(base)*1.5)
    ax.set_ylim3d(0,len(base)*1.5)
    ax.set_zlim3d(0,height*1.5)
    axes = plt.gca()
    plt.title("Shape of Sandcastle: "+ shape)
    ax.set_xlabel("Width")
    ax.set_ylabel("Length")
    ax.set_zlabel("Height")
    plt.show()
    
def shapeCastle(base,h,shape):
    
    
    if(shape=="rectangular"):
        pass
    if(shape=="rhombus"):
        pass
    
    if(shape=="pyramid"):
        
        for i in range(0,len(base)):
            for j in range(0,len(base[0])):
                base[h][j]= 0 
                base[len(base)-1-h][j]=0
                base[i][h]=0
                base[i][len(base[0])-1-h]=0
                    
    return base
        
def main():
    
    '''
    study other shapes and include them
    '''
    createCastle(20,20,10,"cylinder")
    createCastle(20,20,20,"rhombus")
    createCastle(15,30,10,"rectangular")
    createCastle(25,25,10,"pyramid")
      
main()
