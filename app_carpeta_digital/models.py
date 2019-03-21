from django.db import models


class OperadorDestino(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Operador destino'
        verbose_name_plural = 'Operadores destino'


class Cliente(models.Model):
    cedula = models.CharField(max_length=100, unique=True, verbose_name='Cédula')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


def ruta_archivo_cliente(instance, filename):
    cedula = instance.fk_cliente.cedula
    return f'{cedula}_{filename}'


class Documento(models.Model):
    fk_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    archivo = models.FileField(upload_to=ruta_archivo_cliente, verbose_name='Archivo')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
