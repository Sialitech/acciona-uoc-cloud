from datetime import datetime, timedelta
import requests


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
        self.session = requests.session()
        self.token = self.generate_token()
        self.obras = self.get_obras()

    def generate_token(self):
        url = self.url + '/api-token-auth/'
        credentials = {'username': self.username, 'password': self.password}
        response = self.session.post(url, data=credentials)
        return response.json().get('token')

    def get_obras(self):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        obras = self.session.get(
            self.url + '/obras/', headers=headers).json()
        return obras
    
    def post_alarma(self, data):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        response = self.session.post(
            self.url + '/alarmas/', headers=headers, data=data)
        return response.json()

    def post_visualizacion(self, data):
        headers = {'Authorization': 'Token {}'.format(self.token)}
        response = self.session.post(
            self.url + '/visualizaciones/', headers=headers, data=data)
        return response.json()


def off_alarmas(alarmas_totales, alarmas_activas):
    for id_acciona, alarmas in alarmas_activas.items():
        alarmas = alarmas_totales.get(id_acciona)
    if alarmas:
        for id_alarma in alarmas:
            del alarmas[id_alarma]
    return alarmas_totales


def between_dates_js(date, interval):
    date_increment = date + timedelta(minutes=interval)
    date_1 = round(date.timestamp()*1000)
    date_2 = round(date_increment.timestamp()*1000)
    return date_1, date_2


def main():
    CREDENTIALS = {
        'ES102': ['admin', 'admin']
    }
    SEG_ALARMAR = ''
    INTERVALO_VISUALIZACIONES = ''
    DATE_INCREMENT_MIN = 5

    uoc = UOC('http://localhost:8000', 'admin', 'admin')
    # print("{}, {}".format(uoc.token, uoc.obras))

    for datos_obra in uoc.obras:
        url = 'http://' + datos_obra['direccion']
        username, password = CREDENTIALS.get('ES102')
        obra = Obra(datos_obra['id_acciona'], datos_obra['localizacion'],
                    url, username, password)
        alarmas = obra.get_alarmas(SEG_ALARMAR)
        visualizaciones = obra.get_visualizaciones(INTERVALO_VISUALIZACIONES)
        for alarma in alarmas:
            data = {
                "obra": datos_obra['id_acciona'],
                "tipo": alarma['tipo']['tipo'],
                "fecha_activacion": alarma['fecha_activacion']
            }
            result = uoc.post_alarma(data=data)
            print(result)

        for visualizacion in visualizaciones:
            print(visualizacion)
            data = {
                "obra": datos_obra['id_acciona'],
                "tipo": visualizacion['tipo']['tipo'],
                "valor": visualizacion['valor']
            }
            result = uoc.post_visualizacion(data=data)
            print(result)


    
    # session_ouc, obras = get_response(URL_UOC + '/obras/', session_ouc, token)
    # print(obras)
    # session, alarmas = get_alarmas(token, None, obras, 3000)
    # print(alarmas)


    # for key, value in alarmas.items():
    #     post_request(URL_UOC + '/alarmas/', token, data=value)

    # visualizaciones = get_visualizaciones(URL_UOC, token)
    # for key, value in visualizaciones.items():
    #     post_request(URL_UOC + '/visualizaciones/', token, data=value)

    # fecha_ini, fecha_fin = between_dates_js(datetime.now(), DATE_INCREMENT_MIN)
    # alarmas_activas = get_alarmas(URL_UOC, token, fecha_ini=fecha_ini, fecha_fin=fecha_fin)

    # alarmas_destivadas = off_alarmas(alarmas_totales, alarmas_activas)
    # for id_alarma in alarmas_destivadas:
    #     post_delete(URL_UOC + '/alarmas/', token, data=id_alarma):


if __name__ == "__main__":
   main()
