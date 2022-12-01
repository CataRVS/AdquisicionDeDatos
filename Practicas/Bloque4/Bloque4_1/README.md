# Bloque 4 Practica 1
## Enunciado
Generar un reporte ejecutivo para el COO de Maven Pizzas en formato pdf (para ello aprovechar el trabajo previo realizado en el bloque 3).

## Dataset proporcionado
#### Tamaño del dataset
3 csv:
- order_details.csv -> 48620 rows x 4 columns
- orders.csv -> 21350 rows x 3 columns
- pizza_types.csv -> 32 rows x 4 columns

#### Contenido del dataset
- order_details - has 48620 rows containing order details regarding pizza type and order quantity.
- orders - records the datetime indicators of the 21350 orders.
- pizza_types - specifies the category, ingredients information about the 32 different pizza types offered by the pizza place.
## Contenido de la carpeta
- fichero python **Analizar_datos_2016.py** que contiene el código del programa desarrollado para analizar los datos dados, creando tablas y gráficos que usaremos en el programa pdf_crear_reporte_ejecutivo.py
  de la semana que viene.
- fichero python **pdf_crear_reporte_ejecutivo.py** que contiene el código del programa desarollado para crear un informe ejecutivo sobre las ventas de 2016 a partir de la informacio proporcionada por el programa Analizar_datos_2016.py
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución de los fichero Analizar_datos_2016.py y pdf_crear_reporte_ejecutivo.py
- fichero csv **order_details.csv** que contiene los datos descritos anteriormente
- fichero csv **orders.csv** que contiene los datos descritos anteriormente
- fichero csv **pizza_types.csv** que contiene los datos descritos anteriormente
- documento pdf **Reporte_Ejecutivo_COO.pdf** que contiene el reporte ejecutivo producido por el fichero pdf_crear_reporte_ejecutivo.py
- imagen png **pizza.png** que contiene una imagen en formato png para la portada del pdf
- imagen png **ingredientes_usados.png** que contiene un gráfico con los ingredientes y las cantidades usadas en todo el año
- imagen png **ventas_por_dia_semana.png** que contiene un gráfico con las ventas por día de la semana en 2016.
- imagen png **ventas_por_hora.png** que contiene un gráfico con las ventas por hora en 2016.
- imagen png **ventas_por_mes.png** que contiene un gráfico con las ventas por mes en 2016.
- imagen png **ventas_por_tamano.png** que contiene un gráfico con las ventas por tamaño de la pizza en 2016.
- imagen png **ventas_por_tipo.png** que contiene un gráfico con las ventas por tipo de pizza en 2016.
## Ejecución del fichero
#### Descargarse el dataset
Descargarlo desde este repositorio
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python pdf_crear_reporte_ejecutivo.py
Lo hacemos desde la terminal con el siguiente comando:

`python pdf_crear_reporte_ejecutivo.py`
#### Reporte ejecutivo en el documento Reporte_Ejecutivo_COO.pdf
El reporte ejecutivo contiene datos sobre las horas, los días de la semana y los meses en los que más y menos pizzas se venden, los ingredientes más y menos usados y los tipos y tamaños de pizzas más y menos vendidos.
