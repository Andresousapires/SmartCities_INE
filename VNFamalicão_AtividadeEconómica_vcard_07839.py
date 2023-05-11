import json
import requests
import pandas as pd
import os


vcard = "0007839"



url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
params = {
    "op": "2",
    "varcd": vcard,
    "Dim1": "T",
    "lang": "PT"
    }



# Geocod::
Dim2=['PT', '1', '11', '1190312']
N_Dim2=['Portugal','Continente','Norte','Vila Nova de Famalicão']



D1 = []
D2 = []
D3 = []
D4 = []
D5 = []
z = 0



for Geocod in Dim2:


    url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
    params = {
    "op": "2",
    "varcd": vcard,
    "Dim1": "T",
    "Dim2": Geocod,
    "lang": "PT"
    }

    response = requests.get(url, params=params)



    if response.status_code == 200:
        data = response.json()
    else:
        print("Erro ao fazer a solicitação: status code", response.status_code)

    n_anos = len(data[0]['Dados'])

    #print (data)

    Periodos = data[0]['Dados'].keys()



    for a in range(n_anos):
        if a < 10:
            Periodo = str(list(Periodos)[len(Periodos)- 1 - a])
            for i in range(len(data[0]['Dados'][str(Periodo)])):
                #Forma = data[0]['Dados'][Periodo][i]['dim_4_t']
                #Atividades = data[0]['Dados'][Periodo][i]['dim_3_t']
                Total = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append(N_Dim2[z])
                #D3.append(Atividades)
                D4.append(Total)
                #D5.append(Forma)
                
    z = z+1



dataf = {'Período de referência dos dados': D1,
            'Localização geográfica': D2,
            #'Dimensão': D3,
            #'Forma jurídica' : D5,
            'Escrituras celebradas (Nº)': D4
        }



data2 = pd.DataFrame(dataf)

#print (data2)

#json_data = data2.to_json()
path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\AtividadeEconómica'
file = 'dataINE_AtividadeEconómica_' + vcard + '.csv'
data2.to_csv(os.path.join(path, file), index=False)