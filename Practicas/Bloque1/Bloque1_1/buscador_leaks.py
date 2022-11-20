# Catalina Royo-Villanova Seguí
# 202104665

'''
Bloque 1.
Practica 1.

Exportar los datos obtenidos en la practica de obtencion de leaks en commit
de git a un fichero json.
'''

from git import Repo
import pandas as pd
import re, signal, sys

def Extract(directorio_repositorio, main_branch):
    repo = Repo(directorio_repositorio)
    lista_commits = list(repo.iter_commits(main_branch))
    return lista_commits

def Transform(lista_commits):
    mensajes_commits = []
    for i in range(len(lista_commits)):
        mensajes_commits.append(lista_commits[i].message)
    df_commits =  pd.DataFrame(list(zip(lista_commits, mensajes_commits)), columns=['Commit', 'Mensaje'])
    return df_commits

def Load(df, nombre_repo):
    GREEN = "\033[38;5;40m"
    BLUE = "\033[5;36m"
    END = "\033[m"
    Possibles_leaks = ['password', 'pwd', 'contraseña', 'contrase&ntildea', 'key']
    leaks = []
    for i in range(len(df)):
        mensaje = df['Mensaje'][i]
        id_commit = df['Commit'][i]
        for leak in Possibles_leaks:
            if re.search(leak, mensaje, re.IGNORECASE):
                print('Se ha encontrado un leak en el commit ' + BLUE + f'{id_commit}' + END + '.')
                leaks.append(id_commit)
    print(GREEN + f'Se ha acabado la busqueda de leaks en los commits del repositorio {nombre_repo}.\n' + END)
    return leaks


def handler_signal(signal, frame):
    print('\nSE HA INTERRUMPIDO LA EJECUCION DEL PROGRAMA.\n\nSALIENDO...\n')
    sys.exit(1)

signal.signal(signal.SIGINT, handler_signal)


if __name__ == '__main__':
    directorio_repo1 = './skale/skale-manager'
    main_branch1 = 'develop'
    directorio_repo2 = './django-redis'
    main_branch2 = 'master'
    lista_commits1 = Extract(directorio_repo1, main_branch1)
    df_commits1 = Transform(lista_commits1)
    dict_leaks1 = Load(df_commits1, 'skale-manage')

    lista_commits2 = Extract(directorio_repo2, main_branch2)
    df_commits2 = Transform(lista_commits2)
    dict_leaks2 = Load(df_commits2, 'django-redis')