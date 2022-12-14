# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 1.
Practica 2.

Hacer un recomendador de uno de los topics que elijáis, películas, música, series...
(Extraer dataset de www.kaggle.com) Para ello tendréis que elegir un dataset en formato
csv y montar este proceso a través de una ETL que os extraiga la información del csv elegido
y mediante el uso de expresiones regulares os devuelva al menos por pantalla la recomendación
propuesta sobre un input dado.

Opcional:
Esta ETL será desplegada a traves de un orquestador como puede ser Dagster o Airflow.
'''

import pandas as pd
import re
import random

def extract():
    df = pd.read_csv('tv_shows_data.csv')
    return df

def transform(df: pd.DataFrame):
    #Nos quedamos solo las columnas que queremos queremos
    df = df[['Title', 'Genre']]
    #Pedimos el genero de la serie que desea ver
    entrada = input('Choose the genre that you would like to watch: ')
    entrada = entrada.strip()
    #Buscamos las coincidencias en el dataframe con las series
    series = []
    for i in range(len(df['Genre'])):
        if re.search(entrada, df['Genre'][i], flags=re.I) != None:
            series.append(df['Title'][i])
    return series

def load(series: list):
    if len(series) > 3:
        print('Showing 3 recommendations:')
        for i in range(3):
            serie = series.pop(random.randint(0, len(series) - 1))
            print(f'{i+1}) {serie}.')
        if len(series) > 3:
            opc = input('Would you like to see some other 3 recommendations (Y/n): ').strip()
        while opc == 'Y':
            if len(series) >= 3:
                print('Showing 3 recommendations:')
                for i in range(3):
                    serie = series.pop(random.randint(0, len(series) - 1))
                    print(f'{i+1}) {serie}.')
                opc = input('Would you like to see some other 3 recommendations (Y/n): ').strip()
            else:
                opc = 'n'

    elif len(series) == 0:
        print('There is not any recommendations for this genre.')
   
    else:
        print(f'There are {len(series)} recommendations.')
        for i in range(3):
            serie = series.pop(i)
            print(f'{i+1}) {serie}.')



if __name__ == '__main__':
    df = extract()
    series = transform(df)
    load(series)