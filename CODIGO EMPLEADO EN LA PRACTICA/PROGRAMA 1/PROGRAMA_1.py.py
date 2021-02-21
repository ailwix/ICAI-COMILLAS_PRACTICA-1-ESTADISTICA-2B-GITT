#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import pandas as pd
from scipy import stats
from collections import Counter
import csv

##IMFORMACION RELEVANTE.
##ESTE PROGRAMA GENERA FICHEROS CON DATOS. SOLAMENTE ES NECESARIO EJECUTAR LA FUNCION menuSeleccion() Y PEDIR LO 
##QUE SE NECESITA. SE MUESTRAN LAS ESTADISTICAS DE TODOS LOS DATOS RELEVANTES.


# In[2]:


def comprobarOpcion():
    while (True):
        val = input("Seleccione una opción: ")
        if val not in ["1","2","3"]:
            print("Seleccione una opcion válida")
        else:
            return val

def menuSeleccion():
    op = ["Price","Open","High","Low","Vol","Change %"]
    print("----------- INTERFAZ ESTADISTICA PRACTICA 1 -----------")
    print("Seleccione la operación a realizar: ")
    print("1. Analisis de datos de GameStop")
    print("2. Analisis de datos de Sony (división de videojuegos)")
    print("3. Cerrar la interfaz")
    print("\n")
    
    val = comprobarOpcion()
    
    if (int(val) == 1):
        data = load_pandas()
        gamestop = data[0]
        print("Cargando datos seleccionados...")
        print("\n")
        print("----------- Analisis de GameStop -----------")
        print("1. Calculo de medidas estadisticas")
        print("2. Dibujo de histograma de frecuencias relativas")
        print("3. Tabla de frecuencias")
        print("\n")
        val = comprobarOpcion()
        
        if (int(val) == 1):
            print("\n")
            datos  = []
            for i in range(0,len(gamestop)):
                print("MEDIDA " + str(i+1) + " : " + op[i])
                print("\n")
                datos.append(measures(gamestop[i]))
                print("\n")
            excelWriter(datos,"Medidas estadisticas de GameStop")
            print("Se ha generado un fichero csv con los datos")
            menuSeleccion()
            
        elif (int(val) == 2):
            for i in range(0,len(gamestop)):
                print("HISTOGRAMA " + str(i+1) + " : " + op[i])
                draw_hist_rel_frec(gamestop[i],"Histograma de frecuencias relativas: " + op[i])
            menuSeleccion()
        
        elif (int(val) == 3):
            frec_table(list(gamestop[0]),"Tabla de frecuencias de GameStop")
            print("Se ha generado un fichero csv con los datos")
            menuSeleccion()
    
    elif (int(val) == 2):
        data = load_pandas()
        sony = data[1]
        print("Cargando datos seleccionados...")
        print("\n")
        print("----------- Analisis de Sony -----------")
        print("1. Calculo de medidas estadisticas")
        print("2. Dibujo de histograma")
        print("3. Tabla de frecuencias")
        print("\n")
        val = comprobarOpcion()
        
        if (int(val) == 1):
            print("\n")
            datos = []
            for i in range(0,len(sony)):
                print("MEDIDA " + str(i+1) + " : " + op[i])
                print("\n")
                datos.append(measures(sony[i]))
                print("\n")
            excelWriter(datos,"Medidas estadisticas de Sony")
            print("Se ha generado un fichero csv con los datos")
            menuSeleccion()
            
        elif (int(val) == 2):
            for i in range(0,len(sony)):
                print("HISTOGRAMA " + str(i+1) + " : " + op[i])
                draw_hist_rel_frec(sony[i],"Histograma de frecuencias relativas: " + op[i])
            menuSeleccion()
        
        elif (int(val) == 3):
            frec_table(list(sony[0]),"Tabla de frecuencias de Sony")
            print("Se ha generado un fichero csv con los datos")
            menuSeleccion()
    
    elif (int(val) == 3):
        print("Saliendo...")
        return

