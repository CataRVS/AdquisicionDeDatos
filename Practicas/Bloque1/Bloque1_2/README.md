# Bloque 1 Practica 2
## Enunciado
Hacer un recomendador de uno de los topics que elijáis, películas, música, series... (Extraer dataset de www.kaggle.com).
Para ello tendréis que elegir un dataset en formato csv y montar este proceso a través de una ETL que os extraiga la información del csv elegido
y mediante el uso de expresiones regulares os devuelva al menos por pantalla la recomendación propuesta sobre un input dado.
Opcional: Esta ETL será desplegada a traves de un orquestador como puede ser Dagster o Airflow.
## Dataset de kaggle utilizado
<ins>Title:</ins> Netflix TV Series Dataset

<ins>Link:</ins> https://www.kaggle.com/datasets/harshitshankhdhar/netflix-and-amazon-prime-tv-series-dataset
#### Tamaño del dataset
5 columns x 641 rows
#### Contenido del dataset
- Title -> Name of the Series.
- Genre -> Genre of the series.
- Premiere -> Released Year
- No_of_Seasons -> Total number of Seasons
- No_of_Episodes -> Total number of Episodes.
## Contenido de la carpeta
- fichero python **recomendador.py** que contiene el código del programa desarrollado para buscar recomendaciones de series en funcion del género introducido
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero recomendador.py
- fichero csv **tv_shows_data.csv** que contiene los datos sobre las series de Netflix y Amazon Prime descritos anteriormente
## Ejecución del fichero
#### Descargarse el dataset
Lo podemos hacer de dos manera:
- Descargarlo desde su link de kaggle: https://www.kaggle.com/datasets/harshitshankhdhar/netflix-and-amazon-prime-tv-series-dataset
- Descargarlo desde este repositorio
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python recomendador.py
Lo hacemos desde la terminal con el siguiente comando:

`python recomendador.py`
#### Seleccionar el género del que se desea recibir recomendaciones
Al ejecutar el archivo, se abre un input esperando la respuesta del género deseado.
