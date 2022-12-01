# Bloque 3 Práctica 1
## Enunciado
Exportar los datos obtenidos en la practica de obtencion de leaks en commit de git a un fichero json.
## Repositorios de búsqueda de leaks proporcionados
- https://github.com/skalenetwork/skale-manager.git --> rama develop
- https://github.com/cornershop/django-redis.git --> rama master
## Contenido de la carpeta
- fichero python **json_buscador_leaks.py** que contiene el código del programa desarrollado para buscar los leaks en los commits de los repositorios skale-manager y django-redis y guardarlos en formato json
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero json_buscador_leaks.py
- carpeta **skale-manager** que contiene el contenido del repositorio https://github.com/skalenetwork/skale-manager.git
- carpeta **django-redis** que contiene el contenido del repositorio https://github.com/cornershop/django-redis.git
- fichero json **leaks_encontrados_repo_skale-manager.json** que contiene los leaks encontrados del repositorio skale-manager en formato json, se crea durante
 la ejecución del fichero json_buscador_leaks.py
- fichero json **leaks_encontrados_repo_django-redis.json** que contiene los leaks encontrados del repositorio django-redis en formato json, se crea durante
 la ejecución del fichero json_buscador_leaks.py
## Ejecución del fichero
#### Clonar los repositorios skale-manager y django-redis
Lo hacemos desde la terminal con los siguientes comandos:

`git clone https://github.com/skalenetwork/skale-manager.git`

`git clone https://github.com/cornershop/django-redis.git`
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python json_buscador_leaks.py
Lo hacemos desde la terminal con el siguiente comando:

`python json_buscador_leaks.py`

### Leaks encontrados en el repositorio skale-manager en el fichero leaks_encontrados_repo_skale-manager.json
Los leaks encontrados en el repositorio skale-manager se guardarán en un nuevo fichero. Tienen una lista de diccionarios y cada diccionario tiene como clave el commit con el leak y como valor el mensaje del commit.
### Leaks encontrados en el repositorio django-redis en el fichero leaks_encontrados_repo_django-redis.json
Los leaks encontrados en el repositorio django-redis se guardarán en un nuevo fichero. Tienen una lista de diccionarios y cada diccionario tiene como clave el commit con el leak y como valor el mensaje del commit.
