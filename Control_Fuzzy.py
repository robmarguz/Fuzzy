# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:27:31 2023

@author: Roberto Martinez Guzman robmarguz@aol.com
"""

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

Temperatura_ambiente = np.arange(20, 41, 1)
Humedad_relativa = np.arange(70, 91, 1)
Voltaje = np.arange(0, 12.5, .5)

Temperatura_baja = fuzz.trimf(Temperatura_ambiente, [0, 20, 30])
Temperatura_media = fuzz.trimf(Temperatura_ambiente, [20, 30, 40])
Temperatura_alta = fuzz.trimf(Temperatura_ambiente, [30, 40, 40])

Humedad_baja = fuzz.trimf(Humedad_relativa, [0, 70, 80])
Humedad_media = fuzz.trimf(Humedad_relativa, [70, 80, 90])
Humedad_alta = fuzz.trimf(Humedad_relativa, [80, 90, 90])

Voltaje_B =  fuzz.trimf(Voltaje, [0, 0, 3])
Voltaje_VMB = fuzz.trimf(Voltaje, [0, 3, 6])
Voltaje_VM =  fuzz.trimf(Voltaje, [3, 6, 9])
Voltaje_VMA = fuzz.trimf(Voltaje, [6, 9, 12])
Voltaje_VA =  fuzz.trimf(Voltaje, [9, 12, 12])

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
ax0.plot(Temperatura_ambiente, Temperatura_baja, 'r', linewidth=2, label='Baja')
ax0.plot(Temperatura_ambiente, Temperatura_media, 'g', linewidth=2, label='Media')
ax0.plot(Temperatura_ambiente, Temperatura_alta, 'y', linewidth=2, label='Alta')
ax0.set_title('Temperatura Ambiente')
ax0.legend()


ax1.plot(Humedad_relativa, Humedad_baja, 'r', linewidth=2, label='Baja')
ax1.plot(Humedad_relativa, Humedad_media, 'g', linewidth=2, label='Media')
ax1.plot(Humedad_relativa, Humedad_alta, 'y', linewidth=2, label='Alta')
ax1.set_title('Humedad Relativa')
ax1.legend()

ax2.plot(Voltaje, Voltaje_B, 'r', linewidth=2, label='Bajo')
ax2.plot(Voltaje, Voltaje_VMB, 'g', linewidth=2, label='Medio Bajo')
ax2.plot(Voltaje, Voltaje_VM, 'y', linewidth=2, label='Medio')
ax2.plot(Voltaje, Voltaje_VMA, 'c', linewidth=2, label='Medio Alto')
ax2.plot(Voltaje, Voltaje_VA, 'b', linewidth=2, label='Alto')
ax2.set_title('Voltaje Aplicado')
ax2.legend()

for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
plt.tight_layout()


Temperatura_nivel_bajo = fuzz.interp_membership(Temperatura_ambiente, Temperatura_baja, 37)
Temperatura_nivel_medio = fuzz.interp_membership(Temperatura_ambiente, Temperatura_media, 37)
Temperatura_nivel_alto = fuzz.interp_membership(Temperatura_ambiente, Temperatura_alta, 37)

Humedad_nivel_bajo = fuzz.interp_membership(Humedad_relativa, Humedad_baja, 82)
Humedad_nivel_medio = fuzz.interp_membership(Humedad_relativa, Humedad_media, 82)
Humedad_nivel_alto = fuzz.interp_membership(Humedad_relativa, Humedad_alta, 82)

active_rule1 = np.fmin(Temperatura_nivel_medio, Humedad_nivel_medio)
active_rule2 = np.fmin(Temperatura_nivel_alto, Humedad_nivel_medio)
active_rule3 = np.fmin(Temperatura_nivel_medio, Humedad_nivel_alto)
active_rule4 = np.fmin(Temperatura_nivel_alto, Humedad_nivel_alto)


Activacion_VM = np.fmin(active_rule1, Voltaje_VM)
Activacion_VMA = np.fmin(active_rule2, Voltaje_VMA)
Activacion_VA = np.fmin(active_rule3, Voltaje_VA)


tip0 = np.zeros_like(Voltaje)

fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.fill_between(Voltaje, tip0, Activacion_VM, facecolor='b', alpha=0.7) 
ax0.fill_between(Voltaje, tip0, Activacion_VMA, facecolor='b', alpha=0.7) 
ax0.fill_between(Voltaje, tip0, Activacion_VA, facecolor='b', alpha=0.7) 



ax0.set_title('Actividades de la membresías')


for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

Agregado = np.fmax(Activacion_VA, 
                     np.fmax(Activacion_VM, Activacion_VMA))

Voltaje_aplicado = fuzz.defuzz(Voltaje, Agregado, 'centroid')

Activacion = fuzz.interp_membership(Voltaje, Agregado, Voltaje_aplicado) 

fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.plot(Voltaje, Voltaje_VM, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(Voltaje, Voltaje_VMA, 'g', linewidth=0.5, linestyle='--')
ax0.plot(Voltaje, Voltaje_VA, 'r', linewidth=0.5, linestyle='--')

ax0.fill_between(Voltaje, tip0, Agregado, facecolor='Orange', alpha=0.7)

ax0.plot([Voltaje_aplicado, Voltaje_aplicado], [0, Activacion], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Membresías agregadas y línea de resultado')

for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
plt.tight_layout()
























































