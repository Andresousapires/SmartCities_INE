import json
import requests
import pandas as pd
import os


vcard = "0008512"



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
        if a < 120:
            Periodo = str(list(Periodos)[len(Periodos)- 1 - a])
            for i in range(len(data[0]['Dados'][str(Periodo)])):

                Atividades = data[0]['Dados'][Periodo][i]['dim_3_t']
                Total = data[0]['Dados'][Periodo][i].get('valor', 'na')
                D1.append(Periodo)
                D2.append(N_Dim2[z])
                D3.append(Atividades)
                D4.append(Total)
    z = z+1



dataf = {'Período de referência dos dados': D1,
            'Localização geográfica': D2,
            'Atividades': D3,
            'Pessoal ao servoço das Empresas, Anual': D4
        }



data2 = pd.DataFrame(dataf)

atividades_desejadas = ['Agricultura, produção animal, caça, floresta e pesca',
                        'Indústrias extrativas',
                        'Indústrias transformadoras',
                        'Eletricidade, gás, vapor, água quente e fria e ar frio',
                        'Captação, tratamento e distribuição de água; saneamento, gestão de resíduos e despoluição',
                        'Construção',
                        'Comércio por grosso e a retalho; reparação de veículos automóveis e motociclos',
                        'Transportes e armazenagem',
                        'Alojamento, restauração e similares',
                        'Atividades de informação e de comunicação',
                        'Atividades imobiliárias']

data2_filtrado = data2[data2['Atividades'].isin(atividades_desejadas)]

data2_filtrado = data2_filtrado.reset_index(drop = True)

print (data2_filtrado)

#json_data = data2.to_json()
path = r'C:\Users\Andre Pires\OneDrive - LCSD - Associação Data Colab\Documentos\código\SmartCity_Famalicao\integradas\ComercioeServiços'
file = 'dataINE_ComercioServiços_' + vcard + '.csv'
data2_filtrado.to_csv(os.path.join(path, file), index=False)