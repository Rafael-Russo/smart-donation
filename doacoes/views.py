from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Doacao, Categoria, Perfil, Mensagem, PontoColeta,
    ItemEstoque, SolicitacaoRetirada, PostComunidade, ComentarioPost
)
from .forms import (
    DoacaoForm, PerfilForm, MensagemForm, PontoColetaForm,
    ItemEstoqueForm, SolicitacaoRetiradaForm, PostComunidadeForm, ComentarioPostForm
)


# ===================== HOME =====================
def home(request):
    """Página inicial com estatísticas e destaques"""
    # Estatísticas
    total_pontos = PontoColeta.objects.filter(ativo=True).count()
    total_itens = ItemEstoque.objects.filter(status='disponivel').count()
    total_solicitacoes = SolicitacaoRetirada.objects.count()
    total_usuarios = User.objects.count()
    
    # Pontos de coleta em destaque (3 mais recentes ativos)
    pontos_coleta = PontoColeta.objects.filter(ativo=True).select_related('responsavel')[:3]
    
    # Itens urgentes (máximo 4)
    itens_urgentes = ItemEstoque.objects.filter(
        status='disponivel',
        urgencia='alta'
    ).select_related('ponto_coleta', 'categoria')[:4]
    
    # Posts recentes (4 mais recentes)
    posts_recentes = PostComunidade.objects.select_related('autor', 'ponto_coleta')[:4]
    
    categorias = Categoria.objects.all()
    
    context = {
        'total_pontos': total_pontos,
        'total_itens': total_itens,
        'total_solicitacoes': total_solicitacoes,
        'total_usuarios': total_usuarios,
        'pontos_coleta': pontos_coleta,
        'itens_urgentes': itens_urgentes,
        'posts_recentes': posts_recentes,
        'categorias': categorias,
    }
    return render(request, 'doacoes/home.html', context)


# ===================== PONTOS DE COLETA =====================
def ponto_coleta_list(request):
    """Lista todos os pontos de coleta com filtros"""
    pontos = PontoColeta.objects.select_related('responsavel').annotate(
        total_itens=Count('itens')
    )
    
    # Filtros
    cidade = request.GET.get('cidade')
    estado = request.GET.get('estado')
    ativo = request.GET.get('ativo')
    
    if cidade:
        pontos = pontos.filter(cidade__icontains=cidade)
    if estado:
        pontos = pontos.filter(estado=estado)
    if ativo == 'true':
        pontos = pontos.filter(ativo=True)
    elif ativo == 'false':
        pontos = pontos.filter(ativo=False)
    
    context = {
        'pontos_coleta': pontos,
    }
    return render(request, 'doacoes/ponto_coleta_list.html', context)


def ponto_coleta_detail(request, pk):
    """Detalhes de um ponto de coleta"""
    ponto = get_object_or_404(PontoColeta, pk=pk)
    itens = ponto.itens.filter(status='disponivel').select_related('categoria', 'doador')
    
    context = {
        'ponto': ponto,
        'itens': itens,
    }
    return render(request, 'doacoes/ponto_coleta_detail.html', context)


@login_required
def ponto_coleta_criar(request):
    """Criar novo ponto de coleta"""
    if request.method == 'POST':
        form = PontoColetaForm(request.POST)
        if form.is_valid():
            ponto = form.save(commit=False)
            ponto.responsavel = request.user
            ponto.save()
            messages.success(request, 'Ponto de coleta criado com sucesso!')
            return redirect('ponto_coleta_detail', pk=ponto.pk)
    else:
        form = PontoColetaForm()
    
    context = {'form': form}
    return render(request, 'doacoes/ponto_coleta_form.html', context)


