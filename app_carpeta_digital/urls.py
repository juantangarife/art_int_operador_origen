from django.urls import path

from .views import IndexView, ClienteView, ClientesView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('clientes', ClientesView.as_view(), name='clientes'),
    path('clientes/<int:id_cliente>', ClienteView.as_view(), name='cliente')
]
