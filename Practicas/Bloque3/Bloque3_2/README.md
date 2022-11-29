# Bloque 3 Practica 2
## Enunciado
Crear un archivo XML, donde se guarde el reporte de tipologia de datos de la practica de pizzas del bloque anterior y la recomendacion propuesta.

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
- fichero python **Bloque3_2.py** que contiene el código del programa desarrollado para analizar los datos dados,haciendo un análisis de calidad, y para buscar una
  predicción adecuada de los ingredientes de la semana que viene. Todo esto se guardará en el fichero xml lista_de_la_compra.xml
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero Bloque2_1.py
- fichero csv **order_details.csv** que contiene los datos descritos anteriormente
- fichero csv **orders.csv** que contiene los datos descritos anteriormente
- fichero csv **pizza_types.csv** que contiene los datos descritos anteriormente
- fichero csv **lista_de_la_compra.xml** que contiene el analisis de calidad de los datos y los ingredientes y sus respectivas cantidades que hay que comprar para
  la semana que viene
## Ejecución del fichero
#### Descargarse el dataset
Descargarlo desde este repositorio
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python Bloque2_2.py
Lo hacemos desde la terminal con el siguiente comando:

`python Bloque3_2.py`
#### Predicción en el fichero csv lista_de_la_compra.xml_2016.csv
El analisis de calidad de los datos y la predicción de los ingredientes que hay que comprar se guardará en un nuevo fichero xml. En xml esta el elemento raiz 'root'
y este tiene dos hijos 'infodatasets' donde esta guardado el analisis de los datos y 'contents' que guarda la prediccion de los ingredientes que hay que comprar la
semana que viene.
