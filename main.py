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
        self.alarmas = {}
        self.visualizaciones = {}

    def alarmas(self, seg=""):
        url = "{}{}{}".format(self.url, '/api/alarmas/', seg)
        self.alarmas = self.session.get(url).json()
    
    def visualizaciones(self, interval=""):
        url = "{}{}{}".format(self.url, '/api/visualizaciones/', interval)
        self.visualizaciones = self.session.get(url).json()


class UOC:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.session()
        self.token = None
        self.generate_token()
        self.obras = {}

    def generate_token(self):
        url = self.url + '/api-token-auth/'
        credentials = {'username': self.username, 'password': self.password}
        response = self.session.post(url, data=credentials)
        self.token = response.json().get('token')


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
    # OBRAS = {}
    DATE_INCREMENT_MIN = 5

    uoc = UOC('http://localhost:8000', 'admin', 'admin')
    print("{}, {}".format(uoc.token, uoc.session))
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
