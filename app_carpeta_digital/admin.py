from django.contrib import admin

from app_carpeta_digital.models import OperadorDestino, Cliente, Documento


class OperadorDestinoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    list_display_links = ('id', 'nombre')


class ClienteAdmin(admin.ModelAdmin):
    class DocumentoInline(admin.TabularInline):
        model = Documento
        extra = 0
    list_display = ('id', 'cedula', 'nombres', 'apellidos', 'email')
    list_display_links = ('id', 'cedula')
    inlines = (DocumentoInline,)


admin.site.register(OperadorDestino, OperadorDestinoAdmin)
admin.site.register(Cliente, ClienteAdmin)
