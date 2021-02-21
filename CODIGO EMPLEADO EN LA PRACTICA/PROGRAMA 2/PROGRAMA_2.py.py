#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import math as m
import numpy as np


##Funciones del cálculo de los diferentes datos necesarios.
##Se incluye interfaz de usuario para hacerlo todo más ameno.

##Para ejecutar el programa solo es necesario ejecutar la funcion menuSeleccion()

def comprobarOpcion():
    while (True):
        val = input("Seleccione una opción: ")
        if val not in ["1","2","3","4"]:
            print("Seleccione una opcion válida")
        else:
            return val
        
def menuSeleccion():
    SNE=pd.read_csv("SNE_Historical_Data.csv",index_col=None)
    GME=pd.read_csv("GME_Historical_Data.csv",index_col=None)
    SNE_E=pd.read_csv("SNE_Historical_Data_extendido.csv",index_col=None)
    GME_E=pd.read_csv("GME_Historical_Data_extendido.csv",index_col=None)
    
    print("----------- INTERFAZ ESTADISTICA PRACTICA 1 -----------")
    print("Seleccione la operación a realizar: ")
    print("1. Matriz de gráficas de las 6 variables pedidas (Sony y Gamestop).")
    print("2. Graficar de forma individual todas las variables.")
    print("3. Calculo de covarianzas y Pearson.")
    print("4. Cerrar la interfaz.")
    print("\n")
    
    val = comprobarOpcion()
    
    if (int(val) == 1):
        Matriz_Graficas(SNE,GME,SNE_E,GME_E)
        menuSeleccion()
    
    elif (int(val) == 2):
        REND = Rend_Diario(SNE,GME);
        CINC = Roll_Avg_50_Dias(SNE,GME,SNE_E,GME_E);
        DOSC = Roll_Avg_200_Dias(SNE,GME,SNE_E,GME_E);
        Plot_Rend_Diario(REND[0],REND[1])
        Plot_Roll_Avg_50_Dias(CINC[0],CINC[1])
        Plot_Roll_Avg_200_Dias(DOSC[0],DOSC[1])
        menuSeleccion()
    
    elif (int(val) == 3):
        print("\n")
        print("Datos rendimiento diario\n")
        ConvarianzaRendDiario(GME,SNE)
        print("\n")
        print("Datos media movil 50 dias\n")
        Covarianza50Dias(GME,SNE,GME_E,SNE_E)
        print("\n")
        print("Datos media movil 200 dias\n")
        Covarianza200Dias(GME,SNE,GME_E,SNE_E)
        print("\n")
        menuSeleccion()
        
    elif (int(val) == 4):
        print("Saliendo...")
        return

def Rend_Diario(SNE,GME):
    RND_SNE=([],[])
    RND_GME=([],[])
    for i in range(len(SNE)):
        RND_SNE[0].append((SNE["Date"][len(SNE)-1-i]))  
        RND_SNE[1].append(float(SNE["Change %"][len(SNE)-1-i][:-1]))

    for i in range(len(SNE)):
        RND_GME[0].append((GME["Date"][len(SNE)-1-i])) 
        RND_GME[1].append(float(GME["Change %"][len(SNE)-1-i][:-1]))
    
    return [RND_GME,RND_SNE]

def Plot_Rend_Diario(RND_SNE,RND_GME):
    plt.plot(RND_SNE[0],RND_SNE[1],scalex=True)
    plt.ylabel("Rendimiento diario (%)")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Rendimiento Diario: Sony")
    plt.xticks([])
    plt.show()
    
    plt.plot(RND_GME[0],RND_GME[1])
    plt.ylabel("Rendimiento diario (%)")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Rendimiento Diario: Gamestop Enterprises")
    plt.xticks([])
    plt.show()

def Roll_Avg_50_Dias(SNE,GME,SNE_E,GME_E):
    aux_price=[]
    aux_dates=[]
    aux_panda=pd.DataFrame()
    RND_SNE=([],[])
    RND_GME=([],[])
    for i in range(len(SNE_E)):
        aux_dates.append(SNE_E["Date"][i])
        aux_price.append(SNE_E["Price"][i])

    aux_price.reverse()
    aux_dates.reverse()
    aux_panda["Date"]=aux_dates
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=50).mean()

    for i in range(len(SNE)):
        RND_SNE[0].append((SNE["Date"][len(SNE)-1-i]))  
        RND_SNE[1].append(aux_panda["MA"][246+i]) 

    aux_price=[]
    aux_dates=[]
    aux_panda=pd.DataFrame()    
    for i in range(len(GME_E)):
        aux_price.append(GME_E["Price"][i])
        aux_dates.append(GME_E["Date"][i])

    aux_price.reverse()
    aux_dates.reverse()
    aux_panda["Date"]=aux_dates
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=50).mean()


    for i in range(len(SNE)):
        RND_GME[0].append((GME["Date"][len(SNE)-1-i]))  
        RND_GME[1].append(aux_panda["MA"][246+i]) 
    
    return [RND_GME,RND_SNE]

