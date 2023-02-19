# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 07:49:58 2023

@author: Roberto Martinez Guzman
"""

import pandas as pd
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generación de los universos de las variables
Estatura = np.arange(1.6, 2.05, .05 )
Promedio = np.arange(0, 5.5, .5)

# Generación de las funciones de membresía fuzzy
Estatura_baja = fuzz.trimf(Estatura, [1.45, 1.6, 1.75])
Estatura_media = fuzz.trimf(Estatura, [1.6, 1.75, 2])
Estatura_alta = fuzz.trimf(Estatura, [1.75, 2, 2.25])
Promedio_bajo = fuzz.trimf(Promedio, [-3.5, 0, 3.5])
Promedio_medio = fuzz.trimf(Promedio, [0, 3.5, 5])
Promedio_alto = fuzz.trimf(Promedio, [3.5, 5, 6.5])

# Visualización de los Universos y las funciones de membresía
fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 9))

ax0.plot(Estatura, Estatura_baja, 'b', linewidth=1.5, label='Baja')
ax0.plot(Estatura, Estatura_media, 'g', linewidth=1.5, label='Media')
ax0.plot(Estatura, Estatura_alta, 'r', linewidth=1.5, label='Alta')
ax0.set_title('Estatura')
ax0.legend()
ax1.plot(Promedio, Promedio_bajo, 'b', linewidth=1.5, label='Bajo')
ax1.plot(Promedio, Promedio_medio, 'g', linewidth=1.5, label='Medio')
ax1.plot(Promedio, Promedio_alto, 'r', linewidth=1.5, label='Alto')
ax1.set_title('Promedio')
ax1.legend()

# Eliminación de los ejes superior y derecho en las gráficas de las variables de membresía
for ax in (ax0, ax1):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

# Seleccionar dos jugadores con estatura alta y promedio académico alto

# Leer excel con los datos: Nombre, Estatura, Promedio Académico y un campo adicional llamado indicador donde quedará
# el resultado de la regla de activacion para cada jugador

df = pd.read_excel(r'C:\jugadores.xlsx')

# Reglas de activación para cada jugador

for i in range(len(df.index)):
    Estatura_nivel_baja = fuzz.interp_membership(Estatura, Estatura_baja, df.loc[i, 'Estatura'])
    Estatura_nivel_media = fuzz.interp_membership(Estatura, Estatura_media, df.loc[i, 'Estatura'])
    Estatura_nivel_alta = fuzz.interp_membership(Estatura, Estatura_alta, df.loc[i, 'Estatura'])

    Promedio_nivel_bajo = fuzz.interp_membership(Promedio, Promedio_bajo, df.loc[i, 'Promedio académico'])
    Promedio_nivel_medio = fuzz.interp_membership(Promedio, Promedio_medio, df.loc[i, 'Promedio académico'])
    Promedio_nivel_alto = fuzz.interp_membership(Promedio, Promedio_alto, df.loc[i, 'Promedio académico'])
    
#   Se graba en el dataframe el resultado del mínimo entre estatura alta y promedio alto para cada jugador     
    
    df.loc[i, 'Indicador'] = np.fmin(Estatura_nivel_alta, Promedio_nivel_alto)

# Actualizar el excel con los valores de activavcion para cada jugador
df.to_excel(r'C:\jugadores.xlsx', index=False)







