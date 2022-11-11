# Catalina Royo-Villanova Seguí
# 202104665

'''YO: Bug hunter
QUIERO: Crear un proceso ETL
PARA: Encontrar leaks en commits'''

from git import Repo
import pandas as pd
import re, signal, sys

def Extract(directorio_repositorio):
    repo = Repo(directorio_repositorio)
    lista_commits = list(repo.iter_commits('develop'))
    return lista_commits

def Transform(lista_commits):
    mensajes_commits = []
    for i in range(len(lista_commits)):
        mensajes_commits.append(lista_commits[i].message)
    df_commits =  pd.DataFrame(list(zip(lista_commits, mensajes_commits)), columns=['Commit', 'Mensaje'])
    return df_commits

def Load(df):
    Possibles_leaks = ['password', 'pwd', 'contraseña', 'contra&ntildea','key']
    leaks = []
    for i in range(len(df)):
        mensaje = df['Mensaje'][i]
        id_commit = df['Commit'][i]
        for leak in Possibles_leaks:
            if re.search(leak, mensaje, re.IGNORECASE):
                print(f'Se ha encontrado un leak en el commit {id_commit}.')
                leaks.append(id_commit)
    print('Se ha acabado la busqueda de leaks en los commits del repositorio.')
    return leaks


def handler_signal(signal, frame):
    print('\nSE HA INTERRUMPIDO LA EJECUCION DEL PROGRAMA.\n\nSALIENDO...\n')
    sys.exit(1)

signal.signal(signal.SIGINT, handler_signal)


if __name__ == '__main__':
    directorio_repo = './skale/skale-manager'
    lista_commits = Extract(directorio_repo)
    df_commits = Transform(lista_commits)
    leaks = Load(df_commits)