import json
import requests
import pandas as pd
import os

vcard = "0008291"

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
                tipo_médico = data[0]['Dados'][Periodo][i]['dim_4_t']
                sexo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Norte')
                D3.append(tipo_médico)
                D4.append(sexo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Portugal:
                tipo_médico = data[0]['Dados'][Periodo][i]['dim_4_t']
                sexo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Portugal')
                D3.append(tipo_médico)
                D4.append(sexo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Continente:
                tipo_médico = data[0]['Dados'][Periodo][i]['dim_4_t']
                sexo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Continente')
                D3.append(tipo_médico)
                D4.append(sexo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == VNFamalicao:
                tipo_médico = data[0]['Dados'][Periodo][i]['dim_4_t']
                sexo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Vila Nova de Famalicão')
                D3.append(tipo_médico)
                D4.append(sexo)
                D5.append(valor)

    dataf = {'Periodo': D1,
            'NUTS - 2013': D2,
            'Domínios de ambiente' : D3,
            'Classificador económico': D4,
            'Despezas em ambiente dos municípios': D5
            }


data1 = pd.DataFrame(dataf)
json_data = data1.to_json()

#print (data1)

path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\Administração_Pública'
file = 'dataINE_Administração_' + vcard + '.csv'
data1.to_csv(os.path.join(path, file), index=False)