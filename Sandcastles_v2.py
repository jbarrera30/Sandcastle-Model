'''
Created on 31 May 2020

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

visualise = False
 
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
     
    castle = [np.copy(base)]
    for h in range(1,height):
        layer = shapeCastle(base,h,shape)
        castle.append(np.copy(layer))
    if(visualise):
        showCastle(castle,shape) 
    return castle

def shapeCastle(base,h,shape):
    
    if(shape=="rectangular"):
        pass
    if(shape=="rhombus"):
        pass
    
    if(shape=="pyramid"):
        h=h-1
        for i in range(0,len(base)):
            for j in range(0,len(base[0])):
                base[h][j]= 0 
                base[len(base)-1-h][j]=0
                base[i][h]=0
                base[i][len(base[0])-1-h]=0
                    
    return base

def showCastle(castle,shape):
    
    fig = plt.figure()
    ax=fig.gca(projection='3d')
    
    stacks=1
    height = len(castle)
    
    for h in range(0,height):
        layer = castle[h]
        for i in range(0,len(layer)):
            for j in range(0,len(layer[i])):
                if(layer[i][j]==1):
                    for k in range(0,stacks):
                        thickness = k/stacks
                        rect = Rectangle((i, j), 1, 1)
                        rect.set_facecolor("y")
                        ax.add_patch(rect)
                        art3d.pathpatch_2d_to_3d(rect, h+thickness, zdir="z")
                    
    ax.set_xlim3d(0,len(castle[0])*1.5)
    ax.set_ylim3d(0,len(castle[0][0])*1.5)
    ax.set_zlim3d(0,height*1.5)
    axes = plt.gca()
    plt.title("Shape of Sandcastle: "+ shape)
    ax.set_xlabel("Width")
    ax.set_ylabel("Length")
    ax.set_zlabel("Height")
    plt.show()
    
def volume(castle):
    
    volume = 0
    for layer in castle:
        for i in range(len(layer)):
            for j in range(len(layer[i])): 
                volume += layer[i][j]
    return volume  

def setupParameters(condition):
    
    if(condition=="Calm"): 
        i=0 
    if(condition=="Regular"):
        i=1 
    if(condition=="Windy"):
        i=2 
    
    '''include the other options after studying waves'''  
    freqMeans = [8]
    freqStdevs = [3]
    heightMeans = [15]
    heightqStdevs = [9]
    speedMeans = [4]
    speedStdevs = [1]
    
    return [freqMeans[i], freqStdevs[i], heightMeans[i], heightqStdevs[i], speedMeans[i], speedStdevs[i]   ]
    
def waves(parameters):
    
    rc = createCastle(10,5,30,"rectangular")
    t=0
    print("The volume of the sandcastle at time "+ str(t) + "= " +str(volume(rc)))
    hits=[]
    heights=[]
    speeds=[]
    '''
    ALSO, so far height and speed are not coupled.. should we correlate them?
    '''
    while(volume(rc)>0):
        
        nextWave = np.random.normal(parameters[0],parameters[1])
        nextWave = max(nextWave, 0)
        t = t + nextWave
        hits.append(t)
        print("\nNew wave hit at t=" + str(t))
        
        height =  np.random.normal(parameters[2],parameters[3])
        height = max(height, 0)
        print("with height = " + str(height))
        heights.append(height)
        
        speed =  np.random.normal(parameters[4],parameters[5])
        print("and speed = " + str(speed))
        speed = max(speed, 0)
        speeds.append(speed)
        
        rcn = waveHit([speed,height], rc)
        showCastle(rc, "rectangular")  # I suggest deleting this line if you simulate bigger shapes or lots of iterations
                                       # it's only here for visualisation purposes but rendering takes a while
        print("The volume of the sandcastle at time "+ str(t) + "= " +str(volume(rc)))
        
    plot(hits, [heights,speeds], ["Height of wave (in cm)","Speed of wave"])
    
def waveHit(wave,castle):
    
    waveSpeed = wave[0]
    waveHeight = wave[1]
    force = waveSpeed  #change this later with a force function
    hlim = min(waveHeight, len(castle))  #to ensure that waves are lower than the castle (assumption!)
    
    for h in range(0,int(hlim)):  #up to wave height for now, the collapse comes later
        layer = castle[h]
        for i in range(0,len(layer)):
            j=0
            linForce = force
            while(linForce>0 and j<len(layer[i])):
                if(layer[i][j]!=0):
                    #interaction; diminishes both cell and linforce
                    layer[i][j]=0  #simplistic now
                    linForce -= 2   #simplistic now
                j+=1
    
    '''simplistic collapse (for now)'''
    for h in range(1,len(castle)):  
        layer = castle[h]
        for i in range(0,len(layer)):
            for j in range(0,len(layer[i])):
                if(layer[i][j]==1 and castle[h-1][i][j]==0):  #tetris-like collapsing
                    verticalIter= h
                    while(verticalIter>0 and castle[verticalIter-1][i][j]==0):
                        castle[verticalIter-1][i][j]=1
                        castle[verticalIter][i][j]=0
                        verticalIter -=1
    
    return castle

def plot(hits,ys,labels):
    
    x=hits
    for i in range(0, len(ys)):
        '''more options on scatter plot'''
        y = ys[i]
        plt.scatter(x, y)
        axes = plt.gca()
        axes.set_ylim(0) 
        plt.ylabel(labels[i])
        plt.xlabel("Time (in seconds)")
        plt.show()

def main():
    
    waves(setupParameters("Calm"))
    '''
    study other shapes and include them
    
    r = createCastle(30,30,10,"rectangular")
    p = createCastle(30,30,30,"pyramid")
    c = createCastle(30,30,10,"cylinder")
    rh = createCastle(30,30,10,"rhombus")
    '''
main()
