# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 3.
Practica 2.

Crear un archivo XML, donde se guarde el reporte de tipologia de datos
de la practica de pizzas del bloque anterior y la recomendacion propuesta.
'''

import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import numpy as np
import re


def analizar_calidad_de_datos(df, nombre_df):
    BLUE = "\033[4;36m"
    END = "\033[m"
    
    print('\n' + BLUE + f'Fichero {nombre_df}:' + END)
    df_types = df.dtypes
    df_nan = df.isna().sum()
    df_null = df.isnull().sum()
    df_info = pd.concat([df_types, df_nan, df_null], axis=1, sort=False)
    df_info.columns = ['Type', 'Number_of_NaN', 'Number_of_Null']
    print(df_info)
    return df_info


def ordenar_dataframes(order_details: pd.DataFrame, orders: pd.DataFrame):
    order_details_ordenado = order_details.sort_values('order_details_id', ascending=True)
    orders_ordenado = orders.sort_values('order_id', ascending=True)
    order_details_ordenado = (order_details_ordenado.reset_index()).drop(columns=['index'])
    orders_ordenado = (orders_ordenado.reset_index()).drop(columns=['index'])
    return order_details_ordenado, orders_ordenado


def fusionar_dataframes(order_details: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    '''
    Añadimos al dataframe order_details la fecha y el dia de la semana en el que se ha reaizado el encargo
    '''
    date_order_details = order_details.copy()
    
    tipos_pizza = list()
    tamano_pizzas = list()
    fechas = list()
    numero_semana = list()
    cantidades = list()
    
    for linea in range(len(date_order_details)):
        order_id = int(date_order_details.loc[linea, 'order_id']) - 1
        fecha_y_hora = str(orders.loc[order_id, 'date']) 
        cantidad = date_order_details.loc[linea, 'quantity']
        pizza = date_order_details.loc[linea, 'pizza_id']
        pizza = re.sub('-', '_', pizza)
        pizza = re.sub(' ', '_', pizza)
        pizza = re.sub('@', 'a', pizza)
        pizza = re.sub('3', 'e', pizza)
        pizza = re.sub('0', 'o', pizza)

        if type(cantidad) == int:
            cantidad = abs(cantidad)
        else:
            if re.fullmatch('one', cantidad.strip(), flags=re.I) != None:
                cantidad = 1
            elif re.fullmatch('two', cantidad.strip(), flags=re.I) != None:
                cantidad = 2
            else:
                cantidad = abs(int(cantidad))
        cantidades.append(cantidad)

        if pizza.endswith('_v'):
            tipos_pizza.append(np.nan)
            tamano_pizzas.append(np.nan)
        elif pizza.endswith('_xxl'):
            tipos_pizza.append(pizza[:-4])
            tamano_pizzas.append('xxl')
        elif pizza.endswith('_xl'):
            tipos_pizza.append(pizza[:-3])
            tamano_pizzas.append('xl')
        else:
            tipos_pizza.append(pizza[:-2])
            tamano_pizzas.append(pizza[-1])

        formatos = ['%B %d %Y', '%b %d %Y', '%Y-%m-%d', '%d-%m-%y %H:%M:%S', '%A,%d %B, %Y', '%a %d-%b-%Y']

        try: # Si salta un error es que no es un epoch_time
            fecha_y_hora = float(fecha_y_hora)
            fecha_linea = datetime.fromtimestamp(int(fecha_y_hora))
        except ValueError as e:
            i = 0
            while i < len(formatos):
                try: # Si no salta eeror ya hemos encontrado el formato correcto
                    fecha_linea = datetime.strptime(fecha_y_hora, formatos[i])
                    i= len(formatos) + 1
                except: # Si salta error probamos el siguiente tipo
                    i += 1
            if i == len(formatos):
                if linea != 0: # Si no es la primera ocurrencia:
                    fecha_linea = fechas[-1]
                else:
                    fecha_linea = datetime.strptime('01/01/2015', '%d/%m/%Y')

        fechas.append(fecha_linea)
        numero_semana.append(int((fecha_linea).strftime('%W')))

    date_order_details.pop('pizza_id')
    date_order_details.pop('quantity')
    date_order_details.insert(2, 'pizza_type_id', tipos_pizza, True)
    date_order_details.insert(3, 'pizza_size', tamano_pizzas, True)
    date_order_details['quantity'] = cantidades
    date_order_details['date'] = fechas
    date_order_details['week number'] = numero_semana
    
    # Si queremos guardar este nuevo dataframe en un csv, descomentamos la siguiente linea:
    # date_order_details.to_csv('date_order_details.csv')
    return date_order_details


def pizzas_type_df_a_dict(pizza_types):
    pizza_types_dict = dict()
    for i in range(len(pizza_types)):
        pizza_types_dict[pizza_types.loc[i, 'pizza_type_id']] = pizza_types.loc[i, 'ingredients']
    return pizza_types_dict


def que_ingredientes_hay(pizza_types):
    ingredientes = list()
    for i in range(len(pizza_types)):
        ingredientes_pizza = pizza_types.loc[i, 'ingredients']
        lista_ingredientes_pizza = ingredientes_pizza.split(', ')
        for ingrediente in lista_ingredientes_pizza:
            if not ingrediente in ingredientes:
                ingredientes.append(ingrediente)
    return ingredientes


def analizar_ingredientes_por_semana(df, df_ingredientes, pizza_types_dict):
    for i in range(2, 52):
        df_semana = df[df['week number'] == i].reset_index()
        df_ingredientes = contar_y_guardar_ingredientes_semana(df_semana, df_ingredientes, pizza_types_dict)
    return df_ingredientes


def contar_y_guardar_ingredientes_semana(df_semana, df_ingredientes, pizza_types_dict):
    dict_ingredientes = dict()
    for i in range(len(df_semana)):
        pizza = df_semana.loc[i, 'pizza_type_id']
        ingredientes_pizza_str = pizza_types_dict[pizza]
        ingredientes_pizza_list = ingredientes_pizza_str.split(', ')
        cantidad = df_semana.loc[i, 'quantity']
        tamano_letra = df_semana.loc[i, 'pizza_size']
        if tamano_letra == 's':
            tamano = 1
        elif tamano_letra == 'm':
            tamano = 2
        elif tamano_letra == 'l':
            tamano = 3
        elif tamano_letra == 'xl':
            tamano = 4
        elif tamano_letra == 'xxl':
            tamano = 5
        total = tamano*cantidad
        for ingrediente_pizza in ingredientes_pizza_list:
            if ingrediente_pizza in dict_ingredientes.keys():
                dict_ingredientes[ingrediente_pizza] += total
            else:
                dict_ingredientes[ingrediente_pizza] = total
    df_ingredientes_semana_i = pd.DataFrame(dict_ingredientes, [df_semana.loc[i, 'week number']])
    df_ingredientes = pd.concat([df_ingredientes, df_ingredientes_semana_i], sort=False)

    return df_ingredientes


def crar_xml(nombres_dfs, lista_analisis_dfs, lista_compra):
    root = ET.Element('root')  # Elemento raiz

    # Añadimos el contenido de los tipos de columna de cada Dataset utilizado
    info_dataset = ET.SubElement(root, 'infodatasets')
    for num_df in range(len(lista_analisis_dfs)):
        df = lista_analisis_dfs[num_df]
        dataset = ET.SubElement(info_dataset, 'dataset')
        nombre_df = ET.SubElement(dataset, 'dataset_name')
        nombre_df.text = nombres_dfs[num_df]
        for columna_i in df.index:
            columna = ET.SubElement(dataset, 'dataset_column')
            nombre_columna = ET.SubElement(columna, 'column_name')
            nombre_columna.text = columna_i
            for info_i in df.columns:
                info = ET.SubElement(columna, info_i)
                info.text = str(df[info_i][columna_i])
    
    # Añadimos el contenido de la lista de la compra.
    contenido = ET.SubElement(root, 'contents')
    texto_introduccion = 'En este programa vamos a asumir que acabamos de acabar la semana 51 de 2015 y queremos comprar los ingredientes de la semana que viene, la semana 52.'
    intro = ET.SubElement(contenido, 'introduction')
    intro.text = texto_introduccion
    elemento_lista_compra = ET.SubElement(contenido, 'shopping_list')

    for num_ingrediente in lista_compra.index:
        ingrediente = ET.SubElement(elemento_lista_compra, 'ingredient')
        nombre_ingrediente = ET.SubElement(ingrediente, 'ingredient_name')
        nombre_ingrediente.text = str(lista_compra['Ingredient'][num_ingrediente])
        cantidad_ingrediente = ET.SubElement(ingrediente, 'ingredient_amount')
        cantidad_ingrediente.text = str(lista_compra['Quantity'][num_ingrediente])

    ET.indent(root)
    tree = ET.ElementTree(root)
    tree.write('lista_de_la_compra.xml', encoding='UTF-8', xml_declaration=True)


def Extract(nombres, separadores):
    dataframes = list()
    lista_df_info = list()
    for i in range(len(nombres)):
        dataframe = pd.read_csv(nombres[i]+'.csv', encoding='latin_1', sep=separadores[i])
        lista_df_info.append(analizar_calidad_de_datos(dataframe, nombres[i]))
        dataframes.append(dataframe)

    return dataframes, lista_df_info


def Transform(order_details, orders, pizza_types):
    order_details_ordenado, orders_ordenado = ordenar_dataframes(order_details, orders)
    order_details_ordenado['quantity'].fillna(value=1, inplace=True)
    order_details_ordenado['pizza_id'].fillna(value='empty_order_v', inplace=True)
    date_order_details = fusionar_dataframes(order_details_ordenado, orders_ordenado)
    date_order_details = date_order_details[date_order_details['pizza_type_id'].notna()]
    date_order_details = (date_order_details.reset_index()).drop(columns=['index'])

    pizza_types_dict = pizzas_type_df_a_dict(pizza_types)
    ingredientes = que_ingredientes_hay(pizza_types)
    df_ingredientes = pd.DataFrame(columns=ingredientes)

    df_ingredientes = analizar_ingredientes_por_semana(date_order_details, df_ingredientes, pizza_types_dict)
    df_ingredientes = df_ingredientes.fillna(0)
    lista_de_la_compra = df_ingredientes.median().round(0).astype(int)
    lista_de_la_compra = pd.DataFrame(lista_de_la_compra).reset_index()
    lista_de_la_compra.columns = ['Ingredient', 'Quantity']

    return lista_de_la_compra


def Load(nombres, lista_df_info, lista_de_la_compra):

    RED = "\033[3;31m"
    YELLOW = "\033[5;33m"
    END = "\033[m"

    print(RED + '\nEn este programa vamos a asumir que acabamos de acabar la semana 51 de 2015')
    print('y queremos comprar los ingredientes de la semana que viene, la semana 52.\n' + END)

    print(YELLOW + 'Tras analizar el dataset proporcionado, hemos deducido que hay que comprar')
    print('los siguientes ingredientes:' + END)

    print(lista_de_la_compra)

    print('\nCreamos un xml con esta informacion.')
    crar_xml(nombres, lista_df_info, lista_de_la_compra)
    return 


if __name__ == '__main__':
    nombres = ['order_details', 'orders', 'pizza_types']
    separadores = [';', ';', ',']
    dataframes, lista_df_info = Extract(nombres, separadores)
    order_details = dataframes[0]
    orders = dataframes[1]
    pizza_types = dataframes[2]
    lista_de_la_compra = Transform(order_details, orders, pizza_types)
    Load(nombres, lista_df_info, lista_de_la_compra)