from django import forms
from .models import (
    Doacao, Perfil, Mensagem, PontoColeta, ItemEstoque,
    SolicitacaoRetirada, PostComunidade, ComentarioPost
)


class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = [
            'titulo', 'descricao', 'categoria', 'quantidade', 'condicao',
            'urgencia', 'foto', 'endereco_retirada', 'cidade', 'estado'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'estado': forms.Select(choices=[
                ('', 'Selecione'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
            ]),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'foto']
        widgets = {
            'estado': forms.Select(choices=[
                ('', 'Selecione'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
            ]),
        }


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua mensagem...'}),
        }


# Estados brasileiros para reuso
ESTADOS_CHOICES = [
    ('', 'Selecione'),
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
    ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
    ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
]


class PontoColetaForm(forms.ModelForm):
    class Meta:
        model = PontoColeta
        fields = [
            'nome', 'descricao', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email',
            'horario_funcionamento', 'ativo'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'horario_funcionamento': forms.Textarea(attrs={'rows': 2}),
            'estado': forms.Select(choices=ESTADOS_CHOICES),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ItemEstoqueForm(forms.ModelForm):
    class Meta:
        model = ItemEstoque
        fields = [
            'titulo', 'descricao', 'categoria', 'quantidade',
            'status', 'urgencia', 'condicao', 'foto'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover o campo ponto_coleta do formulário pois será definido na view
        if 'ponto_coleta' in self.fields:
            del self.fields['ponto_coleta']


class SolicitacaoRetiradaForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoRetirada
        fields = [
            'quantidade_solicitada', 'tipo', 'endereco_entrega',
            'cidade_entrega', 'estado_entrega', 'observacao_solicitante'
        ]
        widgets = {
            'observacao_solicitante': forms.Textarea(attrs={'rows': 3}),
            'endereco_entrega': forms.Textarea(attrs={'rows': 2}),
            'estado_entrega': forms.Select(choices=ESTADOS_CHOICES),
        }
    
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)
        
        if self.item:
            # Limitar a quantidade máxima ao disponível
            self.fields['quantidade_solicitada'].widget.attrs['max'] = self.item.quantidade_disponivel
            self.fields['quantidade_solicitada'].help_text = f'Máximo: {self.item.quantidade_disponivel}'


class PostComunidadeForm(forms.ModelForm):
    class Meta:
        model = PostComunidade
        fields = ['titulo', 'conteudo', 'tags', 'ponto_coleta', 'fixado']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 6}),
            'tags': forms.TextInput(attrs={'placeholder': 'Ex: ajuda roupas urgente'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Apenas staff pode fixar posts
        if user and not user.is_staff:
            self.fields['fixado'].widget = forms.HiddenInput()
            self.fields['fixado'].initial = False
        
        # Filtrar pontos de coleta ativos
        if user:
            self.fields['ponto_coleta'].queryset = PontoColeta.objects.filter(ativo=True)
            self.fields['ponto_coleta'].required = False


class ComentarioPostForm(forms.ModelForm):
    class Meta:
        model = ComentarioPost
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário...'}),
        }
