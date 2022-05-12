from datetime import datetime
from obra import Obra
from datetime import datetime, timedelta
import re
import logging


logging.basicConfig(
    format='%(asctime)-5s %(levelname)-8s %(message)s',
    level=logging.INFO,
)


def alarmas(uoc, credentials, seconds):
    """Busca en las obras alarmas y las añade en el uoc, si no existen.

    Args:
        uoc (UOC): instancia de la clase UOC.
        credentials (dic): diccionario con las credenciales para acceder a las
        obras.
        seconds (int): parametro para mostar las alarmas de la obra en los
        ultimos X segundos.
    """
    for datos_obra in uoc.obras:
        id_acciona = datos_obra['id_acciona']
        localizacion = datos_obra['localizacion']
        url = 'http://' + datos_obra['direccion']
        username, password = credentials.get(id_acciona)
        obra = Obra(id_acciona, localizacion,
                    url, username, password)
        for alarma in obra.get_alarmas(seconds):
            tipo = alarma['tipo']['tipo']
            fecha = alarma['fecha_activacion']
            exist = uoc.exist_alarma(
                id_acciona, tipo, fecha)
            if not(exist):
                data = {
                    "obra": id_acciona,
                    "tipo": tipo,
                    "fecha_activacion": fecha
                }
                result = uoc.post_alarma(data=data)
                logging.info("guardado_alarm: %s", result)


def visualizaciones(uoc, credentials, horas):
    """Busca en las obras visualizaciones y las añade en el uoc, si no existen,
    si existe actualiza los datos.

    Args:
        uoc (UOC): instancia de la clase UOC.
        credentials (dic): diccionario con las credenciales para acceder a las
        obras.
        interval (str): intervalor para las visualizaciones. ejemplo: 9-14
    """
    interval = intervalo_horas(horas)
    for datos_obra in uoc.obras:
        id_acciona = datos_obra['id_acciona']
        localizacion = datos_obra['localizacion']
        url = 'http://' + datos_obra['direccion']
        username, password = credentials.get(id_acciona)
        obra = Obra(id_acciona, localizacion,
                    url, username, password)
        for visualizacion in obra.get_visualizaciones(interval):
            tipo = visualizacion['tipo']['tipo']
            valor = visualizacion['valor']
            id_visualizacion, valor_old = uoc.exist_visualizacion(
                id_acciona, tipo)
            if id_visualizacion:
                if valor != valor_old:
                    data = {
                        "id": id_visualizacion,
                        "obra": id_acciona,
                        "tipo": tipo,
                        "valor": valor
                    }
                    result = uoc.put_visualizacion(
                        data=data, id=id_visualizacion)
                    logging.info("update_visual: %s", result)
            else:
                data = {
                    "obra": id_acciona,
                    "tipo": tipo,
                    "valor": valor
                }
                result = uoc.post_visualizacion(data=data)
                logging.info("guardado_visual: %s", result)


def borrar_alarmas(uoc, seconds):
    """Bora las alarmas que llevan mas de X segundos

    Args:
        uoc (UOC): instancia de la clase UOC.
        seconds (int): parametro para borrar las alarmas del uoc llevan mas de
        X segundos.
    """
    alarmas, status_code = uoc.get_alarmas()
    fecha_limite = datetime.now() - timedelta(seconds=seconds)
    if status_code == 200:
        for alarma in alarmas:
            if(alarma['fecha_activacion'] < fecha_limite.timestamp()):
                delete = uoc.delete_alarma(alarma['obra'], alarma['id'])
                logging.info("Borrando: {}, Status: {}".format(
                    alarma, delete.status_code))
    else:
        logging.info("error: %s", alarmas)


def intervalo_horas(horas):
    """conseguir el intervalo de las visualizaciones dado el numero de horas.
    Dicho intervalo será desde la hora actual hasta intervalo_horas menos.
    Si son más de y media (ya han pasado más de 30 minutos de la hora actual),
    se calcula el intervalo contando la próxima hora.
    e.g. si son las 10:31 y intervalo_horas=2, entonces intervalo=9-11
    e.g. si son las 10:29 y intervalo_horas=2, entonces intervalo=8-10

    Args:
        horas (int): numero de horas para calcular el intervalo.
    Returns:
        str: intervalo visualizaciones. e.g. "10-11", "14-17", "11-13", "5-9".
    """
    now = datetime.now()
    if now.minute < 30:
        hora_inicial = now.hour
    else:
        hora_inicial = now.hour + 1
    intervalo = "{}-{}".format(hora_inicial - horas, hora_inicial)
    return intervalo


def format_url(url):
    if not re.match('(?:http)://', url):
        return 'http://{}'.format(url)
    return url
