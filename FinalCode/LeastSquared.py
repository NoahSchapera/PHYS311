# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 23:53:41 2022

@author: Noah Schapera
"""

#import relevant libraries
import numpy as np
import numpy.random as rand
import csv
import os

#Create arrays of mass iterables and eccentricity iterables. Used for file name and data labels
masses = np.array(['0.100000','0.500000','0.750000','1.000000','1.500000','3.000000','5.000000','10.000000','15.000000','25.000000', '15.000000', '25.000000', '60.000000'])
eccs = np.array(['0.000000','0.200000','0.400000','0.600000','0.800000'])

#model bolometric mag prototype
bols = np.zeros(1002)

#data bolometric mag prototype            
starBols=np.zeros(1002)

#least squared fit for model-data, with extra columns for labels
sqs=np.zeros(shape=(605,4))



#used to assign least squared value to correct index in sqs 
counter=0



#---------------------------------------------------------------
#Generate Test File Data, please remove when testing actual data
fileName1='Orbit-'+masses[3]+'-'+masses[2]+'-'+eccs[2]+'.txt'
stats = os.stat(fileName1)
if stats.st_size > 100000:
    with open(fileName1, newline = '') as data:                                                                                          
        fileReader = csv.reader(data, delimiter='\t')
        csvArray=np.array(list(fileReader))

    starBols=csvArray[1:1002,3]
    for i in range(starBols.size):
        starBols[i]=float(starBols[i])+2*(rand.rand()-0.5)
    
#---------------------------------------------------------------

#---------------------------------------------------
#when using actual data, please input starBols as an np.array with size = 1002, representing evenly spaced bolometric
#magnitude measurements at equal timesteps across a full period

#starBols = np.array(SomeListHere)
#---------------------------------------------------

for m1 in masses:
    for m2 in masses:
        for e in eccs:
#iterate through all combinations of masses and eccentricities
            
            #each model generates 605 best fit models, if we reach the end of the model datasets, break the loops
            if counter == 605:
                break
            
            leastSquared=0
            
            #generate uniue file name using the masses and eccentricities 
            fileName='Orbit-'+m1+'-'+m2+'-'+e+'.txt'
            
            #calculte file size. Files that did not generate due to being contact binaries will be small (<100k bytes)
            #if so, disregard file. Assume very large least squared. 
            stats = os.stat(fileName)
            
            #otherwise, read all data in file into a list using the csv library
            if stats.st_size > 100000:
                with open(fileName, newline = '') as data:                                                                                          
                    fileReader = csv.reader(data, delimiter='\t')

                    csvArray=np.array(list(fileReader))
                #the bolometric magnitude is in column 3 of our raw data, and exists in all rows except the first
                bols=csvArray[1:1002,3]
                
                #calculate least squared for the model and the actual data
                for i in range(bols.size):
                    leastSquared+=(float(starBols[i])-float(bols[i]))**2
                    
            else:
                leastSquared=9999999999999999999
              
            #assign least squared and model label information to appropriate location in a single row of sqs
            sqs[counter,0]=leastSquared
            sqs[counter,1]=m1
            sqs[counter,2]=m2
            sqs[counter,3]=e
            counter+=1

#find minimum value of all least squared calculated
minSqs=np.min(sqs[:,0])
#find location where mininum value exists in sqs array
bestFitParams=sqs[sqs[:,0]==minSqs][0]

#print out model lables for best fit location in sqs array
print("Best Fit Params")
print('Least Squared: ' + str(bestFitParams[0]))
print('Mass A: ' + str(bestFitParams[1]))
print('Mass B: ' + str(bestFitParams[2]))
print('System Eccentricity: ' + str(bestFitParams[3]))




