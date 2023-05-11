import json
import requests
import pandas as pd
import os


vcard = "0011613"



url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
params = {
    "op": "2",
    "varcd": vcard,
    "Dim1": "T",
    "lang": "PT"
    }



# Geocod::
#Dim2=['PT', '1', '11', '0312']

Dim2=['PT', '1', '11','0312','031204',
      '031206', '031210', '031212', '031213', '031215',
      '031216', '031219', '031221', '031223', '031224',
      '031225', '031227', '031239', '031242', '031230',
      '031232', '031233', '031234', '031235', '031250',
      '031251', '031252', '031253', '031254', '031255',
      '031256', '031257', '031258', '031259', '031260',
      '031241', '031247', '031249']

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
                
                Atividades = data[0]['Dados'][Periodo][i]['dim_3_t']
                Total = data[0]['Dados'][Periodo][i].get('valor', 'na')
                N_Dim2 = data[0]['Dados'][Periodo][i]['geodsg']
                D1.append(Periodo)
                D2.append(N_Dim2)
                D3.append(Atividades)
                D4.append(Total)
                
    z = z+1



dataf = {'Período de referência dos dados': D1,
            'Localização geográfica': D2,
            'Sexo': D3,
            
            'Densidade Populacional': D4
        }

data2 = pd.DataFrame(dataf)

print (data2)

path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\OrdenamentoDoTerritório'
file = 'dataINE_OrdenamentoDoTerritório_' + vcard + '.csv'
data2.to_csv(os.path.join(path, file), index=False)