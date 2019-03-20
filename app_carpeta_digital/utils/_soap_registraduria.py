from zeep import Client

from operador_origen.settings import REGISTRADURIA_WSDL_PATH

client = Client(REGISTRADURIA_WSDL_PATH)


def validar_ciudadano(email: str, first_name: str, last_name: str, id_number: str):
    return client.service.validateClient({
        'email': email,
        'firstName': first_name,
        'lastName': last_name,
        'idNumber': id_number
    })
