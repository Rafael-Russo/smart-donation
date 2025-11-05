from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    """Categorias de itens para doação"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Nome do ícone Bootstrap")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Perfil(models.Model):
    """Perfil estendido do usuário"""
    TIPO_CHOICES = [
        ('doador', 'Doador'),
        ('receptor', 'Receptor'),
        ('ambos', 'Doador e Receptor'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='doador')
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    avaliacao_media = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_doacoes = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"


class Doacao(models.Model):
    """Doação de itens"""
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    doador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doacoes_feitas')
    receptor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doacoes_recebidas')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='doacoes')
    
    quantidade = models.IntegerField(default=1)
    condicao = models.CharField(max_length=100, help_text="Ex: Novo, Usado em bom estado, etc.")
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='disponivel')
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES, default='media')
    
    foto = models.ImageField(upload_to='doacoes/', blank=True, null=True)
    
    # Localização
    endereco_retirada = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_entrega = models.DateTimeField(null=True, blank=True)
    
    # Controle
    visualizacoes = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.doador.username}"
    
    def marcar_como_entregue(self):
        self.status = 'entregue'
        self.data_entrega = timezone.now()
        self.save()


class Mensagem(models.Model):
    """Mensagens entre doadores e receptores"""
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE, related_name='mensagens')
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['data_envio']
    
    def __str__(self):
        return f"De {self.remetente.username} para {self.destinatario.username}"


class Avaliacao(models.Model):
    """Avaliações entre usuários"""
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE, related_name='avaliacoes')
    
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 a 5 estrelas
    comentario = models.TextField(blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ['avaliador', 'doacao']
    
    def __str__(self):
        return f"{self.avaliador.username} avaliou {self.avaliado.username} - {self.nota} estrelas"
