'''
Created on 31 May 2020   (different from GitHub version)

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
import statistics

visualise = False  # To indicate if we want to visualize each castle after its creation. 
# A bit time consuming due to large 3D shapes; good for checking if shapes are created in the right way

'''
This method initializes the base of each castle based on the specified shape, 
and later builds the castle layer by layer accordingly.
'''
def createCastle(w,l,height,shape): 
    
    print()
    print(shape)
    
    if(shape=="rectangular" or shape =="pyramid"):
        base = np.ones((w,l))
    if(shape=="rhombus"):
        base = np.zeros((w,l))
        midL= int( (len(base)-1) /2)
        midR = np.ceil( (len(base)-1) /2)
        for i in range(0,int(np.ceil(len(base)/2))):
            for j in range(0,len(base[i])):
                if(j>= (midL - i) and j <= (midR + i) ):
                    base[i][j]=1
                    base[len(base)-i-1][j]=1
                    
    if(shape=="cylinder"):
        base = np.zeros((w+1,w+1))
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
                    
    if(shape=="ellipsoid"):
    
        base = np.zeros((w,l))
        a = l/2
        b = w/2
        c = math.sqrt(a**2 - b**2)
        thetas = np.linspace(0, 2*math.pi)
        minR = (b**2) /(a - (c *math.cos(math.pi)))
        for theta in thetas:
            radius = (b**2) /(a - (c *math.cos(theta)))
            x= (radius * (math.cos(theta))) + minR
            y= (radius * (math.sin(theta))) + b
            xlow = min(a,x) 
            xhi = max(a,x)
            ylow = min(b,y)
            yhi = max(b,y)
            i=round(ylow)
            while(i<=yhi):
                for j in range(round(xlow),round(xhi)):
                    base[i][j]=1
                i+=1 
                
    castle = [np.copy(base)]
    for h in range(1,height):
        layer = shapeCastle(base,h,shape)
        castle.append(np.copy(layer))
    if(visualise):
        showCastle(castle,shape) 
    return castle

'''
This method is used by the createCastle() to shape each layer 
according to the specified shape of each castle.
'''
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

'''
This method is purely for visualization of the castles. It does not really
participate in the simulation, but it useful for checking if the shapes are
built correctly and if the collapsing is acting as intended. 
'''
def showCastle(castle,shape):
    
    fig = plt.figure()
    ax=fig.gca(projection='3d')
    
    stacks=1  # used to create thickness between layers
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
                    
    lim = max(len(castle[0]), len(castle[0][0]))              
    ax.set_xlim3d(0,lim*1.5)
    ax.set_ylim3d(0,lim*1.5)
    ax.set_zlim3d(0,height*1.5)
    axes = plt.gca()
    plt.title("Shape of Sandcastle: "+ shape)
    ax.set_xlabel("Width")
    ax.set_ylabel("Length")
    ax.set_zlabel("Height")
    plt.show()

'''
This method loops through the castle to measure its (remaining) volume.
'''    
def volume(castle):
    
    volume = 0
    for layer in castle:
        for i in range(len(layer)):
            for j in range(len(layer[i])): 
                volume += layer[i][j]
    return volume  

'''
This method is used to setup the parameters of waves we obtained through research.
''' 
def setupParameters(condition):
    
    if(condition=="Calm"): 
        i=0 
    if(condition=="Regular"):
        i=1 
    if(condition=="Windy"):
        i=2 

    freqMeans = [8]
    freqStdevs = [3]
    heightMeans = [10]
    heightqStdevs = [3]
    speedMeans = [4]
    speedStdevs = [1]
    
    return [freqMeans[i], freqStdevs[i], heightMeans[i], heightqStdevs[i], speedMeans[i], speedStdevs[i]   ]

'''
This method is where the waves are created using the parameters specified above.
After each wave is created, it hits the castle using the waveHit() method, and saves 
the remaining volume. The ratio of the remaining volume to the initial volume is also 
calculated and monitored.
'''     
def waves(parameters, castle):
    
    volumes = [volume(castle)]
    initialVol = volume(castle)
    ratio = volume(castle)/initialVol
    ratios = [ratio]
    t=0
    hits=[]
    heights=[]
    speeds=[]
    '''
    ALSO, so far height and speed are not coupled.. should we correlate them?
    '''
    while(ratio>0.01): #watch out for infinite loops on long shapes!! (waves never reach them)
        
        nextWave = 10  # we removed stochasticity on the frequency of waves
        t = t + nextWave
        hits.append(t)
        
        height =  np.random.normal(parameters[2],parameters[3])
        height = max(height, 0)
        heights.append(height)
        
        speed =  np.random.normal(parameters[4],parameters[5])  #include linear increase for tide phenomena
        speed = max(speed, 0)
        speeds.append(speed)
        
        waveHit([speed,height], castle)
        volumes.append(volume(castle))
        ratio = volume(castle)/initialVol
        ratios.append(ratio)
        
        if(len(ratios)>100 and ratio == ratios[len(ratios)-100]): #prevents infinite loops (explain more once finalised)
            print("Unchanging volume (Waves cannot reach the remaining sandcastle)")
            break
        #showCastle(castle, "falling castle")
        
    #plotWaves(hits, [heights,speeds], ["Height of wave (in cm)","Speed of wave(in ?)"])
    hits.insert(0, 0)
    finalRatio = ratios[len(ratios)-1]
    print("The ratio of the volume of the remaining sandcastle\nto the initial volume is " + str(finalRatio))  #IMPROVE printing later
    return hits,volumes

'''
This method simulates how each wave hits the castle. First, it loops through the castle,
and according to the force function (TBD) it attacks the sand-blocks. After the wave is 
done 'hitting' the sandcastle, the method loops again through the castle and simulates its
collapse.
'''     
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
                else:
                    linForce -= 0.2 # diminishes in y
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

'''
A simple plotting of the speeds & heights of waves that were used in each run of the simulation.
''' 
def plotWaves(hits,ys,labels):
    
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

'''
Plotting of the volume over time of each castle throughout the simulation (needs fixing)
''' 
def plotVolumes(times,volumes,title):
       
    for i in range(0, len(volumes)): #wrong for now.. only plots the last one. Prob because different xs
        x = times[i]
        y = volumes[i]
        plt.plot(x,y)
    
    plt.title(title)   
    axes = plt.gca()
    axes.set_ylim(0)
    plt.xlabel("Time (in seconds)")
    plt.show()

'''
The Simulation() method takes a sandcastle as an argument and allows it to be 
destroyed by waves N times (specified in the for loop), while tracking the 
volume decrease of the castle overtime. It then obtains the final time of each 
run (the time it took for each castle to be destroyed) and calculates their median
value. (can include more/various statistics)
'''            
def Simulation(castle):
    
    print("Initial volume: " + str(volume(castle)))
    times=[]
    volumes=[]
    for i in range(0,1):
        trial = np.copy(castle)
        time, vol = waves(setupParameters("Calm"), trial)
        times.append(time)
        volumes.append(vol)
        
    finaltimes=[]   
    for sim in times:
        finaltime = sim[len(sim)-1]
        finaltimes.append(finaltime)
        
    q2 = statistics.median(finaltimes)
    
    print("Median time for relative destruction: " + str(q2))  

'''
This is the main() function, which initializes the desired castles with the given
parameters (length, width, height, shape) and then allows each castle to be hit by waves,
through the Simulation() method.
'''     
def main():
    
    '''
    we could study more shapes and include them
    NEXT, investigate how these parameters affect lifetime of castle
    '''
    theVol = 20000  # intended to ensure that all shapes of castle have similar initial volumes
    dim = int(theVol**(1/3))
    print(dim)
    
    r = createCastle(dim,dim,dim,"rectangular")
    Simulation(r)
    
    c = createCastle(dim,dim,int(dim*1.4),"cylinder")  # only uses w as the diameter
    Simulation(c)
    
    rh = createCastle(int(dim*1.45),int(dim*1.45),dim,"rhombus")  # actually square rhombus
    Simulation(rh)
    
    p = createCastle(int(dim*1.8),int(dim*1.8),dim,"pyramid")
    Simulation(p)
    
    el = createCastle(int(dim*0.8),int(dim*1.8),dim,"ellipsoid")  # most "aerodynamic" -> best
    Simulation(el)
    
main()