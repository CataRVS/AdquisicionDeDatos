from datetime import datetime
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns



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
    numero_semana = list()
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
        numero_semana.append(int((fecha_linea).strftime('%W')))
        dia_semana.append((fecha_linea).strftime('%A'))
        numero_mes.append((fecha_linea).strftime('%B'))
        horas.append(int((fecha_linea).strftime('%H')))


    date_order_details.pop('pizza_id')
    date_order_details.pop('quantity')
    date_order_details.insert(2, 'pizza_type_id', tipos_pizza, True)
    date_order_details.insert(3, 'pizza_size', tamano_pizzas, True)
    date_order_details['quantity'] = cantidades
    date_order_details['date'] = fechas
    date_order_details['week number'] = numero_semana
    date_order_details['week day'] = dia_semana
    date_order_details['month'] = numero_mes
    date_order_details['hour'] = horas
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


def analizar_ingredientes_por_semana(df, df_ingredientes, pizza_types_dict):
    for i in range(1, 52):
        df_semana = df[df['week number'] == i].reset_index()
        df_ingredientes = contar_y_guardar_ingredientes_semana(df_semana, df_ingredientes, pizza_types_dict)
    return df_ingredientes


def contar_ingredientes_pizzas_y_dibujar(pizza_types: pd.DataFrame, date_order_details: pd.DataFrame):
    pizza_types_dict = pizzas_type_df_a_dict(pizza_types)
    ingredientes = que_ingredientes_hay(pizza_types)
    df_ingredientes = pd.DataFrame(columns=ingredientes)

    df_ingredientes = analizar_ingredientes_por_semana(date_order_details, df_ingredientes, pizza_types_dict)
    df_ingredientes = df_ingredientes.fillna(0)
    df_tot_ingredientes = df_ingredientes.sum()
    df_tot_ingredientes = pd.DataFrame(df_tot_ingredientes).reset_index()
    df_tot_ingredientes.columns = ['Ingredient', 'Quantity']

    sns.set_style("whitegrid")
    sns.catplot(y="Ingredient", x="Quantity", kind='bar', data=df_tot_ingredientes, orient='h', height=10, aspect=0.75)
    plt.title('Cantidad de ingredientes usados en 2016'.upper(),fontweight="bold")
    plt.xlabel('Cantidad usada', fontweight="bold")
    plt.ylabel('Ingrediente', fontweight="bold")
    plt.savefig('ingredientes_usados.png', bbox_inches='tight')

    return df_tot_ingredientes


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

    plt.figure(figsize=(13, 7))
    plt.title('Cantidad de pizzas vendidas por tipo en 2016'.upper(),fontweight="bold")
    sns.barplot(x=df_tot['pizzas'], y=df_tot['cantidad'])
    plt.xlabel('Tipo de pizza', fontweight="bold")
    plt.ylabel('Pizzas vendidas', fontweight="bold")
    plt.xticks(rotation=45)
    plt.savefig('ventas_por_tipo.png', bbox_inches='tight')

    return df_tot


def contar_tamanos_pizzas(df_contar: pd.DataFrame) -> pd.DataFrame:
    '''
    Creamos un diccionario con clave el nombre de las pizzas y con valor la cantidad de pizzas inicializado a 0
    '''
    lista_pizzas_tamanos = ['s', 'm', 'l', 'xl', 'xxl']
    cuantas_pizzas_de_cada = list()
    df_tot = pd.DataFrame()
    for tamano in lista_pizzas_tamanos:
        df_pizza = df_contar[df_contar['pizza_size'] == tamano]
        cuantas_pizzas = int(df_pizza['quantity'].sum())
        cuantas_pizzas_de_cada.append(cuantas_pizzas)

    df_tot['tamanos'] = lista_pizzas_tamanos
    df_tot['cantidad'] = cuantas_pizzas_de_cada

    plt.figure(figsize=(13, 7))
    plt.title('Cantidad de pizzas vendidas por tamaño en 2016'.upper(),fontweight="bold")
    sns.barplot(x=df_tot['tamanos'], y=df_tot['cantidad'])
    plt.xlabel('Tamaño de la pizza', fontweight="bold")
    plt.ylabel('Pizzas vendidas', fontweight="bold")
    plt.savefig('ventas_por_tamano.png', bbox_inches='tight')

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
    plt.figure(figsize=(13, 7))
    plt.title('Cantidad de pizzas vendidas por dia de la semana en 2016'.upper(),fontweight="bold")
    sns.barplot(x=df_dias_semana['dia semana'], y=df_dias_semana['cantidad'])
    plt.xlabel('Dia de la semana', fontweight="bold")
    plt.ylabel('Pizzas vendidas', fontweight="bold")
    plt.savefig('ventas_por_dia_semana.png', bbox_inches='tight')
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
    plt.figure(figsize=(13, 7))
    plt.title('Cantidad de pizzas vendidas por mes en 2016'.upper(),fontweight="bold")
    sns.barplot(x=df_meses['mes'], y=df_meses['cantidad'])
    plt.xlabel('Mes', fontweight="bold")
    plt.ylabel('Pizzas vendidas', fontweight="bold")
    plt.savefig('ventas_por_mes.png', bbox_inches='tight')
    return df_meses


def separar_por_hora(date_order_details):
    cantidad_horas = list()
    for i in range(24):
        df_hora = date_order_details[date_order_details['hour'] == i]
        cantidad_horas.append(int(df_hora['quantity'].sum()))
    df_horas = pd.DataFrame()
    df_horas['hora'] = [i for i in range(24)]
    df_horas['cantidad'] = cantidad_horas
    plt.figure(figsize=(13, 7))
    plt.title('Cantidad de pizzas vendidas por hora en 2016'.upper(),fontweight="bold")
    sns.barplot(x=df_horas['hora'], y=df_horas['cantidad'])
    plt.xlabel('Hora', fontweight="bold")
    plt.ylabel('Pizzas vendidas', fontweight="bold")
    plt.savefig('ventas_por_hora.png', bbox_inches='tight')
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
    ventas_dia_semana = separar_por_dia_semana(date_order_details)
    ventas_mes = separar_por_mes(date_order_details)
    ventas_hora = separar_por_hora(date_order_details)
    ingredientes_usados = contar_ingredientes_pizzas_y_dibujar(pizza_types, date_order_details)
    ventas_tipos_pizza = contar_tipos_pizzas(pizza_types, date_order_details)
    ventas_tamanos_pizza = contar_tamanos_pizzas(date_order_details)
    return ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza