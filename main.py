from datetime import datetime, timedelta
import requests
import schedule
import time


class Obra:
    def __init__(self, code, location, url, username, password):
        self.code = code
        self.location = location
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.session()
        self.login()

    def login(self):
        url = "{}{}".format(self.url, '/login/?username={}&password={}'.format(
            self.username, self.password))
        self.session.get(url)

    def get_alarmas(self, seg=""):
        url = "{}{}{}".format(self.url, '/api/alarmas/', seg)
        return self.session.get(url).json()

    def get_visualizaciones(self, interval=""):
        url = "{}{}{}".format(self.url, '/api/visualizaciones/', interval)
        return self.session.get(url).json()


class UOC:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.headers = None
        self.session = requests.session()
        self.token = self.generate_token()
        self.obras = self.get_obras()
        self.alarmas = None
        self.visualizaciones = None

    def generate_token(self):
        url = self.url + '/api-token-auth/'
        credentials = {'username': self.username, 'password': self.password}
        response = self.session.post(url, data=credentials)
        token = response.json().get('token')
        self.headers = {'Authorization': 'Token {}'.format(token)}
        return token

    def get_obras(self):
        obras = self.session.get(
            self.url + '/obras/', headers=self.headers).json()
        return obras

    def get_alarmas(self):
        alarmas = self.session.get(
            self.url + '/alarmas/', headers=self.headers)
        return alarmas.json(), alarmas.status_code

    def post_alarma(self, data):
        response = self.session.post(
            self.url + '/alarmas/', headers=self.headers, data=data)
        return response.json()

    def delete_alarma(self, id_acciona, id_alarma):
        url = self.url + '/alarmas/{}/{}/'.format(id_acciona, id_alarma)
        response = self.session.delete(url, headers=self.headers)
        return response

    def exist_alarma(self, id_obra, type, timestamp):
        url = '{}{}{}'.format(self.url, '/alarmas/', id_obra)
        alarmas = self.session.get(url, headers=self.headers).json()
        for alarma in alarmas:
            if (
                alarma['tipo']['nombre'] == type and
                alarma['fecha_activacion'] == timestamp
            ):
                return True
        return False

    def exist_visualizacion(self, id_obra, type, value):
        url = '{}{}'.format(self.url, '/visualizaciones/')
        visualizaciones = self.session.get(url, headers=self.headers).json()
        for visualizacion in visualizaciones:
            if (
                visualizacion['obra'] == id_obra and
                visualizacion['tipo']['nombre'] == type and
                visualizacion['valor'] == value
            ):
                return visualizacion['id']

    def post_visualizacion(self, data, id=None):
        url = "{}/visualizaciones/".format(self.url)
        response = self.session.post(
            url, headers=self.headers, data=data)
        return response.json()

    def put_visualizacion(self, data, id):
        url = "{}/visualizaciones/{}/".format(self.url, id)
        response = self.session.put(
            url, headers=self.headers, data=data)
        return response.json()


def alarmas(uoc, credentials, seg):
    for datos_obra in uoc.obras:
        id_acciona = datos_obra['id_acciona']
        localizacion = datos_obra['localizacion']
        url = 'http://' + datos_obra['direccion']
        # print("url_alarm: ", url)
        username, password = credentials.get(id_acciona)
        obra = Obra(id_acciona, localizacion,
                    url, username, password)
        for alarma in obra.get_alarmas(seg):
            # print("current_alarm: ", alarma)
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
        # print("url_visual: ", url)
        username, password = credentials.get(id_acciona)
        obra = Obra(id_acciona, localizacion,
                    url, username, password)
        for visualizacion in obra.get_visualizaciones(interval):
            # print("curret_visual: ", visualizacion)
            tipo = visualizacion['tipo']['tipo']
            valor = visualizacion['valor']
            id_visualizacion = uoc.exist_visualizacion(
                id_acciona, tipo, valor)
            if id_visualizacion:
                data = {
                    "id": id_visualizacion,
                    "obra": id_acciona,
                    "tipo": tipo,
                    "valor": valor
                }
                result = uoc.put_visualizacion(data=data, id=id_visualizacion)
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
    print("status_code: ", status_code)
    fecha_limite = datetime.now() - timedelta(seconds=seconds)
    if status_code == 200:
        for alarma in alarmas:
            if(alarma['fecha_activacion'] < fecha_limite.timestamp()):
                delete = uoc.delete_alarma(alarma['obra'], alarma['id'])
                print("Borrando: {}, Status: {}".format(
                    alarma, delete.status_code))
                
    else:
        print("error:", alarmas)
        

def main():
    CREDENTIALS = {
        'ES102': ['admin', 'admin']
    }
    SEG_ALARMAR = 10
    INTERVALO_VISUALIZACIONES = ''
    BORRAR_ALARMAS = 300

    uoc = UOC('http://localhost:80', 'admin', 'admin')
    schedule.every(10).seconds.do(alarmas, uoc, CREDENTIALS, SEG_ALARMAR)
    schedule.every(5).seconds.do(
        visualizaciones, uoc, CREDENTIALS, INTERVALO_VISUALIZACIONES)
    # schedule.every().hour.do(
    #     alarmas, uoc, CREDENTIALS, INTERVALO_VISUALIZACIONES)
    schedule.every(5).minutes.do(borrar_alarmas, uoc, BORRAR_ALARMAS)

    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
