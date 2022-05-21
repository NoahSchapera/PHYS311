# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 21:05:46 2022

@author: Noah Schapera
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

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
    
    return dPrime,dSec
    

fig, ax = plt.subplots()
fig.set_size_inches(7,5)
ax.set_xlabel('Time (fractions of a period)')
ax.set_ylabel('Magnitude')
ax.set_title('Predicted Light Curve of SV Cam')

t=np.arange(0,1,0.000999)
fileName='Orbit-'+'0.500000'+'-'+'1.000000'+'-'+'0.000000'+'.txt'
print(fileName)

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
    
    ax.plot(time,bols)
    print('Predicted primary eclipse depth: ' + str(dPrim))  
    print('Predicted secondary ecplipse depth: ' + str(dSec))

        

plt.show()