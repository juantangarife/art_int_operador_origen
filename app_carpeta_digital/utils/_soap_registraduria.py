from zeep import Client

from operador_origen.settings import REGISTRADURIA_WSDL_PATH

client = Client(REGISTRADURIA_WSDL_PATH)


def validar_ciudadano(cedula):
    pass  # client.service.addClient
