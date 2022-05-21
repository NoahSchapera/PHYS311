# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 23:53:41 2022

@author: Noah Schapera
"""

#import relevant libraries
import numpy as np
import csv
import os

parameters=[[ 0.10, 2900, 0.16 ],
            [ 0.50, 3800, 0.6 ],
            [ 0.75, 5000, 0.8 ],
            [ 1.0, 6000, 1.0 ],
            [ 1.5, 7000, 1.4 ],
            [ 3, 11000, 2.5 ],
            [ 5, 17000, 3.8 ],
            [ 10, 22000, 5.6 ],
            [ 15, 28000, 6.8 ],
            [ 25, 35000, 8.7 ],
            [ 60, 44500, 15 ]]

def deltaMag(time,bols):
    idsp1=np.where(time<0.2)
    idsp2=np.where(time>0.8)
    
    idss_inter=(time>0.4)*(time<0.6)
    idss=np.where(idss_inter)
    
    idsb1_inter=(time>0.2)*(time<0.4)
    idsb2_inter=(time>0.6)*(time<0.8)
    
    idsb1=np.where(idsb1_inter)
    idsb2=np.where(idsb2_inter)
    
    primary1=np.max(bols[idsp1])
    primary2=np.max(bols[idsp2])
    
    primary = (primary1+primary2)/2
    
    base1=np.mean(bols[idsb1])
    base2=np.mean(bols[idsb2])
    
    base = (base1+base2)/2
    
    secondary=np.max(bols[idss])
    
    

    
    dPrime=primary-base
    dSec=secondary-base
    
    if dSec > dPrime:
        temp = dPrime
        dPrime = dSec
        dSec = temp
    
    return dPrime,dSec


#Create arrays of mass iterables and eccentricity iterables. Used for file name and data labels
masses = np.array(['0.100000','0.500000','0.750000','1.000000','1.500000','3.000000','5.000000','10.000000','15.000000','25.000000', '60.000000'])
e='0.000000'

#model bolometric mag prototype
bols = np.zeros(1002)

#data bolometric mag prototype            
starBols=np.zeros(1002)

#least squared fit for model-data, with extra columns for labels
sqs=np.zeros(shape=(66,3))



#used to assign least squared value to correct index in sqs 
counter=0

data_dPrim=0.65
data_dSec=0.15

flag=False
calcCounter=0

c=0

        
for inCount in range(len(masses)):
    outCount = inCount
    while outCount < len(masses):
        c+=1
        m1 = masses[inCount]
        m2 = masses[outCount]
        
        #generate uniue file name using the masses and eccentricities 
        fileName='Orbit-'+m1+'-'+m2+'-'+e+'.txt'
        

        #iterate through all combinations of masses
        leastSquared=0
        
        
        #calculte file size. Files that did not generate due to being contact binaries will be small (<100k bytes)
        #if so, disregard file. Assume very large least squared. 
        stats = os.stat(fileName)

        #otherwise, read all data in file into a list using the csv library
        if stats.st_size > 100000:
            with open(fileName, newline = '') as data:                                                                                          
                fileReader = csv.reader(data, delimiter='\t')
                csvArray=np.array(list(fileReader))
                
                csvArray=csvArray[1:,:].astype(float)

            bols=csvArray[1:,3]
            time=csvArray[1:,0]

            dPrim,dSec=deltaMag(time,bols)
            
            
            #calculate least squared for the model and the actual data
            leastSquared=(dPrim-data_dPrim)**2+(dSec-data_dSec)**2
                
        else:
            leastSquared=9999999999999999999
          
        #assign least squared and model label information to appropriate location in a single row of sqs
        sqs[counter,0]=leastSquared
        sqs[counter,1]=m1
        sqs[counter,2]=m2
        counter+=1
        outCount+=1

#find minimum value of all least squared calculated
minSqs=np.min(sqs[:,0])
#find location where mininum value exists in sqs array
bestFitParams=sqs[sqs[:,0]==minSqs][0]

#print out model lables for best fit location in sqs array

MA=bestFitParams[1]
MB=bestFitParams[2]

for p in parameters:
    if p[0]==MA:
        TA=p[1]
        RA=p[2]
        
for p in parameters:
    if p[0]==MB:
        TB=p[1]
        RB=p[2]
                
        
print("Best Fit Params")
print(' ')
print('Least Squared: ' + str(bestFitParams[0]))
print(' ')
print('Mass A: ' + str(MA))
print('Temp A: ' + str(TA))
print('Rad A: ' + str(RA))
print(' ')
print('Mass B: ' + str(MB))
print('Temp B: ' + str(TB))
print('Rad B: ' + str(RB))
#print(c)


