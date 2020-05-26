'''
Created on 7 Feb 2019

@author: Petros Laptop
'''
import random
import math
import numpy as np

    
class Sample(object):
    
    def __init__(self, n, l, t):  # constructor

        self.nucleiGrid = np.ones((n, n))  # a 2D array of ones
        self.decayConstant = l 
        self.timestep = t
        
    def countUndecayed(self):
        
        n = len(self.nucleiGrid)
        undecayed = 0  # a counter for undecayed nuclei in the sample
        
        for i in range(0, n):  
            for j in range(0, n):
                   
                nucleus = self.nucleiGrid[i][j]
                
                if (int(nucleus) == 1):     #if nucleus is undecayed (ie a 1)
                    undecayed += 1          #increment the counter
                    
        return undecayed
                    
    def decay(self):
        
        n = len(self.nucleiGrid)
        initialNuclei = n * n  # initial number of nuclei is length times width
        l = self.decayConstant 
        t = self.timestep
        p = l * t  # the probability of decay
        loops = 0  # a counter of loops
        
        while(self.countUndecayed() > initialNuclei / 2):  # to find half life
            
            loops += 1  # increment counter
            for i in range(0, n):   #loop inside the grid
                for j in range(0, n):
                    
                    r = random.random()  # generate a random number
                    if (r < p):  # if the random number is less than the calculated probability
                        self.nucleiGrid[i][j] = 0  # decay the nucleus
        
        simulatedHalfLife = loops * t  # calculate the simulated half life 
        return(simulatedHalfLife)       
        
    def calculateHalfLife(self):
        
        l = self.decayConstant
        halfLife = math.log(2) / l  # formula for half life 
        print("The actual value of the half life is: " + str(halfLife) + " minutes")
        return(halfLife)
        
    def printSample(self):
        
        n = len(self.nucleiGrid)  # length of initial grid
        
        for i in range(0, n):
            print()  # print new line
            for j in range(0, n):
                
                nucleus = self.nucleiGrid[i][j]
                print(int(nucleus), end='')
                print(" ", end='')
                    
        print('\n')
        print("Initial number of undecayed nuclei: " + str(n * n))
        print("Final number of undecayed nuclei: " + str(self.countUndecayed())) 

        
def main():
    
    # prompt for required values
    l = float(input("Type in the value of the decay constant: "))
    n = int(input("Type in the length of the 2D array: "))
    t = float(input("Type in the timestep: "))
    
    mySample = Sample(n , l , t)
    simulatedHalfLife = mySample.decay() 
    mySample.printSample()
    print("The simulated value of the half life is: " + str(simulatedHalfLife) + " minutes")
    calcHalfLife = mySample.calculateHalfLife()
    unc = ( abs(calcHalfLife - simulatedHalfLife)/ calcHalfLife) *100
    print("The % uncertainty is: " + str(unc) )

    
main()
