from django.contrib import admin
from .models import (
    Categoria, Perfil, Doacao, Mensagem, Avaliacao,
    PontoColeta, ItemEstoque, SolicitacaoRetirada,
    PostComunidade, ComentarioPost
)


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


@admin.register(PontoColeta)
class PontoColetaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel', 'cidade', 'estado', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'estado', 'cidade']
    search_fields = ['nome', 'responsavel__username', 'cidade', 'bairro']
    date_hierarchy = 'data_criacao'
    readonly_fields = ['data_criacao', 'data_atualizacao']


class ItemEstoqueInline(admin.TabularInline):
    model = ItemEstoque
    extra = 0
    fields = ['titulo', 'categoria', 'quantidade', 'quantidade_disponivel', 'status']
    readonly_fields = ['quantidade_disponivel']


@admin.register(ItemEstoque)
class ItemEstoqueAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ponto_coleta', 'doador', 'categoria', 'quantidade', 'quantidade_disponivel', 'status', 'urgencia']
    list_filter = ['status', 'urgencia', 'categoria', 'ponto_coleta']
    search_fields = ['titulo', 'descricao', 'doador__username', 'ponto_coleta__nome']
    date_hierarchy = 'data_criacao'
    readonly_fields = ['data_criacao', 'data_atualizacao', 'visualizacoes']


@admin.register(SolicitacaoRetirada)
class SolicitacaoRetiradaAdmin(admin.ModelAdmin):
    list_display = ['solicitante', 'item', 'tipo', 'quantidade_solicitada', 'status', 'data_solicitacao']
    list_filter = ['status', 'tipo', 'data_solicitacao']
    search_fields = ['solicitante__username', 'item__titulo']
    date_hierarchy = 'data_solicitacao'
    readonly_fields = ['data_solicitacao', 'data_resposta', 'data_conclusao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('item', 'solicitante', 'tipo', 'quantidade_solicitada')
        }),
        ('Endereço de Entrega', {
            'fields': ('endereco_entrega', 'cidade_entrega', 'estado_entrega'),
            'classes': ('collapse',)
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacao_solicitante', 'observacao_responsavel')
        }),
        ('Datas', {
            'fields': ('data_solicitacao', 'data_resposta', 'data_conclusao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PostComunidade)
class PostComunidadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ponto_coleta', 'fixado', 'visualizacoes', 'total_comentarios', 'data_criacao']
    list_filter = ['fixado', 'data_criacao', 'ponto_coleta']
    search_fields = ['titulo', 'conteudo', 'autor__username', 'tags']
    date_hierarchy = 'data_criacao'
    readonly_fields = ['visualizacoes', 'data_criacao', 'data_atualizacao']


@admin.register(ComentarioPost)
class ComentarioPostAdmin(admin.ModelAdmin):
    list_display = ['autor', 'post', 'data_criacao', 'resposta_a']
    list_filter = ['data_criacao']
    search_fields = ['autor__username', 'texto', 'post__titulo']
    date_hierarchy = 'data_criacao'
    readonly_fields = ['data_criacao', 'data_atualizacao']
