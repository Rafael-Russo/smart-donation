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


class PontoColeta(models.Model):
    """Ponto de coleta gerenciado por doadores"""
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pontos_coleta')
    
    nome = models.CharField(max_length=200, help_text="Nome do ponto de coleta")
    descricao = models.TextField(help_text="Descrição do local e como funciona")
    
    # Endereço completo
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    
    # Contato
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Horário de funcionamento
    horario_funcionamento = models.TextField(help_text="Ex: Segunda a Sexta, 9h às 17h")
    
    # Foto do local
    foto = models.ImageField(upload_to='pontos_coleta/', blank=True, null=True)
    
    # Status
    ativo = models.BooleanField(default=True)
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ponto de Coleta"
        verbose_name_plural = "Pontos de Coleta"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"
    
    def endereco_completo(self):
        """Retorna endereço formatado"""
        parts = [self.endereco]
        if self.numero:
            parts.append(f"nº {self.numero}")
        if self.complemento:
            parts.append(self.complemento)
        parts.append(f"{self.bairro}, {self.cidade}/{self.estado}")
        parts.append(f"CEP: {self.cep}")
        return " - ".join(parts)


class ItemEstoque(models.Model):
    """Item no estoque de um ponto de coleta"""
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('retirado', 'Retirado'),
        ('cancelado', 'Cancelado'),
    ]
    
    ponto_coleta = models.ForeignKey(PontoColeta, on_delete=models.CASCADE, related_name='itens')
    doador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itens_doados')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='itens_estoque')
    
    quantidade = models.IntegerField(default=1)
    quantidade_disponivel = models.IntegerField(default=1, help_text="Quantidade ainda disponível")
    condicao = models.CharField(max_length=100, help_text="Ex: Novo, Usado em bom estado, etc.")
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='disponivel')
    urgencia = models.CharField(max_length=10, choices=Doacao.URGENCIA_CHOICES, default='media')
    
    foto = models.ImageField(upload_to='itens_estoque/', blank=True, null=True)
    
    # Controle
    visualizacoes = models.IntegerField(default=0)
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item do Estoque"
        verbose_name_plural = "Itens do Estoque"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.ponto_coleta.nome}"
    
    def atualizar_disponibilidade(self):
        """Atualiza status baseado na quantidade disponível"""
        if self.quantidade_disponivel <= 0:
            self.status = 'retirado'
        elif self.status == 'retirado' and self.quantidade_disponivel > 0:
            self.status = 'disponivel'
        self.save()


class SolicitacaoRetirada(models.Model):
    """Solicitação de retirada/entrega de item"""
    TIPO_CHOICES = [
        ('retirada', 'Retirada no Local'),
        ('entrega', 'Entrega'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    item = models.ForeignKey(ItemEstoque, on_delete=models.CASCADE, related_name='solicitacoes')
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes_feitas')
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='retirada')
    quantidade_solicitada = models.IntegerField(default=1)
    
    # Endereço de entrega (se tipo = entrega)
    endereco_entrega = models.CharField(max_length=255, blank=True)
    cidade_entrega = models.CharField(max_length=100, blank=True)
    estado_entrega = models.CharField(max_length=2, blank=True)
    
    # Observações
    observacao_solicitante = models.TextField(blank=True, help_text="Observações do solicitante")
    observacao_responsavel = models.TextField(blank=True, help_text="Resposta/observações do responsável")
    
    # Status e controle
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    
    # Datas
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Solicitação de Retirada"
        verbose_name_plural = "Solicitações de Retirada"
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"{self.solicitante.username} - {self.item.titulo} ({self.get_status_display()})"
    
    def aprovar(self, observacao=''):
        """Aprova a solicitação e atualiza estoque"""
        self.status = 'aprovada'
        self.observacao_responsavel = observacao
        self.data_resposta = timezone.now()
        self.save()
        
        # Reservar quantidade no estoque
        if self.item.quantidade_disponivel >= self.quantidade_solicitada:
            self.item.quantidade_disponivel -= self.quantidade_solicitada
            self.item.status = 'reservado'
            self.item.save()
    
    def recusar(self, motivo=''):
        """Recusa a solicitação"""
        self.status = 'recusada'
        self.observacao_responsavel = motivo
        self.data_resposta = timezone.now()
        self.save()
    
    def concluir(self):
        """Marca como concluída"""
        self.status = 'concluida'
        self.data_conclusao = timezone.now()
        self.save()
        
        # Atualiza status do item
        self.item.atualizar_disponibilidade()


class PostComunidade(models.Model):
    """Post na comunidade"""
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    ponto_coleta = models.ForeignKey(PontoColeta, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='posts/', blank=True, null=True)
    
    # Tags
    tags = models.CharField(max_length=200, blank=True, help_text="Separadas por vírgula")
    
    # Controle
    fixado = models.BooleanField(default=False, help_text="Post fixado no topo")
    visualizacoes = models.IntegerField(default=0)
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Post da Comunidade"
        verbose_name_plural = "Posts da Comunidade"
        ordering = ['-fixado', '-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"
    
    def total_comentarios(self):
        return self.comentarios.count()


class ComentarioPost(models.Model):
    """Comentário em um post da comunidade"""
    post = models.ForeignKey(PostComunidade, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    
    texto = models.TextField()
    
    # Comentário pai (para respostas)
    resposta_a = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['data_criacao']
    
    def __str__(self):
        return f"{self.autor.username} comentou em '{self.post.titulo}'"
    
    def total_respostas(self):
        return self.respostas.count()