@login_required
def ponto_coleta_editar(request, pk):
    """Editar ponto de coleta"""
    ponto = get_object_or_404(PontoColeta, pk=pk, responsavel=request.user)
    
    if request.method == 'POST':
        form = PontoColetaForm(request.POST, instance=ponto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ponto de coleta atualizado com sucesso!')
            return redirect('ponto_coleta_detail', pk=ponto.pk)
    else:
        form = PontoColetaForm(instance=ponto)
    
    context = {'form': form}
    return render(request, 'doacoes/ponto_coleta_form.html', context)


@login_required
def ponto_coleta_excluir(request, pk):
    """Excluir ponto de coleta"""
    ponto = get_object_or_404(PontoColeta, pk=pk, responsavel=request.user)
    
    if request.method == 'POST':
        ponto.delete()
        messages.success(request, 'Ponto de coleta excluído com sucesso!')
        return redirect('ponto_coleta_list')
    
    return redirect('ponto_coleta_detail', pk=pk)


@login_required
def meu_ponto_coleta(request):
    """Visualizar meu ponto de coleta"""
    try:
        ponto = PontoColeta.objects.get(responsavel=request.user)
        return redirect('ponto_coleta_detail', pk=ponto.pk)
    except PontoColeta.DoesNotExist:
        messages.info(request, 'Você ainda não possui um ponto de coleta.')
        return redirect('ponto_coleta_criar')


# ===================== ESTOQUE =====================
@login_required
def item_estoque_criar(request, ponto_id):
    """Adicionar item ao estoque"""
    ponto = get_object_or_404(PontoColeta, pk=ponto_id, responsavel=request.user)
    
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.ponto_coleta = ponto
            item.doador = request.user
            item.save()
            messages.success(request, 'Item adicionado ao estoque!')
            return redirect('meu_estoque')
    else:
        form = ItemEstoqueForm()
    
    context = {
        'form': form,
        'ponto_coleta': ponto,
    }
    return render(request, 'doacoes/item_estoque_form.html', context)


@login_required
def item_estoque_editar(request, pk):
    """Editar item do estoque"""
    item = get_object_or_404(ItemEstoque, pk=pk, ponto_coleta__responsavel=request.user)
    
    if request.method == 'POST':
        form = ItemEstoqueForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            item.atualizar_disponibilidade()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('meu_estoque')
    else:
        form = ItemEstoqueForm(instance=item)
    
    context = {'form': form}
    return render(request, 'doacoes/item_estoque_form.html', context)


@login_required
def item_estoque_excluir(request, pk):
    """Excluir item do estoque"""
    item = get_object_or_404(ItemEstoque, pk=pk, ponto_coleta__responsavel=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item excluído com sucesso!')
        return redirect('meu_estoque')
    
    return redirect('meu_estoque')


@login_required
def meu_estoque(request):
    """Gerenciar estoque do meu ponto de coleta"""
    try:
        meu_ponto = PontoColeta.objects.get(responsavel=request.user)
    except PontoColeta.DoesNotExist:
        messages.warning(request, 'Você precisa criar um ponto de coleta primeiro.')
        return redirect('ponto_coleta_criar')
    
    itens = ItemEstoque.objects.filter(ponto_coleta=meu_ponto).select_related('categoria')
    
    # Filtros
    q = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    status = request.GET.get('status')
    
    if q:
        itens = itens.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q))
    if categoria_id:
        itens = itens.filter(categoria_id=categoria_id)
    if status:
        itens = itens.filter(status=status)
    
    # Estatísticas
    total_itens = itens.count()
    itens_disponiveis = itens.filter(status='disponivel').count()
    itens_reservados = itens.filter(status='reservado').count()
    itens_esgotados = itens.filter(status='esgotado').count()
    
    categorias = Categoria.objects.all()
    
    context = {
        'meu_ponto': meu_ponto,
        'itens': itens,
        'total_itens': total_itens,
        'itens_disponiveis': itens_disponiveis,
        'itens_reservados': itens_reservados,
        'itens_esgotados': itens_esgotados,
        'categorias': categorias,
    }
    return render(request, 'doacoes/meu_estoque.html', context)


# ===================== SOLICITAÇÕES =====================
@login_required
def solicitacao_criar(request, item_id):
    """Criar solicitação de retirada"""
    item = get_object_or_404(ItemEstoque, pk=item_id, status='disponivel')
    
    # Não permitir que o responsável solicite do próprio ponto
    if item.ponto_coleta.responsavel == request.user:
        messages.error(request, 'Você não pode solicitar itens do seu próprio ponto de coleta.')
        return redirect('ponto_coleta_detail', pk=item.ponto_coleta.pk)
    
    if request.method == 'POST':
        form = SolicitacaoRetiradaForm(request.POST, item=item)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.item = item
            solicitacao.solicitante = request.user
            solicitacao.save()
            messages.success(request, 'Solicitação enviada com sucesso!')
            return redirect('minhas_solicitacoes')
    else:
        form = SolicitacaoRetiradaForm(item=item)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'doacoes/solicitacao_form.html', context)


