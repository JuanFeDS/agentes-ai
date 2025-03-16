import logging
import requests

def config_logging(dia, append=True):
    # Especificamos el formato del logging
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

    # Definimos el modo de escritura
    filemode = 'a' if append == True else 'w'

    # Configuramos nuestro logging
    logging.basicConfig(
        filename=f'./Log/log_{dia}.log',
        level=logging.INFO,
        format=LOG_FORMAT,
        filemode=filemode,
        encoding='utf-8'
    )

    # Inicializamos el logging
    logger = logging.getLogger()

    return logger

def send_message(id, message):
    # Ajustamos la solicitud de envio
    result = requests.post(
        id, 
        json={
            'text': message,
        }
    )
