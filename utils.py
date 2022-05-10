from obra import Obra
from datetime import datetime, timedelta


def alarmas(uoc, credentials, seg):
    for datos_obra in uoc.obras:
        id_acciona = datos_obra['id_acciona']
        localizacion = datos_obra['localizacion']
        url = 'http://' + datos_obra['direccion']
        username, password = credentials.get(id_acciona)
        obra = Obra(id_acciona, localizacion,
                    url, username, password)
        for alarma in obra.get_alarmas(seg):
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
