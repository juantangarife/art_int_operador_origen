from django.urls import path

from .views import IndexView, ClienteView, ClientesView, CrearClienteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clientes', ClientesView.as_view(), name='clientes'),
    path('clientes/<int:id_cliente>', ClienteView.as_view(), name='cliente'),
    path('crear-cliente', CrearClienteView.as_view(), name='crear-cliente')
]
