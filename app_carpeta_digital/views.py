import os
from shutil import copy2
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from operador_origen.settings import CARPETA_BUS
from .models import Cliente, OperadorDestino, Documento


class IndexView(View):
    def get(self, request):
        return redirect('app_carpeta_digital:clientes')


class ClientesView(View):
    def get(self, request):
        return render(request, 'app_carpeta_digital/index.html', {
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
            ruta = request.POST.get('ruta', '')
            if id_documento and id_operador and ruta:
                operador: OperadorDestino = OperadorDestino.objects.filter(id=id_operador).first()
                documento: Documento = cliente.documento_set.filter(id=id_documento).first()
                if operador and documento:
                    source = documento.archivo.path
                    destination = os.path.join(CARPETA_BUS, operador.ruta_destino, ruta)
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
