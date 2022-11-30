# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 4.
Practica 1.

Generar un reporte ejecutivo para el COO de Maven Pizzas en formato pdf
(para ello aprovechar el trabajo previo realizado en el bloque 3).
'''

from fpdf import FPDF
import pandas as pd
import Analizar_datos_2016

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("times", "I", 10)
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="R")


def crear_tabla(pdf: FPDF, df: pd.DataFrame) -> FPDF:
    ancho_pagina = pdf.w - 45
    filas = list(df.index)
    columnas = list(df.columns)
    n_col = len(columnas)
    ancho_columna = ancho_pagina / n_col + 2.5
    pdf.set_font('times', 'B', 11)
    pdf.ln(12)
    for columna in columnas:
        pdf.cell(ancho_columna, 5, str(columna), border=True, align='C')
    pdf.ln()
    pdf.set_font('times', '', 11)
    for fila in filas:
        if fila == 45:
            pdf.set_font('times', 'B', 11)
            for columna in columnas:
                pdf.cell(ancho_columna, 5, str(columna), border=True, align='C')
            pdf.ln()
            pdf.set_font('times', '', 11)
        for columna in columnas:
            texto = str(df.loc[fila, columna])
            pdf.cell(ancho_columna, 5, texto, border=True, align='C')
        pdf.ln()
    return pdf


def crear_portada(pdf: FPDF) -> FPDF:
    # Creamos la portada del PDF
    pdf.add_page()
    pdf.set_margin(20) # Queremos que el margen sea de 2 cm
    pdf.set_font('times', 'B', 30) # El titulo esta en negrita y con tamaño 30
    pdf.cell(0, 15, '')
    pdf.ln() # Pasamos a la siguiente linea
    pdf.multi_cell(0, 15, 'REPORTE EJECUTIVO\nVENTAS MAVEN PIZZAS', align='C') # El titulo esta centrado en la página

    # Queremos añadir una foto a la página
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 100)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('pizza.png', x= posicion_foto, w= 100) # Añadimos la imagen
    pdf.ln()

    pdf.set_font('times', '', 16) #Cambiamos el tipo de letra
    pdf.multi_cell(0, 10, 'ADQUISICIÓN DE DATOS\n Catalina Royo-Villanova Seguí', align='C')
    pdf.ln()

    return pdf


def indice(pdf: FPDF):
    pdf.add_page()
    # Descripcion
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Índice'.upper(), align='C')
    pdf.ln(15)
    # pdf.multi_cell(0, 5, 'En este informe veremos como han evolucionado las ventas a lo largo del año,' + 
    # ' que día de la semana y el mes se venden más pizzas, y finalmente, que pizzas se venden más y cuales se venden menos.', align='J')
    pdf.set_font('times', '', 16)
    pdf.cell(150, 10, ' '*10 + '1. Pizzas vendidas por hora.')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '3 ', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()
    pdf.cell(150, 10, ' '*10 + '2. Pizzas vendidas por día de la semana.')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '5 ', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()
    pdf.cell(150, 10, ' '*10 + '3. Pizzas vendidas por mes.')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '6 ', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()
    pdf.cell(150, 10, ' '*10 + '4. Tipos de pizzas más y menos vendidos')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '7 ', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()
    pdf.cell(150, 10, ' '*10 + '5. Tamaños de las pizzas más y menos vendidos')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '9 ', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()
    pdf.cell(150, 10, ' '*10 + '6. Ingredientes más y menos usados')
    pdf.set_font('times', 'I', 14)
    pdf.cell(20, 10, '10', align='R')
    pdf.set_font('times', '', 16)
    pdf.ln()

    return pdf


def pizzas_por_hora(pdf: FPDF, ventas_hora: pd.DataFrame,) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Pizzas vendidas por hora'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las ventas por hora de 2016.')
    pdf = crear_tabla(pdf, ventas_hora)
    pdf.add_page()
    pdf.set_font('times', '', 11)
    pdf.ln(10)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 170)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ventas_por_hora.png', x = posicion_foto, w =170) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, las horas a la que más pizzas se venden son las 12 y las 13, lo que tiene sentido ya que coincide con la hora de comer.')
    pdf.ln()
    pdf.multi_cell(0, 5, 'También podemos ver que las siguientes horas en las que más pizzas se venden son las 17 y 18, horas correspondientes a la hora de la cena.')
    
    return pdf


def pizzas_por_dia_semana(pdf: FPDF, ventas_dia_semana: pd.DataFrame,) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Pizzas vendidas por día de la semana'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las ventas por día de la semana de 2016.')
    pdf = crear_tabla(pdf, ventas_dia_semana)
    pdf.ln(10)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 170)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ventas_por_dia_semana.png', x = posicion_foto, w =170) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, los días de la semana en los que más pizzas se venden son los sabados y los domingos, es decir durante el fin de semana.')
    
    return pdf


def pizzas_por_mes(pdf: FPDF, ventas_mes: pd.DataFrame,) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Pizzas vendidas por mes'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las ventas por mes de 2016.')
    pdf = crear_tabla(pdf, ventas_mes)
    pdf.ln(10)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 170)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ventas_por_mes.png', x = posicion_foto, w =170) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, el mes en el que más pizzas se venden es julio, el primer mes del verano.')
    
    return pdf


def pizzas_mas_menos_vendidas(pdf: FPDF, ventas_tipos_pizza: pd.DataFrame) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Tipos de pizzas más y menos vendidos'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las ventas por tipo de pizza de 2016.')
    pdf = crear_tabla(pdf, ventas_tipos_pizza)
    pdf.add_page()
    pdf.set_font('times', '', 11)
    pdf.ln(10)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 170)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ventas_por_tipo.png', x = posicion_foto, w =170) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, las tres pizzas más vendidas son la bbq_ckn, la classic_dlx, la hawaiian y la pepperoni. Con aproximadamente 2150 ventas cada una en 2016.')
    pdf.ln()
    pdf.multi_cell(0, 5, 'En cambio, la pizza menos vendida, con 424 ventas en 2016, es brie_carre. Las otras dos pizzas con menos ventas son mediterraneo y spinach_supr.')
    return pdf


def tamanos_mas_menos_vendidos(pdf: FPDF, ventas_tamanos_pizza: pd.DataFrame) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Tamaños de las pizzas más y menos vendidos'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las ventas por tamaño de la pizza de 2016.')
    pdf = crear_tabla(pdf, ventas_tamanos_pizza)
    pdf.ln(10)
    pdf.set_font('times', '', 11)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 170)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ventas_por_tamano.png', x = posicion_foto, w =170) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, los tres tamaños más usados son, en orden, el grande, el mediano y el pequeño, con respectivamente 16727, 13802 y 12701 ventas cada uno.')
    pdf.ln()
    pdf.multi_cell(0, 5, 'En este gráfico se puede ver tambien que el tamaño extra grande y extra extra grande no estan muy demandados, especialmente este último con solamente 24 ventas en todo el año. El extra grande como podemos ver tiene 475 ventas.')
    return pdf


def ingredientes_mas_menos_usados(pdf: FPDF, ingredientes_usados: pd.DataFrame) -> FPDF:
    pdf.add_page()
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 'Ingredientes más y menos usados'.upper(), align='C')
    pdf.ln(15)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 10, 'Tabla con las cantidades de ingredientes usados en 2016.')
    pdf = crear_tabla(pdf, ingredientes_usados)
    pdf.add_page()
    pdf.set_font('times', '', 11)
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 160)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('ingredientes_usados.png', x = posicion_foto, w =160) # Añadimos la imagen
    # Comentamos la imagen
    pdf.ln(5)
    pdf.multi_cell(0, 5, 'Como podemos ver, los ingredientes más usados son el ajo (garlic) y el tomate (Tomatoes) con más de 50000 consumiciones en 2016.')
    pdf.ln()
    pdf.multi_cell(0, 5, 'En cambio, los ingredientes menos usados con Brie Carre Cheese, Prosciutto, Caramelized Onions, Pears, Thyme. Todos ellos con 418 consumiciones. Esto se debe a que solo se usan en la pizza Brie Carre, la menos vendida.')
    return pdf


def escribir_pdf(ventas_dia_semana: pd.DataFrame, ventas_mes: pd.DataFrame, ventas_hora: pd.DataFrame, ingredientes_usados: pd.DataFrame, ventas_tipos_pizza: pd.DataFrame, ventas_tamanos_pizza: pd.DataFrame):
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_margins(30, 25, 25)
    pdf.set_auto_page_break(True, 25)
    pdf = crear_portada(pdf)
    # Empezamos con el reporte
    pdf = indice(pdf)
    pdf = pizzas_por_hora(pdf, ventas_hora)
    pdf = pizzas_por_dia_semana(pdf, ventas_dia_semana)
    pdf = pizzas_por_mes(pdf, ventas_mes)
    pdf = pizzas_mas_menos_vendidas(pdf, ventas_tipos_pizza)
    pdf = tamanos_mas_menos_vendidos(pdf, ventas_tamanos_pizza)
    pdf = ingredientes_mas_menos_usados(pdf, ingredientes_usados)

    pdf.output('Reporte_Ejecutivo_COO.pdf')


if __name__ == '__main__':
    nombres = ['order_details', 'orders', 'pizza_types']
    separadores = [';', ';', ',']
    order_details, orders, pizza_types = Analizar_datos_2016.Extract(nombres, separadores)
    date_order_details = Analizar_datos_2016.Transform(order_details, orders)
    ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza = Analizar_datos_2016.Load(pizza_types, date_order_details)
    escribir_pdf(ventas_dia_semana, ventas_mes, ventas_hora, ingredientes_usados, ventas_tipos_pizza, ventas_tamanos_pizza)