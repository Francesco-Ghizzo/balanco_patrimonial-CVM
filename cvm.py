#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


d = pd.read_csv(r'C:\Users\atdal\Downloads\dfp_cia_aberta_BPA_con_2016.csv',encoding = 'ISO-8859-1',sep=";")


# In[3]:


d = d[d['CNPJ_CIA'] == '97.837.181/0001-47']


# In[4]:


df = d[['ORDEM_EXERC','CD_CONTA','DS_CONTA','VL_CONTA']].copy()
d.drop_duplicates(['CD_CONTA','DS_CONTA'], inplace = True)


# In[5]:


rubricas = {a:b for a,b in zip(d['CD_CONTA'],d['DS_CONTA'])}


# In[6]:


def primeiro_filtro(código):
    if len(código) == 1:
        classificação = rubricas[código]
    elif len(código) > 1:
        classificação = rubricas[código[:1]]
    return classificação

df['1º Classificação'] = df['CD_CONTA'].map(lambda x:primeiro_filtro(x))


# In[7]:


def segundo_filtro(código):
    if len(código) == 4:
        classificação = rubricas[código]
    elif len(código) > 4:
        classificação = rubricas[código[:4]]
    elif len(código) < 4:
        classificação = rubricas[código]
    return classificação

df['2º Classificação'] = df['CD_CONTA'].map(lambda x:segundo_filtro(x))


# In[8]:


def terceiro_filtro(código):
    if len(código) == 7:
        classificação = rubricas[código]
    elif len(código) > 7:
        classificação = rubricas[código[:7]]
    elif len(código) < 7:
        classificação = rubricas[código]
    return classificação

df['3º Classificação'] = df['CD_CONTA'].map(lambda x:terceiro_filtro(x))


# In[9]:


def quarto_filtro(código):
    if len(código) == 10:
        classificação = rubricas[código]
    elif len(código) > 10:
        classificação = rubricas[código[:10]]
    elif len(código) < 10:
        classificação = rubricas[código]
    return classificação

df['4º Classificação'] = df['CD_CONTA'].map(lambda x:quarto_filtro(x))


# In[10]:


def quinto_filtro(código):
    if len(código) == 13:
        classificação = rubricas[código]
    elif len(código) > 13:
        classificação = rubricas[código[:13]]
    elif len(código) < 13:
        classificação = rubricas[código]
    return classificação

df['5º Classificação'] = df['CD_CONTA'].map(lambda x:quinto_filtro(x))


# In[11]:


ultimo_df = df[(df['ORDEM_EXERC'] == 'ÚLTIMO')].copy()
ultimo_df.rename(columns = {'VL_CONTA':'Último'},inplace = True)
ultimo_df.drop('ORDEM_EXERC',axis = 1,inplace = True)
ultimo_df.reset_index(inplace = True)
penultimo_df = df[(df['ORDEM_EXERC'] == 'PENÚLTIMO')].copy()
penultimo_df.rename(columns = {'VL_CONTA':'Penúltimo'},inplace = True)
penultimo_df.drop('ORDEM_EXERC',axis = 1, inplace = True)
penultimo_df.reset_index(inplace = True)
new_df = pd.concat((ultimo_df.loc[:,(['DS_CONTA','1º Classificação','2º Classificação','3º Classificação',
                                      '4º Classificação','5º Classificação','Último'])],penultimo_df.loc[:,('Penúltimo')]),axis = 1)

