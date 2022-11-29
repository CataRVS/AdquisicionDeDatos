from datetime import datetime
import pandas as pd
import numpy as np
import re



def ordenar_dataframes(order_details: pd.DataFrame, orders: pd.DataFrame):
    '''
    Ordenamos los dataframes por orden de pedido, asi ordenamos tambien las fechas.
    '''
    order_details_ordenado = order_details.sort_values('order_details_id', ascending=True)
    orders_ordenado = orders.sort_values('order_id', ascending=True)
    order_details_ordenado = (order_details_ordenado.reset_index()).drop(columns=['index'])
    orders_ordenado = (orders_ordenado.reset_index()).drop(columns=['index'])
    return order_details_ordenado, orders_ordenado


def fusionar_dataframes(order_details: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    '''
    Añadimos al dataframe order_details la fecha, el dia de la semana, y el mes en el que se ha reaizado el encargo
    '''
    date_order_details = order_details.copy()
    
    tipos_pizza = list()
    tamano_pizzas = list()
    fechas = list()
    dia_semana = list()
    numero_mes = list()
    horas = list()
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

        formatos_fecha = ['%B %d %Y', '%b %d %Y', '%Y-%m-%d', '%d-%m-%y %H:%M:%S', '%A,%d %B, %Y', '%a %d-%b-%Y']

        try: # Si salta un error es que no es un epoch_time
            fecha_sin_hora = float(fecha_sin_hora)
            fecha_linea = datetime.fromtimestamp(int(fecha_sin_hora))
        except ValueError:
            i = 0
            while i < len(formatos_fecha):
                try: # Si no salta eeror ya hemos encontrado el formato correcto
                    fecha_linea = datetime.strptime(fecha_sin_hora, formatos_fecha[i])
                    i = len(formatos_fecha) + 1
                except: # Si salta error probamos el siguiente tipo
                    i += 1
            if i == len(formatos_fecha):
                if linea != 0: # Si no es la primera ocurrencia:
                    fecha_linea = fechas[-1]
                else:
                    fecha_linea = datetime.strptime('01/01/2016', '%d/%m/%Y')


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
        dia_semana.append((fecha_linea).strftime('%A'))
        numero_mes.append((fecha_linea).strftime('%B'))
        horas.append(int((fecha_linea).strftime('%H')))


    date_order_details.pop('pizza_id')
    date_order_details.pop('quantity')
    date_order_details.insert(2, 'pizza_type_id', tipos_pizza, True)
    date_order_details.insert(3, 'pizza_size', tamano_pizzas, True)
    date_order_details['quantity'] = cantidades
    date_order_details['date'] = fechas
    date_order_details['week day'] = dia_semana
    date_order_details['month'] = numero_mes
    date_order_details['hour'] = horas
    return date_order_details


def contar_tipos_pizzas(pizza_types: pd.DataFrame, df_contar: pd.DataFrame) -> pd.DataFrame:
    '''
    Creamos un diccionario con clave el nombre de las pizzas y con valor la cantidad de pizzas inicializado a 0
    '''
    lista_pizzas = list()
    df_tot = pd.DataFrame()
    for i in range(len(pizza_types)):
        lista_pizzas.append(pizza_types.loc[i, 'pizza_type_id'])
    cuantas_pizzas_de_cada = list()
    for pizza in lista_pizzas:
        df_pizza = df_contar[df_contar['pizza_type_id'] == pizza]
        cuantas_pizzas = int(df_pizza['quantity'].sum())
        cuantas_pizzas_de_cada.append(cuantas_pizzas)

    df_tot['pizzas'] = lista_pizzas
    df_tot['cantidad'] = cuantas_pizzas_de_cada

    df_tot = df_tot.sort_values('cantidad', ascending=False)
    df_tot = (df_tot.reset_index()).drop(columns=['index'])

    return df_tot


def separar_por_dia_semana(date_order_details):
    dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cantidad_dias = list()
    for dia in dias:
        df_dia = date_order_details[date_order_details['week day'] == dia]
        cantidad_dias.append(int(df_dia['quantity'].sum()))
    df_dias_semana = pd.DataFrame()
    df_dias_semana['dia semana'] = dias
    df_dias_semana['cantidad'] = cantidad_dias
    return df_dias_semana
    

def separar_por_mes(date_order_details):
    meses = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    cantidad_meses = list()
    for mes in meses:
        df_mes = date_order_details[date_order_details['month'] == mes]
        cantidad_meses.append(int(df_mes['quantity'].sum()))
    df_meses = pd.DataFrame()
    df_meses['mes'] = meses
    df_meses['cantidad'] = cantidad_meses
    return df_meses


def separar_por_hora(date_order_details):
    cantidad_horas = list()
    for i in range(24):
        df_hora = date_order_details[date_order_details['hour'] == i]
        cantidad_horas.append(int(df_hora['quantity'].sum()))
    df_horas = pd.DataFrame()
    df_horas['hora'] = [i for i in range(24)]
    df_horas['cantidad'] = cantidad_horas
    return df_horas


def Extract(nombres, separadores):
    dataframes = list()
    for i in range(len(nombres)):
        dataframe = pd.read_csv(nombres[i]+'.csv', encoding='latin_1', sep=separadores[i])
        dataframes.append(dataframe)

    return dataframes[0], dataframes[1], dataframes[2]


def Transform(order_details, orders):
    order_details_ordenado, orders_ordenado = ordenar_dataframes(order_details, orders)
    order_details_ordenado['quantity'].fillna(value=1, inplace=True)
    order_details_ordenado['pizza_id'].fillna(value='empty_order_v', inplace=True)
    date_order_details = fusionar_dataframes(order_details_ordenado, orders_ordenado)
    date_order_details = date_order_details[date_order_details['pizza_type_id'].notna()]
    date_order_details = (date_order_details.reset_index()).drop(columns=['index'])

    return date_order_details


def Load(pizza_types, date_order_details):

    ventas_tipos_pizza = contar_tipos_pizzas(pizza_types, date_order_details)
    ventas_dia_semana = separar_por_dia_semana(date_order_details)
    ventas_mes = separar_por_mes(date_order_details)
    ventas_hora = separar_por_hora(date_order_details)
    return ventas_tipos_pizza, ventas_dia_semana, ventas_mes, ventas_hora