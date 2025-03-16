from datetime import datetime

import pandas as pd
import numpy as np

from Utils.functions import send_message, config_logging

def run(config: dict, fecha: datetime):

    # Variables globales
    dia = int(str(fecha).replace('-', '')[:8])

    logger = config_logging(dia)
    logger.info('Ejecutando generación de bases')

    print(f'Ejecutando generación de bases el {dia}')
    print(config)
