from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Pontos de Coleta
    path('pontos-coleta/', views.ponto_coleta_list, name='ponto_coleta_list'),
    path('ponto-coleta/<int:pk>/', views.ponto_coleta_detail, name='ponto_coleta_detail'),
    path('ponto-coleta/criar/', views.ponto_coleta_criar, name='ponto_coleta_criar'),
    path('ponto-coleta/<int:pk>/editar/', views.ponto_coleta_editar, name='ponto_coleta_editar'),
    path('ponto-coleta/<int:pk>/excluir/', views.ponto_coleta_excluir, name='ponto_coleta_excluir'),
    path('meu-ponto-coleta/', views.meu_ponto_coleta, name='meu_ponto_coleta'),
    
    # Estoque
    path('ponto-coleta/<int:ponto_id>/item/criar/', views.item_estoque_criar, name='item_estoque_criar'),
    path('item/<int:pk>/editar/', views.item_estoque_editar, name='item_estoque_editar'),
    path('item/<int:pk>/excluir/', views.item_estoque_excluir, name='item_estoque_excluir'),
    path('meu-estoque/', views.meu_estoque, name='meu_estoque'),
    
    # Solicitações
    path('item/<int:item_id>/solicitar/', views.solicitacao_criar, name='solicitacao_criar'),
    path('minhas-solicitacoes/', views.minhas_solicitacoes, name='minhas_solicitacoes'),
    path('gerenciar-solicitacoes/', views.gerenciar_solicitacoes, name='gerenciar_solicitacoes'),
    path('solicitacao/<int:pk>/aprovar/', views.solicitacao_aprovar, name='solicitacao_aprovar'),
    path('solicitacao/<int:pk>/recusar/', views.solicitacao_recusar, name='solicitacao_recusar'),
    path('solicitacao/<int:pk>/concluir/', views.solicitacao_concluir, name='solicitacao_concluir'),
    path('solicitacao/<int:pk>/cancelar/', views.solicitacao_cancelar, name='solicitacao_cancelar'),
    
    # Comunidade
    path('comunidade/', views.comunidade, name='comunidade'),
    path('comunidade/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('comunidade/post/criar/', views.post_criar, name='post_criar'),
    path('comunidade/post/<int:pk>/editar/', views.post_editar, name='post_editar'),
    path('comunidade/post/<int:pk>/excluir/', views.post_excluir, name='post_excluir'),
    
    # Comentários
    path('post/<int:post_id>/comentario/', views.comentario_criar, name='comentario_criar'),
    path('comentario/<int:pk>/editar/', views.comentario_editar, name='comentario_editar'),
    path('comentario/<int:pk>/excluir/', views.comentario_excluir, name='comentario_excluir'),
    path('comentario/<int:pk>/responder/', views.comentario_responder, name='comentario_responder'),
    
    # Perfil e Autenticação
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
]
