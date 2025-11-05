from django.contrib import admin
from .models import Categoria, Perfil, Doacao, Mensagem, Avaliacao


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'cidade', 'estado', 'avaliacao_media', 'total_doacoes']
    list_filter = ['tipo', 'estado']
    search_fields = ['usuario__username', 'cidade']


@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'doador', 'categoria', 'status', 'urgencia', 'cidade', 'data_criacao']
    list_filter = ['status', 'urgencia', 'categoria', 'estado']
    search_fields = ['titulo', 'descricao', 'doador__username']
    date_hierarchy = 'data_criacao'


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ['remetente', 'destinatario', 'doacao', 'data_envio', 'lida']
    list_filter = ['lida', 'data_envio']
    search_fields = ['remetente__username', 'destinatario__username', 'texto']


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['avaliador', 'avaliado', 'doacao', 'nota', 'data_avaliacao']
    list_filter = ['nota', 'data_avaliacao']
    search_fields = ['avaliador__username', 'avaliado__username']
