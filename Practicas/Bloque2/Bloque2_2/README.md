# Bloque 2 Practica 2
## Enunciado
Pizzerias Maven ha actualizado sus orders a 2016 le gustaría volver a saber saber que stock de ingredientes deberían comprar a la semana,
para optimizar el stock de ingredientes y las compras de estos en función del nuevo dataset.

### Entrega
Dirección de github con al menos el siguiente contenido.
- Informe de calidad de los datos, reflejando la tipología de cada columna y el numero de NaN y Null por cada columna
- ETL para transformar los datos en función de los requerimientos decididos por cada uno a la hora de realizar data wrangling, si es necesario
- ETL que saque como output un csv con la compra semanal de ingredientes
- Opcional: Todo lo necesario para desplegar esto a través de docker y Airflow.
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
- fichero python **crear_lista_de_la_compra_2016.py** que contiene el código del programa desarrollado para analizar los datos dados para buscar una predicción adecuada de los ingredientes
  de la semana que viene.
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero crear_lista_de_la_compra_2015.py
- fichero csv **order_details.csv** que contiene los datos descritos anteriormente
- fichero csv **orders.csv** que contiene los datos descritos anteriormente
- fichero csv **pizza_types.csv** que contiene los datos descritos anteriormente
- fichero csv **lista_de_la_compra_2016.csv** que contiene los ingredientes y sus respectivas cantidades que hay que comprar para la semana que viene
## Ejecución del fichero
#### Descargarse el dataset
Descargarlo desde este repositorio
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python crear_lista_de_la_compra_2016.py
Lo hacemos desde la terminal con el siguiente comando:

`python crear_lista_de_la_compra_2016.py`
#### Predicción en el fichero csv lista_de_la_compra_2016.csv
La predicción de los ingredientes que hay que comprar se guardará en un nuevo fichero. Este tendrá en la primera columna el nombre del ingrediente que hay que comprar
y en la segunda columna la cantidad.
