# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 5.
Api y web scraping.

Senior data analyst de la NBA.
------------------------------

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
'''


from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fpdf import FPDF
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import requests
import seaborn as sns

class PDF(FPDF):
    def header(self):
        global equipo_sel
        self.set_y(15)
        self.set_font('times', '', 10)
        self.cell(65, 10, f'{equipo_sel}'.upper())
        self.cell(20, 10, '') # Añadimos una celda con el tamaño de la imagen
        self.image('equipo.png', 95, 10, 20)
        self.cell(65, 10, datetime.now().strftime('%d/%m/%Y'), align='R')
        self.ln()


    def footer(self):
        self.set_y(-15)
        self.set_font('times', '', 10)
        self.cell(0, 5, f'Página {self.page_no()} de {{nb}}', align='R')
        self.ln()



def Extract_equipos_api():
    with open('config.txt', 'r') as f:
        clave = f.read().strip()
    headers1 = {
    'x-rapidapi-key': clave,
    'x-rapidapi-host': 'v1.basketball.api-sports.io'}

    headers2 = {
    'x-rapidapi-key': clave,
    'x-rapidapi-host': 'v2.nba.api-sports.io'}

    parameters1_equipos = {'league': "12", 'season': "2022-2023"}

    api1_equipos = 'https://v1.basketball.api-sports.io/teams'
    api2_equipos = 'https://v2.nba.api-sports.io/teams'


    equipos1 = requests.get(api1_equipos, headers=headers1, params=parameters1_equipos).json()['response']
    equipos2 = requests.get(api2_equipos, headers=headers2).json()['response']

    return equipos1, equipos2


def Transform_equipos_api(equipos1, equipos2):
    nombres_equipos = [x['name'] for x in equipos1]
    ids_equipos1 = [x['id'] for x in equipos1]
    ids_equipos2 = [x['id'] for x in equipos2 if x['name'] in nombres_equipos or x['name'] == 'LA Clippers']
    code_equipos = [x['code'] for x in equipos2 if x['name'] in nombres_equipos or x['name'] == 'LA Clippers']
    lista_equipos = []
    for i in range(len(nombres_equipos)):
        if nombres_equipos[i] == 'Los Angeles Clippers':
            nombres_equipos[i] = 'L.A. Clippers'
        if nombres_equipos[i] == 'Los Angeles Lakers':
            nombres_equipos[i] = 'L.A. Lakers'
        lista_equipos.append([nombres_equipos[i], code_equipos[i], ids_equipos1[i], ids_equipos2[i]])
    return lista_equipos


def Load_equipos_api(lista_equipos):
    with open('Teams.json', 'w') as file:
        json.dump(lista_equipos, file, indent=4)


def Extract_html():
    URL = 'https://www.marca.com/baloncesto/nba/calendario.html'
    response = requests.get(URL).text
    doc = BeautifulSoup(response, 'html.parser')
    return doc


def preguntar_equipo():
    global equipo_sel
    with open('Teams.json', 'r') as f:
        equipos_con_id = json.load(f)
    equipos = [x[0] for x in equipos_con_id]
    for i in range(len(equipos)):
        print(f'{i + 1}. {equipos[i]}')
    respuesta_incorrecta = True
    while respuesta_incorrecta:
        opc = input('Elige el número del equipo del que quieres hacer un informe: ')
        try:
            opc_int = int(opc) - 1
            if 0 <= opc_int and opc_int <= 29:
                respuesta_incorrecta = False
                equipo_sel = equipos[opc_int]
            else:
                print('Entrada incorrecta, vuelva a introducir el número.\n')
        except ValueError:
            print('Entrada incorrecta, vuelva a introducir el número.\n')
    
    return equipo_sel


def por_que_jornada_vamos():
    with open('Jornadas.json', 'r') as f:
        jornadas = dict(json.load(f))

    hoy = datetime.now()
    fechas = list(jornadas.keys())
    if hoy.strftime('%d-%m-%Y') in fechas:
        jornada_actual = jornadas[hoy.strftime('%d-%m-%Y')]
    else:
        manana = hoy + timedelta(1)
        manana_str = manana.strftime('%d-%m-%Y')
        manana_list = manana_str.split('-')
        manana_int = int(manana_list[2] + manana_list[1] + manana_list[0])
        while (manana_str not in fechas) and (manana_int < 20230410):
            manana = manana + timedelta(1)
            manana_str = manana.strftime('%d-%m-%Y')
            manana_list = manana_str.split('-')
            manana_int = int(manana_list[2] + manana_list[1] + manana_list[0])
        if manana_int < 20230410:
            jornada_actual = jornadas[manana_str]
        else:
            print('Ya se ha acabado la temporada de la NBA.')
            print('Saliendo de programa ...')
            os._exit(1)
    if type(jornada_actual) == list:
        jornada_actual = jornada_actual[0]
    jornada_list = jornada_actual.split()
    jornada = jornada_list[0].lower() + jornada_list[1]

    return jornada


def equipos_jornada(doc, jornada):
    tag = doc.find('caption', {'id': jornada})
    tabla = tag.next_sibling.next_sibling.next_sibling.next_sibling
    a = re.sub(re.compile('\n'), ' ', tabla.text)
    b = re.sub(re.compile('   +'), '    ', a).strip()
    c = re.sub(re.compile(' [0-9\W]+ '), '    ', b)
    equipos_sep = c.split('    ')
    return equipos_sep


def buscar_proximo_partido(doc, jornada, equipo_sel):
    global local
    equipos_sep = equipos_jornada(doc, jornada)
    if equipo_sel in equipos_sep:
        index = equipos_sep.index(equipo_sel)
        if index % 2 == 0:
            contrincante = equipos_sep[index + 1]
            local = True
        else:
            contrincante = equipos_sep[index - 1]
            local = False
        jornada_partido = jornada
    else:
        if jornada != "jornada164":
            siguiente_jornada = 'jornada' + str(int(jornada.split('a')[-1]) + 1 )
            equipos_sep = equipos_jornada(doc, siguiente_jornada)
            while equipo_sel not in equipos_sep and siguiente_jornada != "jornada164":
                siguiente_jornada = 'jornada' + str(int(jornada.split('a')[-1]) + 1 )
                equipos_sep = equipos_jornada(doc, siguiente_jornada)
            if siguiente_jornada == "jornada164":
                print('Este equipo ya no va a jugar más partidos en esta temporada de la NBA.')
                print('Saliendo de programa ...')
                os._exit(1)
            index = equipos_sep.index(equipo_sel)
            if index % 2 == 0:
                contrincante = equipos_sep[index + 1]
                local = True
            else:
                contrincante = equipos_sep[index - 1]
                local = False
        jornada_partido = siguiente_jornada
    return contrincante, jornada_partido


def buscar_y_guardar_logos(doc, equipo_sel, contrincante):
    tag_equipo1 = doc.find('img',{'alt': equipo_sel})
    tag_equipo2 = doc.find('img',{'alt': contrincante})
    link_logo1 = tag_equipo1.attrs['src']
    link_logo2 = tag_equipo2.attrs['src']
    logo1 = requests.get(link_logo1).content
    logo2 = requests.get(link_logo2).content
    with open('equipo.png', 'wb') as img:
        img.write(logo1)
    with open('contrincante.png', 'wb') as img:
        img.write(logo2)


def Transform_html(doc):
    equipo_sel = preguntar_equipo()
    jornada = por_que_jornada_vamos()
    contrincante, jornada_partido = buscar_proximo_partido(doc, jornada, equipo_sel)
    buscar_y_guardar_logos(doc, equipo_sel, contrincante)
    return contrincante, jornada_partido


def Load_html(doc):
    html = doc.prettify("utf-8")
    with open('Web_calendario_NBA.html', 'wb') as f:
        f.write(html)


def buscar_info_equipo_por_nombre(n_equipo):
    with open('Teams.json', 'r') as f:
        info_equipos = json.load(f)
    act = info_equipos[0]
    i = 1
    while act[0] != n_equipo:
        act = info_equipos[i]
        i += 1
    return act


def Extract_estadisticas_api(equipo_sel, contrincante):
    with open('config.txt', 'r') as f:
        clave = f.read().strip()
    headers1 = {
    'x-rapidapi-key': clave,
    'x-rapidapi-host': 'v1.basketball.api-sports.io'}

    headers2 = {
    'x-rapidapi-key': clave,
    'x-rapidapi-host': 'v2.nba.api-sports.io'}

    info_equipo1 = buscar_info_equipo_por_nombre(equipo_sel)
    info_equipo2 = buscar_info_equipo_por_nombre(contrincante)

    equipos_proximo_partido = [info_equipo1, info_equipo2]

    estadisticas1 = list()
    estadisticas2 = list()
    for equipo in equipos_proximo_partido:
        team_id1 = equipo[2]
        team_id2 = equipo[3]
        parameters2_estadisticas = {'id': str(team_id2), 'season': '2022'}
        api1_estadisticas = f'https://v1.basketball.api-sports.io/statistics?season=2022-2023&team={team_id1}&league=12'
        api2_estadisticas = 'https://v2.nba.api-sports.io/teams/statistics'
        statistics1 = requests.get(api1_estadisticas, headers=headers1).json()['response']
        statistics2 = requests.get(api2_estadisticas, headers=headers2, params=parameters2_estadisticas).json()['response']
        estadisticas1.append(statistics1)
        estadisticas2.append(statistics2)
    return equipos_proximo_partido, estadisticas1, estadisticas2


def Transform_estadisticas_api(equipos_proximo_partido, estadisticas1, estadisticas2):
    estadisticas_tot = list()
    for i in range(2):
        nombre = equipos_proximo_partido[i][0]
        codigo = equipos_proximo_partido[i][1]
        statistics1 = estadisticas1[i]
        statistics2 = estadisticas2[i]
        games_wins = {'home': {'total': statistics1['games']['wins']['home']['total'], 'percentage': float(statistics1['games']['wins']['home']['percentage'])}, 'away': {'total': statistics1['games']['wins']['away']['total'], 'percentage': float(statistics1['games']['wins']['away']['percentage'])}, 'all': {'total': statistics1['games']['wins']['all']['total'], 'percentage': float(statistics1['games']['wins']['all']['percentage'])}}
        games_draws = {'home': {'total': statistics1['games']['draws']['home']['total'], 'percentage': float(statistics1['games']['draws']['home']['percentage'])}, 'away': {'total': statistics1['games']['draws']['away']['total'], 'percentage': float(statistics1['games']['draws']['away']['percentage'])}, 'all': {'total': statistics1['games']['draws']['all']['total'], 'percentage': float(statistics1['games']['draws']['all']['percentage'])}}
        games_loses = {'home': {'total': statistics1['games']['loses']['home']['total'], 'percentage': float(statistics1['games']['loses']['home']['percentage'])}, 'away': {'total': statistics1['games']['loses']['away']['total'], 'percentage': float(statistics1['games']['loses']['away']['percentage'])}, 'all': {'total': statistics1['games']['loses']['all']['total'], 'percentage': float(statistics1['games']['loses']['all']['percentage'])}}
        games = {'played': statistics1['games']['played'], 'wins': games_wins, 'draws': games_draws, 'loses': games_loses}
        points_for = {'total': statistics1['points']['for']['total'], 'average': {'home': float(statistics1['points']['for']['average']['home']), 'away': float(statistics1['points']['for']['average']['away']), 'all': float(statistics1['points']['for']['average']['all'])}}
        points_against = {'total': statistics1['points']['against']['total'], 'average': {'home': float(statistics1['points']['against']['average']['home']), 'away': float(statistics1['points']['against']['average']['away']), 'all': float(statistics1['points']['against']['average']['all'])}}
        points = {'for': points_for, 'against': points_against}
        field_goals = {'made': statistics2[0]['fgm'], 'attempted': statistics2[0]['fga'], 'percentage': float(statistics2[0]['fgp'])}
        free_throws = {'made': statistics2[0]['ftm'], 'attempted': statistics2[0]['fta'], 'percentage': float(statistics2[0]['ftp'])}
        three_pointers = {'made': statistics2[0]['tpm'], 'attempted': statistics2[0]['tpa'], 'percentage': float(statistics2[0]['tpp'])}
        rebounds = {'offensive': statistics2[0]['offReb'], 'defensive': statistics2[0]['defReb'], 'total': statistics2[0]['totReb']}
        others = {'assists': statistics2[0]['assists'], 'fouls': statistics2[0]['pFouls'], 'steals': statistics2[0]['steals'], 'turnovers': statistics2[0]['turnovers'], 'blocks': statistics2[0]['blocks']}
        dict_tot = {'games': games, 'points': points, 'field goals': field_goals, 'free throws': free_throws, 'three pointers': three_pointers, 'rebounds': rebounds, 'others': others}
        estadisticas_tot.append({'name': nombre, 'code': codigo, 'statistics': dict_tot})
    return estadisticas_tot


def Load_estadisticas_api(estadisticas_tot):
    with open('Statistics_2_teams.json', 'w') as file:
        json.dump(estadisticas_tot, file, indent=4)


def estadisticas_equipos():
    with open('Statistics_2_teams.json', 'r') as file:
        estadisticas_2_teams = json.load(file)

    equipo = estadisticas_2_teams[0]['statistics']
    contrincante = estadisticas_2_teams[1]['statistics']

    egph = equipo['games']['played']['home']  # games played home
    egpaw = equipo['games']['played']['away'] # games played away
    egpall = equipo['games']['played']['all'] # games played all

    egwht = equipo['games']['wins']['home']['total']       # games wins home total
    egwhp = equipo['games']['wins']['home']['percentage']  # games wins home %
    egwawt = equipo['games']['wins']['away']['total']      # games wins away total
    egwawp = equipo['games']['wins']['away']['percentage'] # games wins away %
    egwallt = equipo['games']['wins']['all']['total']      # games wins all total
    egwallp = equipo['games']['wins']['all']['percentage'] # games wins all %

    egdht = equipo['games']['draws']['home']['total']       # games draws home total
    egdhp = equipo['games']['draws']['home']['percentage']  # games draws home %
    egdawt = equipo['games']['draws']['away']['total']      # games draws away total
    egdawp = equipo['games']['draws']['away']['percentage'] # games draws away %
    egdallt = equipo['games']['draws']['all']['total']      # games draws all total
    egdallp = equipo['games']['draws']['all']['percentage'] # games draws all %

    eglht = equipo['games']['loses']['home']['total']        # games loses home total
    eglhp = equipo['games']['loses']['home']['percentage']   # games loses home %
    eglawt = equipo['games']['loses']['away']['total']       # games loses away total
    eglawp = equipo['games']['loses']['away']['percentage']  # games loses away %
    eglallt = equipo['games']['loses']['all']['total']      # games loses all total
    eglallp = equipo['games']['loses']['all']['percentage'] # games loses all %

    epfth = equipo['points']['for']['total']['home']    # points for total home
    epftaw = equipo['points']['for']['total']['away']   # points for total away
    epftall = equipo['points']['for']['total']['all']   # points for total all
    epfah = equipo['points']['for']['average']['home']  # points for average home
    epfaaw = equipo['points']['for']['average']['away'] # points for average away
    epfaall = equipo['points']['for']['average']['all'] # points for average all

    epath = equipo['points']['against']['total']['home']    # points against total home
    epataw = equipo['points']['against']['total']['away']   # points against total away
    epatall = equipo['points']['against']['total']['all']   # points against total all
    epaah = equipo['points']['against']['average']['home']  # points against average home
    epaaaw = equipo['points']['against']['average']['away'] # points against average away
    epaaall = equipo['points']['against']['average']['all'] # points against average all

    efgm = equipo['field goals']['made']       # field goals made
    efga = equipo['field goals']['attempted']  # field goals attempted
    efgp = equipo['field goals']['percentage'] # field goals %

    eftm = equipo['free throws']['made']       # free throws made
    efta = equipo['free throws']['attempted']  # free throws attempted
    eftp = equipo['free throws']['percentage'] # free throws %

    etpm = equipo['three pointers']['made']       # three pointers made
    etpa = equipo['three pointers']['attempted']  # three pointers attempted
    etpp = equipo['three pointers']['percentage'] # three pointers %

    ero = equipo['rebounds']['offensive'] # rebounds offensive
    erd = equipo['rebounds']['defensive'] # rebounds defensive
    ert = equipo['rebounds']['total']     # rebounds total

    eassi = equipo['others']['assists']   # assists
    efouls = equipo['others']['fouls']    # fouls
    estls = equipo['others']['steals']    # steals
    etrno = equipo['others']['turnovers'] # turnovers
    eblck = equipo['others']['blocks']    # blocks

    cgph = contrincante['games']['played']['home']  # games played home
    cgpaw = contrincante['games']['played']['away'] # games played away
    cgpall = contrincante['games']['played']['all'] # games played all

    cgwht = contrincante['games']['wins']['home']['total']       # games wins home total
    cgwhp = contrincante['games']['wins']['home']['percentage']  # games wins home %
    cgwawt = contrincante['games']['wins']['away']['total']      # games wins away total
    cgwawp = contrincante['games']['wins']['away']['percentage'] # games wins away %
    cgwallt = contrincante['games']['wins']['all']['total']      # games wins all total
    cgwallp = contrincante['games']['wins']['all']['percentage'] # games wins all %

    cgdht = contrincante['games']['draws']['home']['total']       # games draws home total
    cgdhp = contrincante['games']['draws']['home']['percentage']  # games draws home %
    cgdawt = contrincante['games']['draws']['away']['total']      # games draws away total
    cgdawp = contrincante['games']['draws']['away']['percentage'] # games draws away %
    cgdallt = contrincante['games']['draws']['all']['total']      # games draws all total
    cgdallp = contrincante['games']['draws']['all']['percentage'] # games draws all %

    cglht = contrincante['games']['loses']['home']['total']        # games loses home total
    cglhp = contrincante['games']['loses']['home']['percentage']   # games loses home %
    cglawt = contrincante['games']['loses']['away']['total']       # games loses away total
    cglawp = contrincante['games']['loses']['away']['percentage']  # games loses away %
    cglallt = contrincante['games']['loses']['all']['total']      # games loses all total
    cglallp = contrincante['games']['loses']['all']['percentage'] # games loses all %

    cpfth = contrincante['points']['for']['total']['home']    # points for total home
    cpftaw = contrincante['points']['for']['total']['away']   # points for total away
    cpftall = contrincante['points']['for']['total']['all']   # points for total all
    cpfah = contrincante['points']['for']['average']['home']  # points for average home
    cpfaaw = contrincante['points']['for']['average']['away'] # points for average away
    cpfaall = contrincante['points']['for']['average']['all'] # points for average all

    cpath = contrincante['points']['against']['total']['home']    # points against total home
    cpataw = contrincante['points']['against']['total']['away']   # points against total away
    cpatall = contrincante['points']['against']['total']['all']   # points against total all
    cpaah = contrincante['points']['against']['average']['home']  # points against average home
    cpaaaw = contrincante['points']['against']['average']['away'] # points against average away
    cpaaall = contrincante['points']['against']['average']['all'] # points against average all

    cfgm = contrincante['field goals']['made']       # field goals made
    cfga = contrincante['field goals']['attempted']  # field goals attempted
    cfgp = contrincante['field goals']['percentage'] # field goals %

    cftm = contrincante['free throws']['made']       # free throws made
    cfta = contrincante['free throws']['attempted']  # free throws attempted
    cftp = contrincante['free throws']['percentage'] # free throws %

    ctpm = contrincante['three pointers']['made']       # three pointers made
    ctpa = contrincante['three pointers']['attempted']  # three pointers attempted
    ctpp = contrincante['three pointers']['percentage'] # three pointers %

    cro = contrincante['rebounds']['offensive'] # rebounds offensive
    crd = contrincante['rebounds']['defensive'] # rebounds defensive
    crt = contrincante['rebounds']['total']     # rebounds total

    cassi = contrincante['others']['assists']   # assists
    cfouls = contrincante['others']['fouls']    # fouls
    cstls = contrincante['others']['steals']    # steals
    ctrno = contrincante['others']['turnovers'] # turnovers
    cblck = contrincante['others']['blocks']    # blocks

    lequipo = [egph, egpaw, egpall, egwht, egwhp, egwawt, egwawp, egwallt, egwallp, egdht, egdhp, egdawt, egdawp, egdallt, egdallp, eglht, eglhp, eglawt, eglawp, eglallt, eglallp, epfth, epftaw, epftall, epfah, epfaaw, epfaall, epath, epataw, epatall, epaah, epaaaw, epaaall, efgm, efga, efgp, eftm, efta, eftp, etpm, etpa, etpp, ero, erd, ert, eassi, efouls, estls, etrno, eblck]
    lcontrincante = [cgph, cgpaw, cgpall, cgwht, cgwhp, cgwawt, cgwawp, cgwallt, cgwallp, cgdht, cgdhp, cgdawt, cgdawp, cgdallt, cgdallp, cglht, cglhp, cglawt, cglawp, cglallt, cglallp, cpfth, cpftaw, cpftall, cpfah, cpfaaw, cpfaall, cpath, cpataw, cpatall, cpaah, cpaaaw, cpaaall, cfgm, cfga, cfgp, cftm, cfta, cftp, ctpm, ctpa, ctpp, cro, crd, crt, cassi, cfouls, cstls, ctrno, cblck]

    return lequipo, lcontrincante


def crear_graficos_equipo(l):
    sns.set_palette("Set2")
    df1 = pd.DataFrame({'result': ['wins', 'draws', 'loses', 'wins', 'draws', 'loses', 'wins', 'draws', 'loses'], 'location': ['home', 'home', 'home', 'away', 'away', 'away', 'all', 'all', 'all'], 'Value': [l[4], l[10], l[16], l[6], l[12], l[18], l[8], l[14], l[20]]})
    plt.figure(figsize=(12, 7))
    ax1 = sns.barplot(x='result', y='Value', hue='location', data=df1)
    plt.title("Ratio of wins, draws and loses per location", fontsize=16, fontweight='bold')
    for i in ax1.containers:
        ax1.bar_label(i,)

    plt.xlabel('Result', fontweight='bold')
    plt.ylabel('Ratio', fontweight='bold')
    plt.ylim((0, 1))
    plt.savefig('games_result_location.png', bbox_inches = 'tight')



    df2 = pd.DataFrame({'points': ['for', 'against', 'for', 'against', 'for', 'against'], 'location': ['home', 'home', 'away', 'away', 'all', 'all'], 'Value': [l[24], l[30], l[25], l[31], l[26], l[32]]})
    plt.figure(figsize=(12, 7))
    ax2 = sns.barplot(x='points', y='Value', hue='location', data=df2)
    plt.title('Average of number of points scored for and against per location', fontsize=16, fontweight='bold')
    for i in ax2.containers:
        ax2.bar_label(i,)
    plt.xlabel('Points', fontweight='bold')
    plt.ylabel('Number of points scored', fontweight='bold')
    plt.savefig('points_for_against_location.png', bbox_inches = 'tight')



    plt.figure(figsize=(12, 7))
    ax3 = sns.barplot(x=['field goals', 'free throws', 'three pointers'], y=[l[35], l[38], l[41]])
    plt.title('Percentage of successful throws by type', fontsize=16, fontweight='bold')
    for i in ax3.containers:
        ax3.bar_label(i,)
    plt.xlabel('Type of attempt', fontweight='bold')
    plt.ylabel('Percentage of successful throws', fontweight='bold')
    plt.ylim((0, 100))
    plt.savefig('percentage_successful_throws_type.png', bbox_inches = 'tight')



    plt.figure(figsize=(12, 7))
    ax4 = sns.barplot(x=['offensive', 'defensive'], y=[l[42], l[43]])
    plt.title('Number of successful rebounds by type', fontsize=16, fontweight='bold')
    for i in ax4.containers:
        ax4.bar_label(i,)

    plt.xlabel('Type of rebound', fontweight='bold')
    plt.ylabel('Number of successful rebounds', fontweight='bold')
    plt.savefig('number_successful_rebounds_type.png', bbox_inches = 'tight')


def crear_graficos_conjuntos(l1, l2, equipo_sel, contrincante):
    global local
    if local:
        ldf1 = [l1[4], l1[10], l1[16], l2[6], l2[12], l2[18]]
        ldf2 = [l1[24], l1[30], l2[25], l2[31]]
    else:
        ldf1 = [l1[6], l1[12], l1[18], l2[4], l2[10], l2[16]]
        ldf2 = [l1[25], l1[31], l2[24], l2[30]]

    sns.set_palette("Set2")
    df1 = pd.DataFrame({'result': ['wins', 'draws', 'loses', 'wins', 'draws', 'loses'], 'Team': [f'{equipo_sel}', f'{equipo_sel}', f'{equipo_sel}', f'{contrincante}', f'{contrincante}', f'{contrincante}'], 'Value': ldf1})
    plt.figure(figsize=(12, 7))
    ax1 = sns.barplot(x='result', y='Value', hue='Team', data=df1)
    plt.title('Ratio of wins, draws and loses by team', fontsize=16, fontweight='bold')
    for i in ax1.containers:
        ax1.bar_label(i,)

    plt.xlabel('Result', fontweight='bold')
    plt.ylabel('Ratio', fontweight='bold')
    plt.ylim((0, 1))
    plt.savefig('result_percentage_team.png', bbox_inches = 'tight')



    df2 = pd.DataFrame({'points': ['for', 'against', 'for', 'against'], 'Team': [f'{equipo_sel}', f'{equipo_sel}', f'{contrincante}', f'{contrincante}'], 'Value': ldf2})
    plt.figure(figsize=(12, 7))
    ax2 = sns.barplot(x='points', y='Value', hue='Team', data=df2)
    plt.title('Average of number of points scored for and against by team', fontsize=16, fontweight='bold')
    plt.legend(loc='lower right')
    for i in ax2.containers:
        ax2.bar_label(i,)

    plt.xlabel('Points', fontweight='bold')
    plt.ylabel('Number of points scored', fontweight='bold')
    plt.savefig('points_for_against_team.png', bbox_inches = 'tight')


def pronostico(l1, l2):
    global local
    if local:
        diferencia_victorias = l1[4] - l2[6]
        diferencia_puntos_favor = l1[24] - l2[25]
        diferencia_puntos_contra = l2[31] - l1[30]
    else:
        diferencia_victorias = l1[6] - l2[4]
        diferencia_puntos_favor = l1[25] - l2[24]
        diferencia_puntos_contra = l2[30] - l1[31]

    dif_tot = diferencia_victorias*25 + diferencia_puntos_favor + diferencia_puntos_contra
    if dif_tot > 0:
        gana = 1
    elif dif_tot < 0:
        gana = -1
    else:
        gana = 0
    return gana


def portada(pdf: PDF):
    pdf.add_page()
    pdf.set_font('times', 'B', 28)
    pdf.cell(0, 15, '')
    pdf.ln()
    pdf.multi_cell(0, 15, f"{equipo_sel} in the NBA".upper(), align='C') # El titulo esta centrado en la página
    pdf.ln()
    # Queremos añadir una foto a la página
    ancho_pagina = pdf.w
    posicion_foto = (ancho_pagina - 150)//2 # Calculamos la posicion de la foto para que quede centrada
    pdf.image('NBA_logo_letras.png', x= posicion_foto, w= 150) # Añadimos la imagen
    pdf.ln()

    pdf.set_font('times', '', 16) #Cambiamos el tipo de letra
    pdf.multi_cell(0, 10, 'ADQUISICIÓN DE DATOS\n Catalina Royo-Villanova Seguí', align='C')
    pdf.ln()

    return pdf


def analisis_estadisticas(pdf: PDF):
    # Titulo
    pdf.add_page()
    pdf.ln(8)
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 15, "Statistics report of season 2022-2023".upper(), align='C')
    pdf.ln(11)

    # Primer grafico
    pdf.set_font('times', 'U', 15)
    pdf.cell(0, 10, 'Ratio of games results per location:')
    pdf.ln(13)
    pdf.image('games_result_location.png', x=30, w=150)
    pdf.ln(5)


    # Segundo grafico
    pdf.cell(0, 10, 'Average of number points scored for and against per location:')
    pdf.ln(13)
    pdf.image('points_for_against_location.png', x=30, w=150)

    # Titulo
    pdf.add_page()
    pdf.ln(8)
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 15, "Statistics report of season 2022-2023".upper(), align='C')
    pdf.ln(11)

    # Tercer grafico
    pdf.set_font('times', 'U', 15)
    pdf.cell(0, 10, 'Percentage of successful throws by type:')
    pdf.ln(13)
    pdf.image('percentage_successful_throws_type.png', x=30, w=150)
    pdf.ln(5)


    # Cuarto grafico
    pdf.cell(0, 10, 'Number of successful rebounds by type:')
    pdf.ln(13)
    pdf.image('number_successful_rebounds_type.png', x=30, w=150)


    return pdf


def comparacion_equipos(pdf: PDF, equipo_sel: str, contrincante: str, gana: int, jornada_partido: str):
    global local
    if local:
        equipo1 = equipo_sel
        equipo2 = contrincante
    else:
        equipo1 = contrincante
        equipo2 = equipo_sel


    if gana == 1:
        ganador = equipo_sel
    elif gana == -1:
        ganador = contrincante
    else:
        ganador = equipo1

    with open('Jornadas_fechas.json', 'r') as f:
        fecha = datetime.strptime(json.load(f)[jornada_partido], '%d-%m-%Y')


    # Titulo
    pdf.add_page()
    pdf.set_font('times', 'B', 25)
    pdf.ln(8)
    pdf.cell(0, 10, f'{equipo1}', align='C')
    pdf.ln()
    pdf.set_font('times', '', 20)
    pdf.cell(0, 8, 'vs', align='C')
    pdf.ln()
    pdf.set_font('times', 'B', 25)
    pdf.cell(0, 10, f'{equipo2}', align='C')
    pdf.ln(15)

    pdf.set_font('times', '', 12)
    dia_sem = fecha.strftime('%A')
    dia = fecha.strftime('%d')
    mes = fecha.strftime('%B')
    year = fecha.strftime('%Y')
    pdf.multi_cell(0, 5, f"The match will take place on {dia_sem} {dia} {mes}, {year}. It confronts the {equipo2} and the {equipo1} in the latter's home.")
    pdf.ln()
    pdf.multi_cell(0, 5, f'After analizing the progress of both teams so far in the season, it seams more likely that the {ganador} will win.')
    pdf.ln()
    
    # Primer gráfico
    pdf.set_font('times', 'U', 15)
    pdf.multi_cell(0, 10, f'Ratio of games results of {equipo_sel} and {contrincante}:')
    pdf.ln(5)
    pdf.image('result_percentage_team.png', x=30, w=150)
    pdf.ln(10)

    pdf.add_page()
    pdf.set_font('times', 'B', 25)
    pdf.ln(8)
    pdf.cell(0, 10, f'{equipo1}', align='C')
    pdf.ln()
    pdf.set_font('times', '', 20)
    pdf.cell(0, 8, 'vs', align='C')
    pdf.ln()
    pdf.set_font('times', 'B', 25)
    pdf.cell(0, 10, f'{equipo2}', align='C')
    pdf.ln(15)

   # Segundo grafico
    pdf.set_font('times', 'U', 15)
    pdf.multi_cell(0, 10, f'Average of number points scored for and against per location of {equipo_sel} and {contrincante}:')
    pdf.ln(5)
    pdf.image('points_for_against_team.png', x=30, w=150)

    return pdf


def anexos(pdf: PDF):
    global local
    with open('Statistics_2_teams.json', 'r') as file:
        data = json.load(file)
    if local:
        home = data[0]
        away = data[1]
    else:
        home = data[1]
        away = data[2]
    data_home = json.dumps(home, indent=4)
    data_home_list = data_home.split('\n')
    data_home_list1 = data_home_list[:53]
    data_home_list2 = data_home_list[53:]
    data_away = json.dumps(away, indent=4)
    data_away_list = data_away.split('\n')
    data_away_list1 = data_away_list[:53]
    data_away_list2 = data_away_list[53:]

    pdf.add_page()
    pdf.ln(8)
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 15, 'Raw Data'.upper(), align='C')
    pdf.ln(11)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 8, 'Home team raw data:')
    pdf.ln()
    pdf.set_font('times', '', 10)
    for i in range(len(data_home_list1)):
        pdf.cell(75, 4, data_home_list1[i])
        pdf.cell(75, 4, data_home_list2[i])
        pdf.ln()
    pdf.cell(75, 4, '')
    pdf.cell(75, 4, data_home_list2[-2])
    pdf.ln()
    pdf.cell(75, 4, '')
    pdf.cell(75, 4, data_home_list2[-1])
    pdf.ln()

    pdf.add_page()
    pdf.ln(8)
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 15, 'Raw Data'.upper(), align='C')
    pdf.ln(11)
    pdf.set_font('times', 'U', 12)
    pdf.cell(0, 8, 'Away team raw data:')
    pdf.ln()
    pdf.set_font('times', '', 10)
    for i in range(len(data_away_list1)):
        pdf.cell(75, 4, data_away_list1[i])
        pdf.cell(75, 4, data_away_list2[i])
        pdf.ln()
    pdf.cell(75, 4, '')
    pdf.cell(75, 4, data_away_list2[-2])
    pdf.ln()
    pdf.cell(75, 4, '')
    pdf.cell(75, 4, data_away_list2[-1])
    pdf.ln()
    return pdf


def crear_pdf(equipo_sel, contrincante, gana, jornada_partido):
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_margins(30, 35, 30)
    pdf.set_auto_page_break(True, 25)
    pdf = portada(pdf)
    pdf = analisis_estadisticas(pdf)
    pdf = comparacion_equipos(pdf, equipo_sel, contrincante, gana, jornada_partido)
    pdf = anexos(pdf)

    fecha = datetime.now().strftime('%d%m%Y')
    equipo_sel_limpio = re.sub('\.', '', re.sub(' ', '_', equipo_sel))
    pdf.output(f'{equipo_sel_limpio}_{fecha}.pdf')

if __name__ == '__main__':
    global local
    # Cargamos los equipos que hay en esta temporada de la NBA
    equipos1, equipos2 = Extract_equipos_api()
    lista_equipos = Transform_equipos_api(equipos1, equipos2)
    Load_equipos_api(lista_equipos)

    # Seleccionamos un equipo y buscamos la informacion de su proximo partido
    doc = Extract_html()
    contrincante, jornada_partido = Transform_html(doc)
    Load_html(doc)
    
    # Cargamos las estadisticas del equipo seleccionado y de su contrincante
    equipos_proximo_partido, estadisticas1, estadisticas2 = Extract_estadisticas_api(equipo_sel, contrincante)
    estadisticas_tot = Transform_estadisticas_api(equipos_proximo_partido, estadisticas1, estadisticas2)
    Load_estadisticas_api(estadisticas_tot)

    # Estudiamos las estadisticas de los equipos
    l_equipo, l_contrincante = estadisticas_equipos()
    crear_graficos_equipo(l_equipo)
    crear_graficos_conjuntos(l_equipo, l_contrincante, equipo_sel, contrincante)
    gana = pronostico(l_equipo, l_contrincante)

    # Creamos el pdf
    crear_pdf(equipo_sel, contrincante, gana, jornada_partido)