@login_required
def minhas_solicitacoes(request):
    """Listar minhas solicitações"""
    solicitacoes = SolicitacaoRetirada.objects.filter(
        solicitante=request.user
    ).select_related('item', 'item__ponto_coleta').order_by('-data_solicitacao')
    
    # Filtros
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    if tipo:
        solicitacoes = solicitacoes.filter(tipo=tipo)
    
    # Estatísticas
    pendentes = solicitacoes.filter(status='pendente').count()
    aprovadas = solicitacoes.filter(status='aprovada').count()
    concluidas = solicitacoes.filter(status='concluida').count()
    recusadas = solicitacoes.filter(status='recusada').count()
    
    context = {
        'solicitacoes': solicitacoes,
        'pendentes': pendentes,
        'aprovadas': aprovadas,
        'concluidas': concluidas,
        'recusadas': recusadas,
    }
    return render(request, 'doacoes/minhas_solicitacoes.html', context)


@login_required
def gerenciar_solicitacoes(request):
    """Gerenciar solicitações recebidas no meu ponto"""
    try:
        meu_ponto = PontoColeta.objects.get(responsavel=request.user)
    except PontoColeta.DoesNotExist:
        messages.warning(request, 'Você precisa criar um ponto de coleta primeiro.')
        return redirect('ponto_coleta_criar')
    
    solicitacoes = SolicitacaoRetirada.objects.filter(
        item__ponto_coleta=meu_ponto
    ).select_related('item', 'solicitante').order_by('-data_solicitacao')
    
    # Filtros
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    
    if status:
        solicitacoes = solicitacoes.filter(status=status)
    if tipo:
        solicitacoes = solicitacoes.filter(tipo=tipo)
    
    # Estatísticas
    pendentes = solicitacoes.filter(status='pendente').count()
    aprovadas = solicitacoes.filter(status='aprovada').count()
    concluidas = solicitacoes.filter(status='concluida').count()
    recusadas = solicitacoes.filter(status='recusada').count()
    
    context = {
        'meu_ponto': meu_ponto,
        'solicitacoes': solicitacoes,
        'pendentes': pendentes,
        'aprovadas': aprovadas,
        'concluidas': concluidas,
        'recusadas': recusadas,
    }
    return render(request, 'doacoes/gerenciar_solicitacoes.html', context)


@login_required
def solicitacao_aprovar(request, pk):
    """Aprovar solicitação"""
    solicitacao = get_object_or_404(
        SolicitacaoRetirada,
        pk=pk,
        item__ponto_coleta__responsavel=request.user,
        status='pendente'
    )
    
    if request.method == 'POST':
        observacao = request.POST.get('observacao', '')
        solicitacao.aprovar(observacao)
        messages.success(request, 'Solicitação aprovada!')
        return redirect('gerenciar_solicitacoes')
    
    return redirect('gerenciar_solicitacoes')


@login_required
def solicitacao_recusar(request, pk):
    """Recusar solicitação"""
    solicitacao = get_object_or_404(
        SolicitacaoRetirada,
        pk=pk,
        item__ponto_coleta__responsavel=request.user,
        status='pendente'
    )
    
    if request.method == 'POST':
        motivo = request.POST.get('observacao', '')
        solicitacao.recusar(motivo)
        messages.success(request, 'Solicitação recusada.')
        return redirect('gerenciar_solicitacoes')
    
    return redirect('gerenciar_solicitacoes')


@login_required
def solicitacao_concluir(request, pk):
    """Marcar solicitação como concluída (recebida)"""
    solicitacao = get_object_or_404(
        SolicitacaoRetirada,
        pk=pk,
        solicitante=request.user,
        status='aprovada'
    )
    
    if request.method == 'POST':
        solicitacao.concluir()
        messages.success(request, 'Item marcado como recebido!')
        return redirect('minhas_solicitacoes')
    
    return redirect('minhas_solicitacoes')


@login_required
def solicitacao_cancelar(request, pk):
    """Cancelar solicitação pendente"""
    solicitacao = get_object_or_404(
        SolicitacaoRetirada,
        pk=pk,
        solicitante=request.user,
        status='pendente'
    )
    
    if request.method == 'POST':
        solicitacao.status = 'cancelada'
        solicitacao.save()
        messages.success(request, 'Solicitação cancelada.')
        return redirect('minhas_solicitacoes')
    
    return redirect('minhas_solicitacoes')


