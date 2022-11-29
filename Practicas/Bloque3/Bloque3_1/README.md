# Bloque 3 Práctica 1
## Enunciado
Exportar los datos obtenidos en la practica de obtencion de leaks en commit de git a un fichero json.
## Repositorios de búsqueda de leaks proporcionados
- https://github.com/skalenetwork/skale-manager.git --> rama develop
- https://github.com/cornershop/django-redis.git --> rama master
## Contenido de la carpeta
- fichero python **Practica3_1.py** que contiene el código del programa desarrollado para buscar los leaks en los commits de los repositorios skale-manager y django-redis
  y guardarlos en formato json
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero Practica3_1.py
- carpeta **skale-manager** que contiene el contenido del repositorio https://github.com/skalenetwork/skale-manager.git
- carpeta **django-redis** que contiene el contenido del repositorio https://github.com/cornershop/django-redis.git
- fichero json **leaks_encontrados_repo_skale-manage.json** que contiene los leaks encontrados del repositorio skale-manager en formato json, se crea durante
 la ejecución del fichero Practica3_1.py
- fichero json **leaks_encontrados_repo_django-redis.json** que contiene los leaks encontrados del repositorio django-redis en formato json, se crea durante
 la ejecución del fichero Practica3_1.py
## Ejecución del fichero
#### Clonar los repositorios skale-manager y django-redis
Lo hacemos desde la terminal con los siguientes comandos:

`git clone https://github.com/skalenetwork/skale-manager.git`

`git clone https://github.com/cornershop/django-redis.git`
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python Practica3_1.py
Lo hacemos desde la terminal con el siguiente comando:

`python Practica3_1.py`
