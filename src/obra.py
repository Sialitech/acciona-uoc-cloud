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

    def get_alarmas(self, seconds=""):
        """Devuelve las alarmas

        Args:
            seconds (str, optional): si tiene valor, devuelve las alarmas que
            llevan mas de X segundos

        Returns:
            list[dict]: lista de las alarmas
        """
        url = "{}{}{}".format(self.url, '/api/alarmas/', seconds)
        return self.session.get(url).json()

    def get_visualizaciones(self, interval=""):
        """Devuelve las visualizaciones

        Args:
            interval (str, optional): si tiene valor, devuelve las
            visualizaciones comprendidas entre horas, ejem: 10-14

        Returns:
            list[dict]: lista de visualizaciones
        """
        url = "{}{}{}".format(self.url, '/api/visualizaciones/', interval)
        return self.session.get(url).json()
