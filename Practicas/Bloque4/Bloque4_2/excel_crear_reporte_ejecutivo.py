# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 4.
Practica 2.

Generar un fichero excel con un reporte ejecutivo, un reporte de ingredientes, un reporte de pedidos
(uno por cada hoja en el fichero de excel) para el dataset de Maven Pizzas trabajado en el bloque 3.
'''

import Analizar_datos_2016
import xlsxwriter
import pandas as pd
from xlsxwriter.utility import xl_rowcol_to_cell



def escribir_tabla_y_grafico(excel, worksheet, df: pd.DataFrame, nombre_hoja, eje_x, titulo, fila):
    titulo2 = excel.add_format({'bold': True, 'font_size':16, 'font_color':'blue', 'align':'center', 'border': 2})
    worksheet.merge_range(fila+2, 1, fila+2, 14, titulo, titulo2)
    columnas = list(df.columns)
    titulo_celda = excel.add_format({'bold': True, 'border': 1})
    celda_verde = excel.add_format({'font_color':'28B463', 'border': 1})
    celda_roja = excel.add_format({'font_color':'DF1616', 'border': 1})
    celda_azul = excel.add_format({'font_color':'16B1DF', 'border': 1})
    media = df[columnas[1]].mean()

    worksheet.write(fila+4, 1, columnas[0], titulo_celda)
    worksheet.write(fila+4, 2, columnas[1], titulo_celda)
    for j in range(len(df)):
        if df.loc[j, columnas[1]] > media:
            worksheet.write(fila+j+5, 1, df.loc[j, columnas[0]], celda_verde)
            worksheet.write(fila+j+5, 2, df.loc[j, columnas[1]], celda_verde)
        elif df.loc[j, columnas[1]] < media:
            worksheet.write(fila+j+5, 1, df.loc[j, columnas[0]], celda_roja)
            worksheet.write(fila+j+5, 2, df.loc[j, columnas[1]], celda_roja)
        else:
            worksheet.write(fila+j+5, 1, df.loc[j, columnas[0]], celda_azul)
            worksheet.write(fila+j+5, 2, df.loc[j, columnas[1]], celda_azul)

    chart = excel.add_chart({'type': 'column'})
    chart.set_size({'width': 705, 'height': 580})
    chart.set_x_axis({'name': eje_x})
    chart.set_y_axis({'name': 'Nº de ventas'})

    chart.add_series({
    'categories': f'={nombre_hoja}!$B${fila+6}:$B${fila+j+6}',
    'values':     f'={nombre_hoja}!$C${fila+6}:$C${fila+j+6}'})
    chart.set_legend({'none': True})

    # Insert the chart into the worksheet.
    worksheet.insert_chart(f'{xl_rowcol_to_cell(fila + 4 ,4)}', chart)
    if j < 30:
        fila += 33
    else:
        fila += j + 6
    return worksheet, fila

def hoja1(excel: xlsxwriter.Workbook, ventas_hora: pd.DataFrame, ventas_dia_semana: pd.DataFrame, ventas_mes: pd.DataFrame):
    worksheet = excel.add_worksheet('reporte_ejecutivo_ventas')
    worksheet.merge_range(0, 0, 0, 2, 'Catalina Royo-Villanova Seguí')
    titulo1 = excel.add_format({'bold': True, 'font_size':20, 'font_color':'red', 'align':'center', 'border': 5})
    worksheet.merge_range(1, 1, 1, 14, "Reporte Ejecutivo Ventas de Maven's Pizza".upper(), titulo1)
    worksheet, fila = escribir_tabla_y_grafico(excel, worksheet, ventas_hora, 'reporte_ejecutivo_ventas', 'Horas', 'Pizzas vendidas por hora', 0)
    worksheet, fila = escribir_tabla_y_grafico(excel, worksheet, ventas_dia_semana, 'reporte_ejecutivo_ventas', 'Día de la semana', 'Pizzas vendidas por día de la semana', fila)
    worksheet, fila = escribir_tabla_y_grafico(excel, worksheet, ventas_mes, 'reporte_ejecutivo_ventas', 'Año', 'Pizzas vendidas por mes', fila)
    return excel


def hoja2(excel: xlsxwriter.Workbook, ingredientes_usados: pd.DataFrame):
    worksheet = excel.add_worksheet('reporte_de_ingredientes')
    worksheet.merge_range(0, 0, 0, 2, 'Catalina Royo-Villanova Seguí')
    titulo1 = excel.add_format({'bold': True, 'font_size':20, 'font_color':'red', 'align':'center', 'border': 5})
    worksheet.merge_range(1, 1, 1, 14, "Reporte de Ingredientes de Maven's Pizza".upper(), titulo1)
    titulo2 = excel.add_format({'bold': True, 'font_size':16, 'font_color':'blue', 'align':'center', 'border': 2})
    worksheet.merge_range(2, 1, 2, 14, 'Ingredientes más y menos usados', titulo2)
    columnas = list(ingredientes_usados.columns)
    titulo_celda = excel.add_format({'bold': True, 'border': 1})
    celda_verde = excel.add_format({'font_color':'28B463', 'border': 1})
    celda_roja = excel.add_format({'font_color':'DF1616', 'border': 1})
    celda_azul = excel.add_format({'font_color':'16B1DF', 'border': 1})
    media = ingredientes_usados[columnas[1]].mean()

    worksheet.write(4, 1, columnas[0], titulo_celda)
    worksheet.write(4, 2, columnas[1], titulo_celda)
    for j in range(len(ingredientes_usados)):
        if ingredientes_usados.loc[j, columnas[1]] > media:
            worksheet.write(j+5, 1, ingredientes_usados.loc[j, columnas[0]], celda_verde)
            worksheet.write(j+5, 2, ingredientes_usados.loc[j, columnas[1]], celda_verde)
        elif ingredientes_usados.loc[j, columnas[1]] < media:
            worksheet.write(j+5, 1, ingredientes_usados.loc[j, columnas[0]], celda_roja)
            worksheet.write(j+5, 2, ingredientes_usados.loc[j, columnas[1]], celda_roja)
        else:
            worksheet.write(j+5, 1, ingredientes_usados.loc[j, columnas[0]], celda_azul)
            worksheet.write(j+5, 2, ingredientes_usados.loc[j, columnas[1]], celda_azul)

    worksheet.merge_range(4, 4, 69, 14, '', celda_verde)
    worksheet.insert_image('E5', 'ingredientes_usados.png', {'x_scale': 0.99, 'y_scale': 1.38, 'x_offset': 1, 'y_offset': 1})
    return excel


def hoja3(excel: xlsxwriter.Workbook, ventas_tipos_pizza: pd.DataFrame, ventas_tamanos_pizza: pd.DataFrame):
    worksheet = excel.add_worksheet('reporte_de_pedidos')
    worksheet.merge_range(0, 0, 0, 2, 'Catalina Royo-Villanova Seguí')
    titulo1 = excel.add_format({'bold': True, 'font_size':20, 'font_color':'red', 'align':'center', 'border': 5})
    worksheet.merge_range(1, 1, 1, 14, "Reporte de Pedidos de Maven's Pizza".upper(), titulo1)
    worksheet, fila = escribir_tabla_y_grafico(excel, worksheet, ventas_tipos_pizza, 'reporte_de_pedidos', 'tipos', "Tipos de pizzas más y menos vendidos", 0)
    worksheet, fila = escribir_tabla_y_grafico(excel, worksheet, ventas_tamanos_pizza, 'reporte_de_pedidos', 'tamaños', "Tamaños de pizzas más y menos vendidos", fila)
    return excel


def escribir_excel(ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza):
    excel = xlsxwriter.Workbook('Reporte_Mavens_pizza.xlsx')
    excel = hoja1(excel, ventas_hora, ventas_dia_semana, ventas_mes)
    excel = hoja2(excel, ingredientes_usados)
    excel = hoja3(excel, ventas_tipos_pizza, ventas_tamanos_pizza)
    excel.close()



if __name__ == '__main__':
    nombres = ['order_details', 'orders', 'pizza_types']
    separadores = [';', ';', ',']
    order_details, orders, pizza_types = Analizar_datos_2016.Extract(nombres, separadores)
    date_order_details = Analizar_datos_2016.Transform(order_details, orders)
    ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza = Analizar_datos_2016.Load(pizza_types, date_order_details)
    escribir_excel(ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza)