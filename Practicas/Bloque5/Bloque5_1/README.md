# Bloque 5 Practica 1
## Enunciado
#### Api y web scraping: Senior data analyst de la NBA.

Como senior data analyst, uno de los GM (general manager) más innovadores de la NBA ha
decidido evaluar como se va a comportar su equipo durante los partidos de este año. Por
lo que necesitaría construir un analizador de las principales estadísticas del equipo
hasta el momento para la temporada 2022-2023 y un pronóstico para el próximo partido.
Para ello debes de disponer de una ETL que extraiga, transforme los datos y guarde un
informe de los puntos clave del equipo en cuestión en formato pdf y ofrezca por pantalla
la predicción para el próximo partido. Entregando el siguiente contenido en el repositorio
de datos:

- Código de una ETL que extraiga datos de una API de datos de la NBA, a continuación, se
  dejan un par de ejemplos de API:

  - https://www.api-basketball.com/
  - https://sportsdata.io/

- Además  una ETL que obtenga datos usando técnicas de web scraping donde se tendrá que
  elegir una fuente de datos para obtener pronósticos, como por ejemplo:

  - https://www.sportytrader.es/
  - https://www.solobasket.com/apuestas-deportivas/pronosticos-nba/
  - https://www.marca.com/baloncesto/nba/calendario.html

- El reporte en formato PDF, a continuación de dejan un par de ejemplos con posible contenido
  del reporte:

  - https://scores.nbcsports.com/nba/teamstats.asp?teamno=06&type=stats
  - https://espndeportes.espn.com/basquetbol/nba/equipo/estadisticas/_/nombre/dal/dallas-mavericks

- Fichero requirements.txt para la instalación de los recursos necesarios

- Fichero de config.txt para la configuración necesaria de las ETLs (como por ejemplo los
  credenciales usados para consumir las APIs, recordar no subir vuestras credenciales, solo
  el fichero con la estructura necesaria)

- README.md con la descripción general del repo y las instrucciones de uso.

Opcional: (este opcional aportara el 10% sobre la nota final de la práctica)

- Desplegar mediante Docker, importante: será necesario que el pdf se guarde en la instancia
  desde donde se lance la imagen no en el contenedor, además incluir instrucciones para consumir
  el pronóstico.

- Orquestar las pipelines para que se lancen automáticamente todos los días a las 15:00UTC.

## Contenido de la carpeta
- fichero python **analisis_equipos_NBA.py** que contiene el código del programa desarrollado para extraer los datos de la api y de la pagina web, tratarlos y exportarlos a un pdf.
- fichero de texto **requirements.txt** que contiene las librerias necesarias para la ejecución del fichero analisis_equipos_NBA.py.
- fichero de texto **config.txt** que contiene la clave necesaria para acceder a las APIs usadas.
- fichero json **Jornadas.json** que contiene un diccionario que tiene como clave las fechas y como valor la jornada que se desarrolla dicha fecha.
- fichero json **Jornadas_fechas.json** que contiene un diccionario que tiene como clave la jornada y como valor la fecha en la que esta tiene lugar.
- imagen png **NBA_logo_letras.png** que contiene una imagen en formato png para la portada del pdf.
- documento pdf **Minnesota_Timberwolves_01012023.pdf** que contiene un ejemplo de un reporte producido por el fichero analisis_equipos_NBA.py.
- archivo html **Web_calendario_NBA.html** que contiene los datos en bruto del calendario de la NBA de la página web del periódico [Marca](https://www.marca.com/baloncesto/nba/calendario.html).
  Este archivo se crea durante la ejecución del fichero analisis_equipos_NBA.py.
- imagen png **equipo.png** que contiene el logo del equipo analizado extraido de un link contenido en el archivo Web_calendario_NBA.html.
- imagen png **contrincante.png** que contiene el logo del contrincante del equipo analizado en el proximo partido extraido de un link contenido en el archivo
  Web_calendario_NBA.html.
- fichero json **Teams.json** que contiene los equipos de la NBA con sus IDs extraidos de las API  https://v1.basketball.api-sports.io/teams y https://v2.nba.api-sports.io/teams.
  Este archivo se crea durante la ejecución del fichero analisis_equipos_NBA.py.
- fichero json **Statistics_2_teams.json** que contiene las estadísticas del equipo seleccionado y su contrincante en el próximo partido extraidas de las API 
  https://v1.basketball.api-sports.io/statistics?season=2022-2023&team={id_equipo}&league=12 y https://v2.nba.api-sports.io/teams/statistics. Este archivo se 
  crea durante la ejecución del fichero analisis_equipos_NBA.py.
- imagen png **games_result_location.png** que contiene un gráfico con el ratio de victorias, empates y derrotas por sitio del equipo seleccionado. 
- imagen png **result_percentage_team.png** que contiene un gráfico con el ratio de victorias, empates y derrotas del equipo seleccionado y su contrincante.
- imagen png **points_for_against_locatio.png** que contiene un gráfico con los puntos a favor y en contra por sitio del equipo seleccionado.
- imagen png **points_for_against_team.png** que contiene un gráfico con los puntos a favor y en contra del equipo seleccionado y su contrincante.
- imagen png **number_successful_rebounds_type.png** que contiene un gráfico con los rebotes ofensivos y defensivos realizados por el equipo seleccionado.
- imagen png **percentage_successful_throws_type.png** que contiene un gráfico con el porcentage de canastas según los diferentes tiros del equipo seleccionado.

## Ejecución del fichero
#### Descargarse los siguientes archivos desde este repositorio:
  - requirements.txt
  - config.txt
  - Jornadas.json
  - Jornadas_fechas.json
  - NBA_logo_letras.png
#### Instalar las librerías del requirements.txt
Lo hacemos desde la terminal con el siguiente comando:

`pip install -r requirements.txt`
#### Escribir en el archivo config.txt la key de tu cuenta de la API (es la misma para ambas APIs utilizadas).
Si no tienes una cuenta, te puedes crear una cuenta gratuita pinchando [aquí](https://dashboard.api-football.com/register)

#### Ejecutar el fichero de python analisis_equipos_NBA.py
Lo hacemos desde la terminal con el siguiente comando:

`python pdf_crear_reporte_ejecutivo.py`

Durante la ejecución del archivo tendremos que elegir el equipo del que queramos hacer el reporte.
#### Reporte del equipo en el documento {nombre_equipo}\_{fecha}.pdf
El reporte ejecutivo contiene las estadísticas del equipo seleccionado, la comparación de este con el contrincante de su proximo partido y una predicción del resultado de este.
