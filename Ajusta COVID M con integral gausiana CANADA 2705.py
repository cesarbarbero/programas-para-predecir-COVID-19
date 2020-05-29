# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:57:54 2020

@author: cesar barbero
# Ajusta datos crudos de muertes por dia con Gaussiana
"""
# import librerias
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from numpy import sqrt,pi,log
from scipy.special import erf
from datetime import datetime, timedelta
from scipy import stats

# define funcion de ajuste
def func(x, a, b, c,norm):
    return norm+sqrt(pi)*a*c*erf(x/(sqrt(2)*c)-b/(sqrt(2)*c))/sqrt(2)
def rMF(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

# define y abre archivo de datos
largoexp=0
nombre_file='D:/MundoCA/argentinaJHU2705deaths.csv'
DiadeInicio="January 22, 2020"

ini_date = datetime(2020,1,22)
pob_pais=46.75 #poblacion canada
pais="Spain"

# limits parameters
inibound= [0.0,50.0,0.0,10 ]
endbound= [1000.0, 120.0, 5000.0,100000]

# seed
p0=[6,82,11,91]

# define largo de la prediccion
largosim =180 #dias
inicio=0
sigmaAlta=1.5 # error 50%!!!!!!!!!!!
sigmaBaja=0.7 # error 50%!!!!!!!!!!!
count = 0
with open(nombre_file, 'r') as f:
    for line in f:
        #print(largoexp,line)
        largoexp += 1
        
      
# Define tasa de mortalidad
tasaMmin=8/100 # Minimo nro de infectados
tasaMmax=0.5/100 # Maximo nro de infectados
tasaARG=4.15/100 #tasa de mortalidad en Argentina (12-04-2020)
lpais='Data from JHU '
        
# imprime parametros
print()
print()
print("File with total deaths per day= ",nombre_file)
print("Number of data pairs= ", largoexp)

# Dimensiona arreglos
x = np.arange(0.0, largoexp+1, 1.0)
y = np.arange(0.0, largoexp+1, 1.0)
derDatos = np.arange(0.0, largoexp+1, 1.0)
xdata=np.arange(0.0, largoexp+1, 1.0)
xsim=np.arange(0.0, largosim, 1.0)
ysim=np.arange(0.0, largosim, 1.0)
CalcCasosMin=np.arange(0.0, largosim, 1.0)
CalcCasosMax=np.arange(0.0, largosim, 1.0) 
deri=np.arange(0.0, largosim, 1.0)
ysimbajo=np.arange(largoexp+1, largosim, 1.0) 
ysimalto=np.arange(largoexp+1, largosim, 1.0)
xsimSigma= np.arange(largoexp+1, largosim, 1.0)
MdY=np.arange(0.0, largoexp+1, 1.0)
deribaja=np.arange(0.0, largosim, 1.0)
derialta=np.arange(0.0, largosim, 1.0)


# Abre archivo de datos
import csv
s=20
i=inicio
npYviejo = 0
derDatos[0]=0
with open(nombre_file) as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=';')
     line_count = 0

# lee datos
     
     for row in csv_reader:
         i=i+1        
         npX=float(row[0])
         npY=float(row[1])
         MdY[i]=npY
         x[i]=npX
         y[i]=npY
         derDatos[i]=y[i]-y[i-1]
         #print(x[i],y[i],derDatos[i])
         xsim[i]=npX 
         npYviejo=npY

# carga datos para fiting
MA=1
xdata=x
ydata=rMF(y,MA)

#Constrain the optimization to the region

popt, pcov = curve_fit(func, xdata, ydata, bounds=(inibound, endbound))
perr = sqrt(np.diag(pcov))

a= popt[0]
b= popt[1]
c= popt[2]
norm= popt[3]
print ("Fit parameters")
print('Amplitude (a)=',a)
print('Day of maximum (b)=',int(b))
print('Width (c)=',c)
print('Normalization constant (norm)=',norm) 
print("perr=",perr)

# llena el arreglo con datos simulados
i=inicio
LSQ=0
deriSim=derDatos*1.0

while i<largosim:   
    xsim[i]=i
    ysim[i]=func(i,a,b,c,norm)
    deri[i]= ysim[i]-ysim[i-1]
    if i<largoexp+1:
        LSQ=LSQ+(ysim[i]-ydata[i])**2
        deriSim[i]=deri[i]
        
    i=i+1
deriSim[0]=0
TotalM=int(max(ysim))
LSQ=sqrt(LSQ)
print("LSQ=",LSQ)
LSQnorm=LSQ/TotalM
print("LSQnormnalized % =",int(LSQnorm*100))

# repasa datos y calcula datos relevantes
j=inicio

maxX=0
maxY=0
dia95=0
finX=0
while j<largosim:
    CalcCasosMin[j]=ysim[j]/tasaMmin
    CalcCasosMax[j]=ysim[j]/tasaMmax
    
  
    if deri[j]>deri[j-1]:
        maxY=int(deri[j])
        maxX=int(xsim[j])
    if ysim[j]<0.9978*TotalM:
       finX=xsim[j]
       #print(j,int(deri[j]))
    if ysim[j]<0.9545*TotalM:
       dia95=xsim[j]
    if ysim[j]<0.6827*TotalM:
       diaSigma=xsim[j]
    if ysim[j]<TotalM:
       zeroD=xsim[j]  
       
    j=j+1 
 
deribaja=deri*sigmaBaja
derialta=deri*sigmaAlta

# Grafica datos y ajuste
plt.style.use('default')

plt.legend(loc='upper left')

plt.plot(xdata, ydata, 'r', label=lpais,marker='o',
         fillstyle="none",markersize=15)
plt.plot(xsim, ysim, 'b-',label="Forecast")
plt.errorbar(xsim, ysim*1.05,linestyle='none', xerr=0, yerr=ysim*0.05)

plt.plot(xdata, func(xdata, *popt), 'g', 
         label='Fit', marker='o', fillstyle='none',markersize=5)
#plt.plot(xsimSigma, ysimbajo, 'b:',label="Bcs (-30%)")
#plt.plot(xsimSigma, ysimalto, 'b:',label="Wcs (+50%)")
titulo="COVID-19 deaths "+pais
plt.suptitle(titulo)
LejeX="Days from "+DiadeInicio  
plt.xlabel(LejeX)
plt.ylabel('Cummulative deaths')
plt.legend()

plt.show()

MaxCalcCasosMax=int(max(CalcCasosMax))
MaxCalcCasosMin=int(max(CalcCasosMin))

# Grafica casos calculados
SI=1
NO=0
grafica=SI
if grafica==NO:
    lmax ='Maximum=' + str(MaxCalcCasosMax)
    lmin = 'Minimum= '+ str(MaxCalcCasosMin)
    plt.plot(xsim,CalcCasosMax, 'r-', label= lmax)
    plt.plot(xsim,CalcCasosMin, 'b-', label = lmin)
   
    plt.xlabel(LejeX)
    plt.ylabel('Infected')
    plt.legend()
    plt.show()
else:
    pass
    
#grafica casos por dia
MA=3
derDatosS=rMF(derDatos,MA)

lgaus="Predicted gaussian "
lalta="upper limit (+50 %)"
lbaja="lower limit  (-30 %)"
plt.bar(x,derDatosS,color='r', label="Data JHU ")

plt.suptitle(titulo)
deri[0]=0
derialta[0]=0
deribaja[0]=0
plt.plot(xsim,deri,'b-', label=lgaus)

plt.plot(xsim,derialta,'b:',label=lalta)
#plt.plot(xsim,deribaja,'g:',label=lbaja)
plt.xlabel(LejeX)
plt.ylabel('Deaths per day')
plt.legend()
plt.show()

#grafica integral de gausiana contra muertes
sim_data=func(xdata, *popt)

plt.suptitle(titulo)
slope, intercept, r_value, p_value, std_err = stats.linregress(sim_data,ydata)
R2=int(r_value*1000)/1000
plt.plot(func(xdata, *popt),ydata, 'r', marker='o', 
         linestyle='none',fillstyle="none", markersize=10)
plt.plot(ydata,ydata,"b-", label="R**2="+str(R2))
plt.xlabel("Calculated cummulative deaths")
plt.ylabel('Recorded Cummulative deaths')
plt.legend()
plt.show()
slope, intercept, r_value, p_value, std_err = stats.linregress(deriSim,derDatosS)

# grafica gausiana contra muertes por dia

plt.suptitle(titulo)
plt.plot(deriSim,derDatosS, 'r', marker='o', 
         linestyle='none',fillstyle="none", markersize=10)
R2=int(r_value*1000)/1000
plt.plot(deriSim,deriSim,"b-", label="R**2="+str(R2))
plt.xlabel('Recorded deaths per day')
plt.ylabel('Calculated deaths per day')

plt.legend()

# ancho
FWHM = 2*sqrt(2)*sqrt(2*log(2))*c
print("FWHM=", int(FWHM), " days")

# Imprime parametros
print()
TotalM=int(max(ysim))
diferHigh=int(TotalM*sigmaAlta)
diferLow=int(TotalM*sigmaBaja)
print("Total of deaths =",TotalM,"(",diferHigh,"-",diferLow,")")
print("Total deaths per million=", int(TotalM/pob_pais))
print()

maxX2=int(b)# analytical day of the maximum
maxY2=int(a) # analytical number of deaths/day maximum

new_date = ini_date + timedelta(maxX2)
print("Maximum of death/day=",int(maxY2),"the day=", new_date,maxX2)
print()
new_date = ini_date + timedelta(zeroD)
print("100% deaths the day =",new_date,"a los:",zeroD)
new_date = ini_date + timedelta(finX)
print("3 sigma deaths (99.78%) the day =",new_date,"a los:",finX)
new_date = ini_date + timedelta(dia95)
print("2 sigma (95.45%) of deaths the day",new_date)
new_date = ini_date + timedelta(diaSigma)
print("1 sigma (68.27%) of deaths the day",new_date)

print("")
ancho=zeroD-maxX
iniM=maxX-ancho
new_date = ini_date+timedelta(iniM)
print("Start of mortality=",new_date,iniM)
print()
print("Total of infected")
print('High value=' ,MaxCalcCasosMax,"infected")
print('Low value=',MaxCalcCasosMin, "infected")





