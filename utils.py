from obra import Obra
from datetime import datetime, timedelta


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
                print("guardado_alarm: ", result)


def visualizaciones(uoc, credentials, interval):
    """Busca en las obras visualizaciones y las añade en el uoc, si no existen,
    si existe acutaliza los datos.

    Args:
        uoc (UOC): instancia de la clase UOC.
        credentials (dic): diccionario con las credenciales para acceder a las
        obras.
        interval (_type_): _description_
    """
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
                    print("update_visual: ", result)
            else:
                data = {
                    "obra": id_acciona,
                    "tipo": tipo,
                    "valor": valor
                }
                result = uoc.post_visualizacion(data=data)
                print("guardado_visual: ", result)


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
                print("Borrando: {}, Status: {}".format(
                    alarma, delete.status_code))
    else:
        print("error:", alarmas)
