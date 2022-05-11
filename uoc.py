import requests


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
        """Obtiene el token para tener credenciales

        Returns:
            str: token
        """
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
        """Comprueba si la alama especificada existe o no

        Args:
            id_obra (str): identificador de la obra
            type (str): tipo de alarma
            timestamp (timestamp): fecha en que se creo la alarma

        Returns:
            boolean: devuelve True si existe y False sino se encontro
        """
        url = '{}{}{}'.format(self.url, '/alarmas/', id_obra)
        alarmas = self.session.get(url, headers=self.headers).json()
        for alarma in alarmas:
            if (
                alarma['tipo']['nombre'] == type and
                alarma['fecha_activacion'] == timestamp
            ):
                return True
        return False

    def exist_visualizacion(self, id_obra, type):
        """Comprueba si la visualizacion especificada existe o no

        Args:
            id_obra (str): identificador de la obra
            type (str): tipo de la visualizacion

        Returns:
            list: si existe devuelve el id y el valor de la visualizacion
        """
        url = '{}{}'.format(self.url, '/visualizaciones/')
        visualizaciones = self.session.get(url, headers=self.headers).json()
        for visualizacion in visualizaciones:
            if (
                visualizacion['obra'] == id_obra and
                visualizacion['tipo']['nombre'] == type
            ):
                return visualizacion['id'], visualizacion['valor']
        return None, None

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
