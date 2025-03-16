"""Modulo para conectarse a DWH Cloud"""

import os
import yaml

import pandas as pd

import cx_Oracle
import sqlalchemy as sa

from dotenv import load_dotenv

load_dotenv()

# Variables globales
try:
    ruta_config = './config/config.yml'
    with open(ruta_config, "r", encoding='utf-8') as archivo:
        config = yaml.safe_load(archivo)
except:
    ruta_config = '../config/config.yml'
    with open(ruta_config, "r", encoding='utf-8') as archivo:
        config = yaml.safe_load(archivo)

# Variables para la conexión
ruta_instantclient = config['rutas']['ruta_instantclient']

dsn_con = os.getenv('dwh_dsn')
usuario = os.getenv('dwh_user')
password = os.getenv('dwh_password')

# Conexión con la base de datos - CX_Oracle
cx_Oracle.init_oracle_client(lib_dir=ruta_instantclient)

conn = cx_Oracle.connect(user=f'{usuario}', password=f'{password}', dsn=dsn_con)
cur = conn.cursor()

# Funciones
def consulta(query: str) -> pd.DataFrame:
    """Ejecuta un query SQL que retorna un dataframe

    Args:
        query (str): Query a ejecutar

    Returns:
        pd.DataFrame: Dataframe resultante de la consulta
    """
    # Lectura del query
    df = pd.read_sql(query, con=conn)
    return(df)

def registro_to_dwh(df: pd.DataFrame, query: str):
    """Carga los registros de un DataFrame en el DWH

    Args:
        df (pd.DataFrame): DataFrame a cargar
        query (str): Query de inserción
    """
    # Convertir DataFrame a lista de tuplas con valores convertidos a str y truncados
    rows = [tuple(str(val)[:2000] for val in row) for row in df.values]

    total_rows = len(rows)
    chunksize = 5000

    # Inserción de los registros
    for i in range(0, total_rows, chunksize):
        chunk = rows[i:i+chunksize]
        cur.executemany(query, chunk)
        conn.commit()

def ejecutar_procedimiento(procedimiento: str):
    """Ejecuta un procedimiento SQL con parámetros

    Args:
        procedimiento (str): Nombre del procedimiento
    """
    cur.callproc(procedimiento)
    conn.commit()

def ejecutar_procedimiento_parametros(procedimiento: str, parametros: list):
    """Ejecuta un procedimiento SQL con parámetros

    Args:
        procedimiento (str): Nombre del procedimiento
        parametros (list): Lista de parámetros
    """
    cur.callproc(procedimiento, parametros)
    conn.commit()

def ejecutar_query(query: str):
    """Ejecuta un bloque de código SQL

    Args:
        query (str): Query SQL
    """
    cur.execute(query)
    conn.commit()

def cerrar_conexion():
    """Cerrar la conexión"""
    conn.close()
