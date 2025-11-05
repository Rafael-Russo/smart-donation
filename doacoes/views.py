from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Doacao, Categoria, Perfil, Mensagem
from .forms import DoacaoForm, PerfilForm, MensagemForm


def home(request):
    """Página inicial com listagem de doações disponíveis"""
    doacoes = Doacao.objects.filter(status='disponivel').select_related('doador', 'categoria')[:12]
    categorias = Categoria.objects.all()
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    cidade = request.GET.get('cidade')
    urgencia = request.GET.get('urgencia')
    
    if categoria_id:
        doacoes = doacoes.filter(categoria_id=categoria_id)
    if cidade:
        doacoes = doacoes.filter(cidade__icontains=cidade)
    if urgencia:
        doacoes = doacoes.filter(urgencia=urgencia)
    
    context = {
        'doacoes': doacoes,
        'categorias': categorias,
    }
    return render(request, 'doacoes/home.html', context)


def doacao_detalhe(request, pk):
    """Detalhes de uma doação específica"""
    doacao = get_object_or_404(Doacao, pk=pk)
    doacao.visualizacoes += 1
    doacao.save(update_fields=['visualizacoes'])
    
    context = {
        'doacao': doacao,
    }
    return render(request, 'doacoes/doacao_detalhe.html', context)


@login_required
def doacao_criar(request):
    """Criar nova doação"""
    if request.method == 'POST':
        form = DoacaoForm(request.POST, request.FILES)
        if form.is_valid():
            doacao = form.save(commit=False)
            doacao.doador = request.user
            doacao.save()
            messages.success(request, 'Doação cadastrada com sucesso!')
            return redirect('doacao_detalhe', pk=doacao.pk)
    else:
        form = DoacaoForm()
    
    return render(request, 'doacoes/doacao_form.html', {'form': form})


@login_required
def doacao_editar(request, pk):
    """Editar doação existente"""
    doacao = get_object_or_404(Doacao, pk=pk, doador=request.user)
    
    if request.method == 'POST':
        form = DoacaoForm(request.POST, request.FILES, instance=doacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doação atualizada com sucesso!')
            return redirect('doacao_detalhe', pk=doacao.pk)
    else:
        form = DoacaoForm(instance=doacao)
    
    return render(request, 'doacoes/doacao_form.html', {'form': form, 'doacao': doacao})


@login_required
def doacao_reservar(request, pk):
    """Reservar uma doação"""
    doacao = get_object_or_404(Doacao, pk=pk, status='disponivel')
    
    if doacao.doador == request.user:
        messages.error(request, 'Você não pode reservar sua própria doação.')
        return redirect('doacao_detalhe', pk=pk)
    
    doacao.receptor = request.user
    doacao.status = 'reservado'
    doacao.save()
    
    messages.success(request, 'Doação reservada com sucesso! Entre em contato com o doador.')
    return redirect('doacao_detalhe', pk=pk)


@login_required
def minhas_doacoes(request):
    """Listar doações do usuário"""
    doacoes_feitas = Doacao.objects.filter(doador=request.user)
    doacoes_recebidas = Doacao.objects.filter(receptor=request.user)
    
    context = {
        'doacoes_feitas': doacoes_feitas,
        'doacoes_recebidas': doacoes_recebidas,
    }
    return render(request, 'doacoes/minhas_doacoes.html', context)


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
    
    return render(request, 'doacoes/perfil.html', {'form': form, 'perfil': perfil})


def registro(request):
    """Registro de novo usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criar perfil automaticamente
            Perfil.objects.create(usuario=user)
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('perfil')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})


def buscar(request):
    """Busca de doações"""
    query = request.GET.get('q', '')
    doacoes = Doacao.objects.filter(status='disponivel')
    
    if query:
        doacoes = doacoes.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(categoria__nome__icontains=query) |
            Q(cidade__icontains=query)
        )
    
    context = {
        'doacoes': doacoes,
        'query': query,
    }
    return render(request, 'doacoes/buscar.html', context)
