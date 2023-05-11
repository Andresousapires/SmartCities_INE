import json
import requests
import pandas as pd
import os

vcard = "0008714"

url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
params = {
    "op": "2",
    "varcd": vcard,
    "Dim1": "T",
    "lang": "PT"
    }

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print("Erro ao fazer a solicitação: status code", response.status_code)

data_actual = data[0]['UltimoPref']
Periodo1 = data_actual[0:4]
n_censos = len(data[0]['Dados'])

#print(data[0]['Dados'])

Periodos = data[0]['Dados'].keys()
for i in range(n_censos):
    valor = list(Periodos)[i] 

# Geocod::
Portugal = 'PT'
Continente = '1'
Norte = '11'
VNFamalicao = '1190312'

D1=[]
D2=[]
D3=[]
D4=[]
D5=[]

for a in range(n_censos):
    if a < 11:
        Periodo = str(list(Periodos)[len(Periodos)- 1 - a])
        for i in range(len (data[0]['Dados'][Periodo])):
            if data[0]['Dados'][Periodo][i]['geocod'] == Norte:
                
                
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Norte')
                
                
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Portugal:
                
                
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Portugal')
                
                
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Continente:
                
                
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Continente')
                
                
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == VNFamalicao:
                
                
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Vila Nova de Famalicão')
                
                
                D5.append(valor)

    dataf = {'Periodo': D1,
            'NUTS - 2013': D2,

            
            'Taxa de abstenção nas eleições para a Assembleia da República': D5
            }


data1 = pd.DataFrame(dataf)
json_data = data1.to_json()

#print (data1)

path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\Cidadania'
file = 'dataINE_Cidadania_' + vcard + '.csv'
data1.to_csv(os.path.join(path, file), index=False)