def Plot_Roll_Avg_50_Dias(RND_SNE,RND_GME):
    plt.plot(RND_SNE[0],RND_SNE[1],scalex=True)
    plt.ylabel("Media Movil de 50 dias")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Media Movil: Sony")
    plt.xticks([])
    plt.show()

    plt.plot(RND_GME[0],RND_GME[1])
    plt.ylabel("Media Movil de 50 días")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Media Movil: Gamestop Enterprises")
    plt.xticks([])
    plt.show()
    
def Roll_Avg_200_Dias(SNE,GME,SNE_E,GME_E):
    aux_price=[]
    aux_panda=pd.DataFrame()
    RND_SNE=([],[])
    RND_GME=([],[])
    for i in range(len(SNE_E)):
        aux_price.append(SNE_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=200).mean()

    for i in range(len(SNE)):
        RND_SNE[0].append((SNE["Date"][len(SNE)-1-i]))  
        RND_SNE[1].append(aux_panda["MA"][246+i]) 

    aux_price=[]
    aux_panda=pd.DataFrame()    
    for i in range(len(GME_E)):
        aux_price.append(GME_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=200).mean()


    for i in range(len(SNE)):
        RND_GME[0].append((GME["Date"][len(SNE)-1-i]))  
        RND_GME[1].append(aux_panda["MA"][246+i]) 
    
    return [RND_GME,RND_SNE]

def Plot_Roll_Avg_200_Dias(RND_SNE,RND_GME):
    plt.plot(RND_SNE[0],RND_SNE[1],scalex=True)
    plt.ylabel("Media Movil de 200 dias")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Media Movil: Sony")
    plt.xticks([])
    plt.show()

    plt.plot(RND_GME[0],RND_GME[1])
    plt.ylabel("Media Movil de 200 días")
    plt.xlabel("Días: 08-01-2018 - 05-02-2021")
    plt.title("Media Movil: Gamestop Enterprises")
    plt.xticks([])
    plt.show()

##Funcion encargada de realizar la matriz de graficos.

def Matriz_Graficas(SNE,GME,SNE_E,GME_E):
    REND = Rend_Diario(SNE,GME);
    CINC = Roll_Avg_50_Dias(SNE,GME,SNE_E,GME_E);
    DOSC = Roll_Avg_200_Dias(SNE,GME,SNE_E,GME_E);
    
    fig,ax =  plt.subplots(2,3,figsize=(13,13));
    ax[0][0].plot(REND[0][0],REND[0][1],scalex=True);
    ax[0][0].set_xticks([])
    ax[0][0].set_title("Rendimiento Diario: Sony")
    ax[0][0].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    ax[0][0].set_ylabel("Rendimiento diario (%)")
    
    ax[0][1].plot(REND[1][0],REND[1][1],scalex=True);
    ax[0][1].set_xticks([])
    ax[0][1].set_title("Rendimiento Diario: Gamestop Enterprises")
    ax[0][1].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    ax[0][1].set_ylabel("Rendimiento diario (%)")
    
    ax[0][2].plot(CINC[0][0],CINC[0][1],scalex=True);
    ax[0][2].set_xticks([])
    ax[0][2].set_title("Media Movil: Sony")
    ax[0][2].set_ylabel("Media Movil de 50 dias")
    ax[0][2].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    
    ax[1][0].plot(CINC[1][0],CINC[1][1],scalex=True);
    ax[1][0].set_xticks([])
    ax[1][0].set_title("Media Movil: Gamestop Enterprises")
    ax[1][0].set_ylabel("Media Movil de 50 días")
    ax[1][0].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    
    ax[1][1].plot(DOSC[0][0],DOSC[0][1],scalex=True);
    ax[1][1].set_xticks([])
    ax[1][1].set_title("Media Movil: Sony")
    ax[1][1].set_ylabel("Media Movil de 200 dias")
    ax[1][1].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    
    ax[1][2].plot(DOSC[1][0],DOSC[1][1],scalex=True);
    ax[1][2].set_xticks([])
    ax[1][2].set_title("Media Movil: Gamestop Enterprises")
    ax[1][2].set_ylabel("Media Movil de 200 días")
    ax[1][2].set_xlabel("Días: 08-01-2018 - 05-02-2021")
    
    plt.show()


# In[2]:


def Covarianza(X,Y): #Se puede suponer que X e Y tienen el mismo número de elementos
    suma=0 
    for i in range(len(X)):
        suma+=((X[i]-Media(X))*(Y[i]-Media(Y)))
    return suma/(len(X))

def CovarianzaMuestral(X,Y): #Se puede suponer que X e Y tienen el mismo número de elementos
    suma=0
    for i in range(len(X)):
        suma+=((X[i]-Media(X))*(Y[i]-Media(Y)))
    return suma/(len(X)-1)

