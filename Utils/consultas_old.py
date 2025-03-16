import pandas as pd
import numpy as np

import cx_Oracle
import sqlalchemy as sa

import yaml

# Variables globales
ruta_config = './config/config.yml'
with open(ruta_config, "r") as archivo:
    config = yaml.safe_load(archivo)

# Variables para la conexión
ruta_instantclient = config['rutas']['ruta_instantclient']

service_name = config['credenciales']['dwh_onpremise']['service_name']
ip = config['credenciales']['dwh_onpremise']['ip']
port = config['credenciales']['dwh_onpremise']['port']

usuario = config['credenciales']['dwh_onpremise']['usuario']
password = config['credenciales']['dwh_onpremise']['password']

def consulta(query):
    # Conexión con la base de datos - CX_Oracle
    cx_Oracle.init_oracle_client(config_dir = ruta_instantclient)
    dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
    conn = cx_Oracle.connect(user=usuario, password=password, dsn=dsn_tns)
    cur = conn.cursor()

    # Lectura del query
    df = pd.read_sql(query, con=conn)
    return(df)

def registro_to_dwh(df, query):
    # Conexión con la base de datos - CX_Oracle
    cx_Oracle.init_oracle_client(config_dir = ruta_instantclient)
    dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
    conn = cx_Oracle.connect(user=usuario, password=password, dsn=dsn_tns)
    cur = conn.cursor()

    # Conexión con sqlalchemy
    oracle_db = sa.create_engine(f'oracle+cx_oracle://{usuario}:{password}@{ip}:{port}/?service_name={service_name}')
    connection = oracle_db.connect()

    # Convertir DataFrame a lista de tuplas con valores convertidos a str y truncados
    rows = [tuple(str(val)[:2000] for val in row) for row in df.values]

    total_rows = len(rows)
    chunksize = 5000

    # Inserción de los registros
    for i in range(0, total_rows, chunksize):
        chunk = rows[i:i+chunksize]
        cur.executemany(query, chunk)
        conn.commit()

    # Cerramos la conexión
    conn.close()