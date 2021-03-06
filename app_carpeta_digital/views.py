import os
from shutil import copy2
from django.contrib import messages
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.views import View

from app_carpeta_digital.utils import validar_ciudadano
from operador_origen.settings import CARPETA_BUS
from .models import Cliente, OperadorDestino, Documento


class IndexView(View):
    def get(self, request):
        return redirect('app_carpeta_digital:clientes')


class ClientesView(View):
    def get(self, request):
        return render(request, 'app_carpeta_digital/clientes.html', {
            'clientes': Cliente.objects.all()
        })


class ClienteView(View):
    def get(self, request, id_cliente):
        cliente: Cliente = Cliente.objects.filter(id=id_cliente).first()
        if cliente:
            return render(request, 'app_carpeta_digital/cliente.html', {
                'cliente': cliente,
                'documentos': cliente.documento_set.all(),
                'operadores': OperadorDestino.objects.all()
            })
        else:
            return redirect('app_carpeta_digital:index')

    def post(self, request, id_cliente):
        cliente: Cliente = Cliente.objects.filter(id=id_cliente).first()
        if cliente:
            id_documento = request.POST.get('id_documento', '')
            id_operador = request.POST.get('id_operador', '')
            if id_documento and id_operador:
                operador: OperadorDestino = OperadorDestino.objects.filter(id=id_operador).first()
                documento: Documento = cliente.documento_set.filter(id=id_documento).first()
                if operador and documento:
                    source = documento.archivo.path
                    destination = os.path.join(CARPETA_BUS)
                    try:
                        os.makedirs(destination)
                    except:
                        pass
                    copy2(source, os.path.join(destination, os.path.basename(source)))
                    success = f'El documento "{documento.nombre}"" fue enviado al operador "{operador.nombre}"'
                    messages.success(request, success)
                else:
                    messages.error(request, 'El operador o el documento no son válidos')
            else:
                messages.warning(request, 'Todos los campos son obligatorios')
        else:
            messages.error(request, 'El cliente no existe')
        return self.get(request, id_cliente)


class CrearClienteView(View):
    def get(self, request):
        return render(request, 'app_carpeta_digital/crear_cliente.html', {})

    @atomic
    def post(self, request):
        cedula = request.POST.get('cedula', '')
        nombres = request.POST.get('nombres', '')
        apellidos = request.POST.get('apellidos', '')
        email = request.POST.get('email', '')
        if cedula and nombres and apellidos and email:
            existe_cedula = Cliente.objects.filter(cedula=cedula).first()
            if not existe_cedula:
                existe_email = Cliente.objects.filter(email=email).first()
                if not existe_email:
                    documento = validar_ciudadano(
                        email=email,
                        first_name=nombres,
                        last_name=apellidos,
                        id_number=cedula
                    )
                    if documento:
                        nuevo = Cliente(email=email, cedula=cedula, nombres=nombres, apellidos=apellidos)
                        nuevo.save()
                        messages.success(request, 'El cliente fue creado exitosamente')
                    else:
                        messages.error(request, 'Los datos no se encuentran registrados en la Registraduría')
                else:
                    messages.warning(request, 'Ya existe un cliente con el correo electrónico ingresado')
                    return self.get(request)
            else:
                messages.warning(request, 'Ya existe un cliente con la cédula ingresada')
                return self.get(request)

            return redirect('app_carpeta_digital:clientes')
        else:
            messages.warning(request, 'Todos los campos son obligatorios')
            return self.get(request)
