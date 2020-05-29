# -*- coding: utf-8 -*-
"""
Created on Sat May 23 09:57:40 2020

@author: Cesar Barbero
"""

#lee automaticamente data de paises


# import librerias
import csv
from numpy import arange,zeros

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from numpy import sqrt,pi,log,exp
from scipy.special import erf
from datetime import datetime, timedelta
from scipy import stats
from math import trunc

ndatos=131
xdatos=arange(1,ndatos+1,1)
ydatos=zeros (ndatos)
world=zeros (ndatos)
derY=zeros (ndatos)
line=[]
UmbralF=30
UmbralG=30
# define funciones
def Gauss(x, a, b, c):
    return a*exp(-(x-b)**2/(2*c**2)) # gaussiana
def igauss(x, a, b, c,norm):
    return norm+sqrt(pi)*a*c*erf(x/(sqrt(2)*c)-b/(sqrt(2)*c))/sqrt(2)
def rMF(y, N):
    return np.convolve(y, np.ones((N,))/N)[(N-1):]
def derivada(x,y,ndatos):
    for z in range(1,ndatos):
        
        derY[z]=(y[z]-y[z-1])
        print(z,derY[z])
        return derY

def ajusta(x,y,ndatos,pais):
    titulo= "Country province/state="+ pais
    Nsim=200
    totalM=0
    a=pdd=c=norm=fwhm=sigma3=inicio= R2= Pco= R2p= 0
    if y[ndatos-1]>UmbralF:
        popt, pcov = curve_fit(igauss, xdatos, ydatos, bounds=(inibound, endbound))
        #perr = sqrt(np.diag(pcov))
        a = int(popt[0]*100)/100
        pdd = int(popt[1])
        pddDate=ini_date + timedelta(pdd)
        dia=pddDate.date()
        c=popt[2]
        fwhm = int(2*sqrt(2)*sqrt(2*log(2))*c)
        norm= int(popt[3])
        xsim=arange(1,Nsim,1)
        ysim=igauss(xsim, a, pdd, c, norm)
        totalM=int(max(ysim))
        ysimS=igauss(x, a, pdd, c, norm)
        slope, intercept, r_value, p_value, std_err = stats.linregress(ysimS,y)
        R2=trunc(r_value*1000)/1000.0
        print("R2=",R2)
        # calcula fin e inicio
        sigma3=int(((fwhm/2)*3)+pdd)
        #Date=ini_date + timedelta(sigma3)
        #sigma3=str(Date.date())
        inicio=int(pdd-((fwhm/2)*3))
        #Date=ini_date + timedelta(inicio)
        #inicio=str(Date.date())
        #calcula % de completado
        complepor=95*y[ndatos-1]/totalM
        #complepor= 68.24*(ndatos-pdd)/((fwhm/2)-pdd)
        Pco=int(complepor)
        print("Percentage of completitud=",Pco)
        lR2="R**2 ="+str(R2)
        ltexto="% of end="+str(int(Pco))
        #print(y[ndatos-1])
        
        # grafica cummulative deaths muertos > 1% del total
        if y[ndatos-1]>UmbralG:
                        
            LejeX="Days from 22nd of january, 2020"  
            plt.xlabel(LejeX)
            plt.ylabel('Cummulative deaths')
            plt.suptitle(titulo)
            letTM="Total deaths= "+ str(totalM)
            plt.plot(xsim,ysim,label=letTM)
            ymax=max(y)
            
            plt.text(x[1]+5,ymax/2,ltexto)
            plt.plot(x,y,"bo",label=lR2)
            plt.legend()
            nombre_archivo_png="D:/MundoCA/Igausiana/"+pais+"cd.png"
            plt.savefig(nombre_archivo_png)
            plt.show()
            
            
            #calcula derivadas
            for z in range(1,ndatos):
                derY[z]=(y[z]-y[z-1])
            derYs=rMF(derY,3)
            derSim=Gauss(xsim,a,pdd,c)
            
            #grafica derivadas
            plt.xlabel(LejeX)
            plt.ylabel('deaths per day')
            plt.suptitle(titulo)
            lpeakday="Peak="+str(dia)
            lfwhm="fwhm ="+str(fwhm)
            plt.bar(x,derYs,color="r",label=lfwhm)
            plt.plot(xsim,derSim,"b-",label=lpeakday)
            plt.legend()
            nombre_archivo_png="D:/MundoCA/gausiana/"+pais+"pdd.png"
            plt.savefig(nombre_archivo_png)
            plt.show()
              
    else:
        print("Too few number of deaths to fit")
        a = pdd = c = norm = R2= 0
    plt.show()
   
    return totalM,pdd,fwhm,sigma3,inicio,R2,a,c,norm,Pco
pars=[""]

def abreescribe(numpaises):
    # abre archivo para grabar como csv
    with open("D:/MundoCA/worldJHU2805parms.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        
        writer.writerow(line[0])
        for j in range(1,numpaises):
            
            test=line[j][3]
            if test>0:
                writer.writerow(line[j])
    
# define y abre archivo de datos
largoexp=0
nombre_file="D:/MundoCA/worldJHU2805deaths.csv"
DiadeInicio="January 22, 2020"

ini_date = datetime(2020,1,22)

# limits parameters
inibound= [0.0,50.0,0.0,10 ]
endbound= [5000.0, 120.0, 10000.0,50000]

# seed
p0=[100,82,20,500]
linea=[]
j=0
# Abre archivo de datos


print ("")
print("Country province/colony/state")
with open(nombre_file) as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=';')
     line_count = 0

# lee datos, ajusta y graba
     h=0
     
     for row in csv_reader:
         #print(row[1])  
         pais=row[1]
         provincia=row[0]
         pais=pais+" "+provincia
         if row[1]!="":
             for i in range (5,ndatos):
                 ydatos[i]=int(row[i])*1
             print()
             
             print(pais)
           
             totalM,pdd,fwhm,sigma3,inicio,R2,a,c,norm,Pco=ajusta(xdatos,ydatos,
                                                              ndatos,pais)
             
             line.append([pais,totalM,pdd,fwhm,sigma3,inicio,R2/1.0,a,c,norm,Pco])
             j=j+1
             
             #print(totalM,pdd,fwhm,sigma3,inicio)
             #print("a,b,c,norm=",a,pdd,c,norm)
             letTM="Total deaths= "+ str(totalM)
             if pdd>0:
                 print('Day of the peak=',pdd,'FWHM=',fwhm,letTM,)
                 print("End (99.78%)= ",sigma3,"Begin= ",inicio)
         else:
             pass
         print()
pars=["Country Province/state","Total deaths","Peak Day","FWHM "," End 3s",
      "Begin","R**2","a","c","norm","% end"]
line.append(pars)
line[0]=(pars)
numpaises=j
abreescribe(numpaises)
        
print("THE END")





   



     