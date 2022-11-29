# Bloque 1 Práctica 1
## Enunciado
Hacer un buscador de leaks en commits de github, para ello hay que usar pandas y expresiones regulares además del arquetipo que hemos trabajado en clase.
Como optativo, montarlo todo en una imagen docker y hacer una barra de progreso para ver que esta haciendo nuestra ETL.
## Repositorios de búsqueda de leaks proporcionados
- https://github.com/skalenetwork/skale-manager.git --> rama develop
- https://github.com/cornershop/django-redis.git --> rama master
## Contenido de la carpeta
- fichero python **buscador_leaks.py** que contiene el código del programa desarrollado para buscar los leaks en los commits de los repositorios skale-manager y django-redis
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero buscador_leaks.py
- carpeta **skale-manager** que contiene el contenido del repositorio https://github.com/skalenetwork/skale-manager.git
- carpeta **django-redis** que contiene el contenido del repositorio https://github.com/cornershop/django-redis.git
## Ejecución del fichero
#### Clonar los repositorios skale-manager y django-redis
Lo hacemos desde la terminal con los siguientes comandos:

`git clone https://github.com/skalenetwork/skale-manager.git`

`git clone https://github.com/cornershop/django-redis.git`
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Ejecutar el fichero de python buscador_leaks.py
Lo hacemos desde la terminal con el siguiente comando:

`python buscador_leaks.py`
