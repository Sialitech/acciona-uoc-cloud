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
