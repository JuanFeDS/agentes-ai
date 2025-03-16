import yaml
from datetime import datetime, timedelta

from src import generacion_bases

from Utils.functions import send_message, config_logging

# Variables Globales
fecha = datetime.now()

dia = int(str(fecha).replace('-', '')[:8])
mes = int(str(fecha).replace('-', '')[:6])

# Archivo de configuración
ruta_config = './config/config.yml'
with open(ruta_config, "r") as archivo:
    config = yaml.safe_load(archivo)

# Función principal
def main():
    logger = config_logging(dia)
    logger.info('Empieza la ejecución')

    print('Hello World')

    logger.info('Generando bases...')
    generacion_bases.run(config, fecha)

# Entry Point
if __name__ == '__main__':
    main()