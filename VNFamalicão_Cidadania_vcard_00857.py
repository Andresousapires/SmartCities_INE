import json
import requests
import pandas as pd
import os

vcard = "0000857"

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
                
                tipo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Norte')
                
                D4.append(tipo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Portugal:
                
                tipo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Portugal')
                
                D4.append(tipo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == Continente:
                
                tipo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Continente')
                
                D4.append(tipo)
                D5.append(valor)
            if data[0]['Dados'][Periodo][i]['geocod'] == VNFamalicao:
                
                tipo = data[0]['Dados'][Periodo][i]['dim_3_t']
                valor = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append('Vila Nova de Famalicão')
                
                D4.append(tipo)
                D5.append(valor)

    dataf = {'Periodo': D1,
            'NUTS - 2013': D2,

            'Tipo de ato notarial': D4,
            'Principais atos notariais celebrados por escritura pública nos cartórios notariais': D5
            }


data1 = pd.DataFrame(dataf)
json_data = data1.to_json()

#print (data1)

path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\Cidadania'
file = 'dataINE_Cidadania_' + vcard + '.csv'
data1.to_csv(os.path.join(path, file), index=False)