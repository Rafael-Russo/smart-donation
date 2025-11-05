from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doacao/<int:pk>/', views.doacao_detalhe, name='doacao_detalhe'),
    path('doacao/nova/', views.doacao_criar, name='doacao_criar'),
    path('doacao/<int:pk>/editar/', views.doacao_editar, name='doacao_editar'),
    path('doacao/<int:pk>/reservar/', views.doacao_reservar, name='doacao_reservar'),
    path('minhas-doacoes/', views.minhas_doacoes, name='minhas_doacoes'),
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('buscar/', views.buscar, name='buscar'),
]