def Media(X):
    suma=0
    for i in range(len(X)):
        suma+=X[i]
    return suma/len(X)

def correlacion(X,Y):
    #Sabiendo que CovarianzaMuestra(X,X)=Varianza
    numerador=CovarianzaMuestral(X,Y)
    denominador=m.sqrt(CovarianzaMuestral(X,X))*m.sqrt(CovarianzaMuestral(Y,Y))
    return numerador/denominador

def ConvarianzaRendDiario(GME,SNE):
    RND_SNE=[]
    RND_GME=[]
    for i in range(len(SNE)): 
        RND_SNE.append(float(SNE["Change %"][i][:-1]))
        RND_GME.append(float(GME["Change %"][i][:-1]))

    print("Covarianza")
    print(Covarianza(RND_SNE,RND_SNE))    
    print(Covarianza(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(Covarianza(RND_GME,RND_SNE)) 
    print(Covarianza(RND_GME,RND_GME))
    #Covarianza <0 --> Cuando el rendimiento diario de Sony/GameStop sube, el rendimiento diario de la otra compañia baja

    print(" ")

    print("Coeficiente de Correlacion lineal de Pearson")
    print(correlacion(RND_SNE,RND_SNE)) # Debe ser 1 ya que la relación con sí mismo es de dependencia linea directa
    print(correlacion(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(correlacion(RND_GME,RND_SNE))
    print(correlacion(RND_GME,RND_GME))
    #Correlacion < 0 (pero muy poco) --> Hay poca dependencia lineal inversa ---> poca relación lineal

def Covarianza50Dias(GME,SNE,GME_E,SNE_E):
    aux_price=[]
    aux_panda=pd.DataFrame()
    RND_SNE=[]
    RND_GME=[]
    for i in range(len(SNE_E)):
        aux_price.append(SNE_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=50).mean()

    for i in range(len(SNE)):  
        RND_SNE.append(aux_panda["MA"][246+i]) 

    aux_price=[]
    aux_panda=pd.DataFrame()    
    for i in range(len(GME_E)):
        aux_price.append(GME_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=50).mean()
    
    for i in range(len(SNE)): 
        RND_GME.append(aux_panda["MA"][246+i]) 
    print("Covarianza")
    print(Covarianza(RND_SNE,RND_SNE))    
    print(Covarianza(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(Covarianza(RND_GME,RND_SNE)) 
    print(Covarianza(RND_GME,RND_GME))
    #Covarianza <0 --> Cuando el M.A. de 50 días de Sony/GameStop sube, el M.A. de la 50 días de la otra compañia baja

    print(" ")

    print("Coeficiente de Correlacion lineal de Pearson")
    print(correlacion(RND_SNE,RND_SNE)) # Debe ser 1 ya que la relación con sí mismo es de dependencia linea directa
    print(correlacion(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(correlacion(RND_GME,RND_SNE))
    print(correlacion(RND_GME,RND_GME))
    #Correlacion < 0 (pero muy poco) --> Hay poca dependencia lineal inversa ---> poca relación lineal

def Covarianza200Dias(GME,SNE,GME_E,SNE_E):
    aux_price=[]
    aux_panda=pd.DataFrame()
    RND_SNE=[]
    RND_GME=[]
    for i in range(len(SNE_E)):
        aux_price.append(SNE_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=200).mean()

    for i in range(len(SNE)):  
        RND_SNE.append(aux_panda["MA"][246+i]) 

    aux_price=[]
    aux_panda=pd.DataFrame()    
    for i in range(len(GME_E)):
        aux_price.append(GME_E["Price"][i])

    aux_price.reverse()
    aux_panda["Price"]=aux_price
    aux_panda["MA"]=aux_panda["Price"].rolling(window=200).mean()


    for i in range(len(SNE)):  
        RND_GME.append(aux_panda["MA"][246+i])  

    print("Covarianza")
    print(Covarianza(RND_SNE,RND_SNE))    
    print(Covarianza(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(Covarianza(RND_GME,RND_SNE)) 
    print(Covarianza(RND_GME,RND_GME))
    #Covarianza <0 --> Cuando el M.A. de 200 días de Sony/GameStop sube, el M.A. de la 200 días de la otra compañia baja
    print(" ")

    print("Coeficiente de Correlacion lineal de Pearson")
    print(correlacion(RND_SNE,RND_SNE)) # Debe ser 1 ya que la relación con sí mismo es de dependencia linea directa
    print(correlacion(RND_SNE,RND_GME)) #conmutación --> mismo resultado
    print(correlacion(RND_GME,RND_SNE))
    print(correlacion(RND_GME,RND_GME))
    #Correlacion < 0 --> Fuerte dependencia lineal inversa ---> Fuerte relación lineal


# In[3]:


menuSeleccion()

