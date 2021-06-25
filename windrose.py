# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 19:09:12 2019

@author: plinio.silva
"""
import pandas as pd
import sys
import numpy as np
#sys.exit() #apenas comodidade para carregar apenas bibliotecas. Deve estar comentado.
#%% Windrose 
arquivo = 'Exemplo.pkl'
outmet = pd.read_pickle(arquivo)
outmet = outmet.set_index('time')
outmet = outmet.loc[:,:'10gustdirc']
outmet = outmet.drop('10gustdirc',axis=1)
#%%

#transformado os dados que estão em str em float
for i in outmet.columns[:14]:
    outmet[i] = pd.to_numeric(outmet[i],errors = 'coerce' )


#%%
#drop nos NaN para nao atrapalhar no calculo da frequencia
outmet = outmet.dropna(axis = 0)


#%% Tirando dados espurios 
outmet = outmet[outmet['wspdavg'] > 0]
outmet = outmet[np.logical_and(outmet['wdiravg'] > 0,outmet['wdiravg'] < 359)]

#%%
#definindo o intervalo de intensidades.
intensidades = np.linspace(0,max(outmet['wspdavg']),10) 


# Definindo o internvalo de direcoes
# +22.5 ==> Colocar os eixos cardeais como ponto medio. 0 graus ==> Norte, 
# +360 para tornar o -45 em 315 graus.
direcoes = [aux for aux in np.arange(- 22.5,361 - 22.5, 45)] #temp intervalo de direcoes


#%% Colocando os valores que estao entre 315 e 0 na escala -22.5 e 0, para facitar o split pela direcao
outmet.loc[:,'wdiravg'] = outmet['wdiravg'].apply(lambda x: x - 360 if x >= 337.5 else x)


#%%

rose = dict( 
frequency = [],
direction = [],
strength = [],
)

#%% Calculando as frequencias e intensidades da windrose
for i in outmet.groupby(pd.cut(outmet['wdiravg'],direcoes)): #Agrupando por direcao
    
    #i[0] --> intervalo de direcao.
    #i[1] --> dataframe com o intervalo de direcoes 
    #i[0].mid --> eh o indice que representa o eixo cardeal.
    print("Direcao: ",i[0].mid,' ---------------------------')
    for j in i[1].groupby(pd.cut(i[1]['wspdavg'],intensidades)): #Agrupando por velocidade
        a = pd.cut(i[1]['wspdavg'],intensidades)
        pass
        #j[1] --> dataframe com dados de velocidade dentro dos limiter de direcao e velocidade estipulados
        #j[0].left --> limite esquerdo do intervalo
        #j[0].right -> limite direito do intervalo
        
        rose['direction'].append(i[0].mid)
        rose['frequency'].append(len(j[1])/len(outmet)*100)
        rose['strength'].append('%.1f - %.1f'%(j[0].left,j[0].right))
        print("Frequencia: ",len(j[1])/len(outmet)*100)
        print('Forca %.1f - %.1f'%(j[0].left,j[0].right))
        print()
        pass
    pass

#%%
windrose =  pd.DataFrame(rose)
windrose['frequency'].sum()

import plotly.express as px
from plotly.offline import plot

fig = px.bar_polar(windrose, r="frequency", theta="direction",title = arquivo,
                   color="strength", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma[-2::-1])

plot(fig,filename = arquivo.replace('pkl','html'))
