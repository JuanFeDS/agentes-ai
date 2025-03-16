"""Modulo de Decoradores"""
import os
import inspect

from datetime import datetime

from Utils.functions import config_logging

FECHA = int(str(datetime.now()).replace('-', '')[:8])

def logging_decorator(func):
    """
    Este módulo proporciona un decorador para agregar registros (logging) a los scripts que se 
    ejecutan en el programa. Utiliza un decorador que envuelve la función objetivo para generar 
    mensajes de logging en los niveles de información y error, incluyendo detalles de 
    inicialización, finalización exitosa, y manejo de excepciones.

    Attributes:
        FECHA (int): Fecha actual en formato YYYYMMDD, usada para nombrar los archivos de log.

    Functions:
        logging_decorator(func): Decorador para agregar registros detallados a las funciones.
    """

    logger = config_logging(FECHA)
    script_name = os.path.basename(inspect.getfile(func))

    def wrapper(*args, **kwargs):
        logger.info(lambda: f"Inicializando el script {script_name}.")
        try:
            result = func(*args, **kwargs)
            logger.info(lambda: f"{script_name} ejecutado con exito.")
            return result
        except Exception as e:
            logger.error(lambda: f"Ocurrio un error con el script: {script_name}.")
            logger.error(lambda: f"{e}")
            raise ValueError(lambda: f"Ha ocurrido un error: {script_name}: {e}")

    return wrapper
