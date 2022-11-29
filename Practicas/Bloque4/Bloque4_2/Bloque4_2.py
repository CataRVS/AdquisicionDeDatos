# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 4.
Practica 1.

Generar un reporte ejecutivo para el COO de Maven Pizzas en formato pdf
(para ello aprovechar el trabajo previo realizado en el bloque 3).
'''

import Analizar_datos_2016
import xlsxwriter
import pandas as pd
from xlsxwriter.utility import xl_rowcol_to_cell



def escribir_tabla_y_grafico(excel, worksheet, df: pd.DataFrame, nombre_hoja, eje_x):
    columnas = list(df.columns)
    titulo_celda = excel.add_format({'bold': True, 'border': 1})
    celda_verde = excel.add_format({'font_color':'28B463', 'border': 1})
    celda_roja = excel.add_format({'font_color':'DF1616', 'border': 1})
    celda_azul = excel.add_format({'font_color':'16B1DF', 'border': 1})
    media = df[columnas[1]].mean()

    worksheet.write(4, 1, columnas[0], titulo_celda)
    worksheet.write(4, 2, columnas[1], titulo_celda)
    for j in range(len(df)):
        if df.loc[j, columnas[1]] > media:
            worksheet.write(j+5, 1, df.loc[j, columnas[0]], celda_verde)
            worksheet.write(j+5, 2, df.loc[j, columnas[1]], celda_verde)
        elif df.loc[j, columnas[1]] < media:
            worksheet.write(j+5, 1, df.loc[j, columnas[0]], celda_roja)
            worksheet.write(j+5, 2, df.loc[j, columnas[1]], celda_roja)
        else:
            worksheet.write(j+5, 1, df.loc[j, columnas[0]], celda_azul)
            worksheet.write(j+5, 2, df.loc[j, columnas[1]], celda_azul)
    worksheet.autofilter(f'{xl_rowcol_to_cell(4,1)}:{xl_rowcol_to_cell(4, 2)}')

    chart = excel.add_chart({'type': 'column'})
    chart.set_size({'width': 720, 'height': 576})
    chart.set_x_axis({'name': eje_x})
    chart.set_y_axis({'name': 'Nº de ventas'})

    chart.add_series({
    'categories': f'={nombre_hoja}!$B$6:$B${j+6}',
    'values':     f'={nombre_hoja}!$C$6:$C${j+6}'})
    chart.set_legend({'none': True})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('E6', chart)
    return worksheet


def hoja(excel: xlsxwriter.Workbook, ventas_tipos_pizza: pd.DataFrame, nombre_hoja, titulo, eje_x):
    worksheet = excel.add_worksheet(nombre_hoja)
    worksheet.merge_range(0, 0, 0, 2, 'Catalina Royo-Villanova Seguí')
    titulo1 = excel.add_format({'bold': True, 'font_size':20, 'font_color':'red', 'align':'center', 'border': 5})
    worksheet.merge_range(1, 1, 1, 9, "Reporte Evecutivo Ventas Maven's Pizza".upper(), titulo1)
    titulo2 = excel.add_format({'bold': True, 'font_size':16, 'font_color':'blue', 'align':'center', 'border': 2})
    worksheet.merge_range(2, 1, 2, 9, titulo, titulo2)
    worksheet = escribir_tabla_y_grafico(excel, worksheet, ventas_tipos_pizza, nombre_hoja, eje_x)
    return excel


def escribir_excel(ventas_tipos_pizza, ventas_dia_semana, ventas_mes, ventas_hora):
    excel = xlsxwriter.Workbook('Reporte_Ejecutivo_COO.xlsx')
    excel = hoja(excel, ventas_hora, 'horas', 'Pizzas vendidas por hora', 'Hora')
    excel = hoja(excel, ventas_dia_semana, 'días_semana', 'Pizzas vendidas por día de la semana', 'Día de la semana')
    excel = hoja(excel, ventas_mes, 'meses', 'Pizzas vendidas por mes', 'Mes')
    excel = hoja(excel, ventas_tipos_pizza, 'tipos_de_pizza', "Tipos de pizzas más y menos vendidos", 'Tipos')
    excel.close()



if __name__ == '__main__':
    nombres = ['order_details', 'orders', 'pizza_types']
    separadores = [';', ';', ',']
    order_details, orders, pizza_types = Analizar_datos_2016.Extract(nombres, separadores)
    date_order_details = Analizar_datos_2016.Transform(order_details, orders)
    ventas_tipos_pizza, ventas_dia_semana, ventas_mes, ventas_hora = Analizar_datos_2016.Load(pizza_types, date_order_details)
    escribir_excel(ventas_tipos_pizza, ventas_dia_semana, ventas_mes, ventas_hora)