# ===================== COMUNIDADE =====================
def comunidade(request):
    """Lista de posts da comunidade"""
    posts = PostComunidade.objects.select_related('autor', 'ponto_coleta').order_by('-data_criacao')
    posts_fixados = posts.filter(fixado=True)
    posts_normais = posts.filter(fixado=False)
    
    # Filtros
    q = request.GET.get('q')
    ponto_id = request.GET.get('ponto')
    
    if q:
        posts_normais = posts_normais.filter(
            Q(titulo__icontains=q) | Q(conteudo__icontains=q) | Q(tags__icontains=q)
        )
    if ponto_id:
        posts_normais = posts_normais.filter(ponto_coleta_id=ponto_id)
    
    pontos_coleta = PontoColeta.objects.filter(ativo=True)
    
    context = {
        'posts': posts_normais,
        'posts_fixados': posts_fixados,
        'pontos_coleta': pontos_coleta,
    }
    return render(request, 'doacoes/comunidade.html', context)


def post_detail(request, pk):
    """Detalhes de um post com comentários"""
    post = get_object_or_404(PostComunidade, pk=pk)
    post.visualizacoes += 1
    post.save(update_fields=['visualizacoes'])
    
    comentarios = post.comentarios.select_related('autor', 'resposta_a').order_by('data_criacao')
    
    context = {
        'post': post,
        'comentarios': comentarios,
    }
    return render(request, 'doacoes/post_detail.html', context)


@login_required
def post_criar(request):
    """Criar novo post"""
    if request.method == 'POST':
        form = PostComunidadeForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, 'Publicação criada com sucesso!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostComunidadeForm(user=request.user)
    
    context = {'form': form}
    return render(request, 'doacoes/post_form.html', context)


@login_required
def post_editar(request, pk):
    """Editar post"""
    post = get_object_or_404(PostComunidade, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = PostComunidadeForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicação atualizada!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostComunidadeForm(instance=post, user=request.user)
    
    context = {'form': form}
    return render(request, 'doacoes/post_form.html', context)


@login_required
def post_excluir(request, pk):
    """Excluir post"""
    post = get_object_or_404(PostComunidade, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Publicação excluída.')
        return redirect('comunidade')
    
    return redirect('post_detail', pk=pk)


@login_required
def comentario_criar(request, post_id):
    """Adicionar comentário a um post"""
    post = get_object_or_404(PostComunidade, pk=post_id)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            ComentarioPost.objects.create(
                post=post,
                autor=request.user,
                texto=texto
            )
            messages.success(request, 'Comentário adicionado!')
        return redirect('post_detail', pk=post_id)
    
    return redirect('post_detail', pk=post_id)


@login_required
def comentario_editar(request, pk):
    """Editar comentário"""
    comentario = get_object_or_404(ComentarioPost, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            comentario.texto = texto
            comentario.save()
            messages.success(request, 'Comentário atualizado!')
        return redirect('post_detail', pk=comentario.post.pk)
    
    return redirect('post_detail', pk=comentario.post.pk)


@login_required
def comentario_excluir(request, pk):
    """Excluir comentário"""
    comentario = get_object_or_404(ComentarioPost, pk=pk, autor=request.user)
    post_id = comentario.post.pk
    
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, 'Comentário excluído.')
        return redirect('post_detail', pk=post_id)
    
    return redirect('post_detail', pk=post_id)


@login_required
def comentario_responder(request, pk):
    """Responder a um comentário"""
    comentario_pai = get_object_or_404(ComentarioPost, pk=pk)
    
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            ComentarioPost.objects.create(
                post=comentario_pai.post,
                autor=request.user,
                texto=texto,
                resposta_a=comentario_pai
            )
            messages.success(request, 'Resposta adicionada!')
        return redirect('post_detail', pk=comentario_pai.post.pk)
    
    return redirect('post_detail', pk=comentario_pai.post.pk)


# ===================== PERFIL E AUTENTICAÇÃO =====================
@login_required
def perfil(request):
    """Visualizar e editar perfil"""
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    context = {
        'perfil': perfil,
        'form': form,
    }
    return render(request, 'doacoes/perfil.html', context)


def registro(request):
    """Registro de novo usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/registro.html', context)
