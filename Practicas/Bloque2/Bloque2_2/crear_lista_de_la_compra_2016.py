# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 2.
Practica 2.

Pizzerias Maven ha actualizado sus orders a 2016 le gustaría volver a saber saber que stock de
ingredientes deberían comprar a la semana, para optimizar el stock de ingredientes y las compras
de estos en función del nuevo dataset.

Entrega:
Dirección de github con al menos el siguiente contenido.
- Informe de calidad de los datos, reflejando la tipología de cada columna y el numero de NaN
  y Null por cada columna.
- ETL para transformar los datos en función de los requerimientos decididos por cada uno a la
  hora de realizar data wrangling, si es necesario.
- ETL que saque como output un csv con la compra semanal de ingredientes.

Opcional:
- Todo lo necesario para desplegar esto a través de docker y Airflow.
'''

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
    df_info.columns = ['Type', 'Number of NaN', 'Number of Null']
    print(df_info)


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
        fecha_sin_hora = str(orders.loc[order_id, 'date']) 
        hora = str(orders.loc[order_id, 'time'])
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
            fecha_sin_hora = float(fecha_sin_hora)
            fecha_linea = datetime.fromtimestamp(int(fecha_sin_hora))
        except ValueError as e:
            i = 0
            while i < len(formatos):
                try: # Si no salta eeror ya hemos encontrado el formato correcto
                    fecha_linea = datetime.strptime(fecha_sin_hora, formatos[i])
                    i= len(formatos) + 1
                except: # Si salta error probamos el siguiente tipo
                    i += 1
            if i == len(formatos):
                if linea != 0: # Si no es la primera ocurrencia:
                    fecha_linea = fechas[-1]
                else:
                    fecha_linea = datetime.strptime('01/01/2015', '%d/%m/%Y')

        formatos_hora = ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M %p', '%d/%m/%Y %HH %MM %SS']
        if fecha_linea.strftime('%H:%M:%S') == '00:00:00':
            fecha_str = fecha_linea.strftime('%d/%m/%Y')
            fecha_y_hora = fecha_str + ' ' + hora
            i = 0
            while i < len(formatos_hora):
                try: # Si no salta error ya hemos encontrado el formato correcto
                    fecha_linea = datetime.strptime(fecha_y_hora, formatos_hora[i])
                    i = len(formatos_hora) + 1
                except: # Si salta error probamos el siguiente tipo
                    i += 1
            if i == len(formatos_hora):
                if fecha_linea.strftime('%d/%m/%Y') == fecha_str:
                    fecha_linea = fechas[-1]
                else:
                    fecha_linea = datetime.strptime(fecha_str + ' 11:30:00', '%d/%m/%Y %H:%M:%S')

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
    for i in range(1, 52):
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


def Extract():
    order_details = pd.read_csv('order_details.csv', encoding='latin_1', sep=';')
    analizar_calidad_de_datos(order_details, 'order_details')
    orders = pd.read_csv('orders.csv', encoding='latin_1', sep=';')
    analizar_calidad_de_datos(orders, 'orders')
    pizza_types = pd.read_csv('pizza_types.csv', encoding='latin_1')
    analizar_calidad_de_datos(pizza_types, 'pizza_types')

    return order_details, orders, pizza_types


def Transform(order_details, orders, pizza_types):
    order_details_ordenado, orders_ordenado = ordenar_dataframes(order_details, orders)
    order_details_ordenado['quantity'].fillna(value=1, inplace=True)
    order_details_ordenado['pizza_id'].fillna(value='empty_order_v', inplace=True)
    date_order_details = fusionar_dataframes(order_details_ordenado, orders_ordenado)
    date_order_details = date_order_details[date_order_details['pizza_type_id'].notna()]
    date_order_details = (date_order_details.reset_index()).drop(columns=['index'])

    print(date_order_details)

    pizza_types_dict = pizzas_type_df_a_dict(pizza_types)
    ingredientes = que_ingredientes_hay(pizza_types)
    df_ingredientes = pd.DataFrame(columns=ingredientes)

    df_ingredientes = analizar_ingredientes_por_semana(date_order_details, df_ingredientes, pizza_types_dict)
    df_ingredientes = df_ingredientes.fillna(0)
    lista_de_la_compra = df_ingredientes.median().round(0).astype(int)
    lista_de_la_compra = pd.DataFrame(lista_de_la_compra).reset_index()
    lista_de_la_compra.columns = ['Ingredient', 'Quantity']

    return lista_de_la_compra


def Load(lista_de_la_compra):

    RED = "\033[3;31m"
    YELLOW = "\033[5;33m"
    END = "\033[m"

    print(RED + '\nEn este programa vamos a asumir que acabamos de acabar la semana 51 de 2016')
    print('y queremos comprar los ingredientes de la semana que viene, la semana 52.\n' + END)

    print(YELLOW + 'Tras analizar el dataset proporcionado, hemos deducido que hay que comprar')
    print('los siguientes ingredientes:' + END)

    print(lista_de_la_compra)
    
    lista_de_la_compra.to_csv('lista_de_la_compra_2016.csv', sep=';')
    return 




if __name__ == '__main__':
    order_details, orders, pizza_types = Extract()
    lista_de_la_compra = Transform(order_details, orders, pizza_types)
    Load(lista_de_la_compra)