def load_pandas():
    df_gme = pd.read_csv("GME_Historical_Data.csv",encoding = "ISO-8859-1")
    date_gme = df_gme.iloc[0:]["Date"]
    price_gme = df_gme.iloc[0:]["Price"]
    op_gme = df_gme.iloc[0:]["Open"]
    high_gme = df_gme.iloc[0:]["High"]
    low_gme = df_gme.iloc[0:]["Low"]
    vol_gme = df_gme.iloc[0:]["Vol."]
    change_gme = df_gme.iloc[0:]["Change %"]
    
    vol_gme_i=[]
    for i in np.array(vol_gme):
        if (i != "-"):
            vol_gme_i.append(i.strip('M'))
    
    vol_gme_ii=[]
    for i in np.array(vol_gme_i):
        if (i != "-"):
            vol_gme_ii.append(float(i.strip('K')))
        
    change_gme_i=[]
    for i in np.array(change_gme):
        if (i != "-"):
            change_gme_i.append(float(i.strip('%')))
    
    df_sne = pd.read_csv("SNE_Historical_Data.csv",encoding = "ISO-8859-1")
    date_sne = df_sne.iloc[0:]["Date"]
    price_sne = df_sne.iloc[0:]["Price"]
    op_sne = df_sne.iloc[0:]["Open"]
    high_sne = df_sne.iloc[0:]["High"]
    low_sne = df_sne.iloc[0:]["Low"]
    vol_sne = df_sne.iloc[0:]["Vol."]
    change_sne = df_sne.iloc[0:]["Change %"]
    
    vol_sne_i=[]
    for i in np.array(vol_sne):
        if (i != "-"):
            vol_sne_i.append(i.strip('M'))
    
    vol_sne_ii=[]
    for i in np.array(vol_sne_i):
        if (i != "-"):
            vol_sne_ii.append(float(i.strip('K')))
        
    change_sne_i=[]
    for i in np.array(change_sne):
        if (i != "-"):
            change_sne_i.append(float(i.strip('%')))
    
    
    data_gme = [price_gme,op_gme,high_gme,low_gme,vol_gme_ii,change_gme_i]
    data_sne = [price_sne,op_sne,high_sne,low_sne,vol_sne_ii,change_sne_i]
    
    return data_gme,data_sne,date_gme,date_sne

def measures(data):
    avg = st.mean(data)
    med = st.median(data)
    f_med = np.quantile(data,.25)      ##PRIMER CUARTIL
    l_med = np.quantile(data,.75)     ##SEGUNDO CUARTIL
    interqu_range = l_med - f_med    ##RANGO INTERCUARTILICO
    
    pstdev = st.pstdev(data)         ##DESVIACION MEDIA
    pvar = st.pvariance(data)        ##VARIANZA
    stdev = st.stdev(data)           ##DESVIACION MUESTRAL
    var = st.variance(data)          ##VARIANZA MUESTRAL
    
    print("MEDIA: " + str(avg))
    print("MEDIANA: " + str(med))
    print("PRIMER CUARTIL: " + str(f_med))
    print("TERCER CUARTIL: " + str(l_med))
    print("RECORRIDO INTERCUARTILICO: " + str(interqu_range))
    
    print("DESVIACION MEDIA: " + str(pstdev))
    print("VARIANZA: " + str(pvar))
    print("DESVIACION MEDIA MUESTRAL: " + str(stdev))
    print("VARIANZA MUESTRAL: " + str(var))
    
    val = [avg,med,f_med,l_med,interqu_range,pstdev,pvar,stdev,var]
    return val

def excelWriter(data,title):
    col = ["Media","Mediana","Primer Cuartil","Segundo Cuartil","Rango intercuartilico",
            "Desviacion media","Varianza","Desviacion media muestral","Varianza muestral"]
    row = ["Price","Open","High","Low","Vol","Change %"]
    df = pd.DataFrame(data,index=row,columns=col)
    df.to_csv(title,sep=";",index=True)
    
def draw_hist_rel_frec(data,title):
    res = stats.relfreq(data, numbins=150, defaultreallimits=None, weights=None)
    x = res.lowerlimit + np.linspace(0, res.binsize*res.frequency.size,res.frequency.size)
    fig = plt.figure(figsize=(30, 20))
    
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(x, res.frequency, width=res.binsize)
    ax.set_title(title)
    ax.set_xlim([x.min(), x.max()+5])
    plt.show()

def frec_table(data,title):
    data.sort()
    frec_rel = []
    
    header = ["VALOR","FREC. ABSOLUTA","FREC. RELATIVA","FREC. ABS. ACUMULADA","FREC. RE. ACUMULADA"]
    valor = list(Counter(data).keys())
    frec_abs = list(Counter(data).values())
    for i in range(0,len(frec_abs)): frec_rel.append(frec_abs[i]/len(data))
    frec_abs_ac = list(np.cumsum(frec_abs))
    frec_rel_ac = list(np.cumsum(frec_rel))
    
    table = [valor,frec_abs,frec_rel,frec_abs_ac,frec_rel_ac]
    df = pd.DataFrame(np.transpose(table),columns=header)
    print(df)
    df.to_csv(title,sep=";",index=False)
    


# In[3]:


menuSeleccion()

