'''
Created on 26 May 2020

@author: Petros Laptop
'''
import random
import math
import numpy as np
import matplotlib.pyplot as plt

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
    
    t=0
    hits=[]
    heights=[]
    speeds=[]
    '''
    use while loop instead of for
    '''
    for hit in range(0,10):
        
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
    
    plot(hits, [heights,speeds], ["Height of wave (in cm)","Speed of wave"])
    
def waveHit():
    
    '''fill this in later'''
    
    pass

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
      
main()
