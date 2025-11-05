# 📊 Script de População do Banco de Dados

## 🎯 Visão Geral

O comando `popular_db` foi criado para facilitar o setup inicial do banco de dados, populando com dados de exemplo para teste e demonstração.

## 🚀 Como Usar

### Opção 1: Apenas Categorias (Básico)

```powershell
python manage.py popular_db
```

**O que cria:**
- ✅ 8 categorias padrão (Roupas, Alimentos, Móveis, etc.)

**Quando usar:**
- Setup inicial do projeto
- Ambiente de produção
- Quando você quer adicionar seus próprios dados

---

### Opção 2: Dados Completos (Recomendado para Testes)

```powershell
python manage.py popular_db --completo
```

**O que cria:**
- ✅ 8 categorias padrão
- ✅ 4 usuários de exemplo com perfis completos
- ✅ 8 doações variadas de exemplo
- ✅ Estatísticas atualizadas nos perfis

**Quando usar:**
- Desenvolvimento e testes
- Demonstração do sistema
- Aprender a usar o sistema

---

## 👥 Usuários Criados

### 1. Maria Silva (`maria_silva`)
- **Tipo:** Doador
- **Localização:** São Paulo - SP
- **Senha:** `senha123`
- **Doações:** 3 itens (Sofá, Roupas infantis, Brinquedos)

### 2. João Santos (`joao_santos`)
- **Tipo:** Doador e Receptor
- **Localização:** Rio de Janeiro - RJ
- **Senha:** `senha123`
- **Doações:** 3 itens (Notebook, Cesta básica, Panelas)

### 3. Ana Costa (`ana_costa`)
- **Tipo:** Doador
- **Localização:** Belo Horizonte - MG
- **Senha:** `senha123`
- **Doações:** 2 itens (Livros, Mesa de jantar)

### 4. Carlos Oliveira (`carlos_oliveira`)
- **Tipo:** Receptor
- **Localização:** Curitiba - PR
- **Senha:** `senha123`
- **Doações:** 0 (apenas busca doações)

---

## 🎁 Doações Criadas

### Categoria: Móveis
1. **Sofá 3 lugares em bom estado**
   - Doador: Maria Silva
   - Urgência: Média
   - Status: Disponível

2. **Mesa de jantar 4 lugares**
   - Doador: Ana Costa
   - Urgência: Média
   - Status: Disponível

### Categoria: Roupas
3. **Roupas infantis (2-4 anos)**
   - Doador: Maria Silva
   - Quantidade: 15 peças
   - Urgência: Baixa
   - Status: Disponível

### Categoria: Eletrônicos
4. **Notebook Dell - i5, 8GB RAM**
   - Doador: João Santos
   - Urgência: Alta
   - Status: Disponível

### Categoria: Alimentos
5. **Cesta básica completa**
   - Doador: João Santos
   - Urgência: **URGENTE**
   - Status: Disponível

### Categoria: Livros
6. **Kit livros didáticos ensino médio**
   - Doador: Ana Costa
   - Quantidade: 21 livros
   - Urgência: Alta
   - Status: Disponível

### Categoria: Brinquedos
7. **Brinquedos diversos**
   - Doador: Maria Silva
   - Quantidade: 20 itens
   - Urgência: Baixa
   - Status: Disponível

### Categoria: Utensílios
8. **Jogo de panelas 5 peças**
   - Doador: João Santos
   - Urgência: Média
   - Status: Disponível

---

## 🔄 Executar Novamente

O script é **inteligente** e **seguro**:
- ✅ Não duplica dados existentes
- ✅ Pode ser executado múltiplas vezes
- ✅ Apenas cria o que ainda não existe

```powershell
# Se executar novamente, verá mensagens como:
# "Categoria 'Roupas' já existe"
# "Usuário 'maria_silva' já existe"
```

---

## 🧪 Cenários de Teste

### Testar como Doador
1. Login com: `maria_silva` / `senha123`
2. Veja suas doações em "Minhas Doações"
3. Crie uma nova doação
4. Edite uma doação existente

### Testar como Receptor
1. Login com: `carlos_oliveira` / `senha123`
2. Navegue pela página inicial
3. Busque doações por categoria
4. Reserve um item de interesse
5. Veja em "Minhas Doações" > "Doações Recebidas"

### Testar como Ambos
1. Login com: `joao_santos` / `senha123`
2. Veja que ele tem doações feitas E pode buscar outras

---

## 🗑️ Limpar Dados de Teste

Se quiser recomeçar do zero:

```powershell
# CUIDADO: Isso apaga TUDO!
# 1. Parar o servidor (Ctrl+C)

# 2. Apagar banco de dados
Remove-Item db.sqlite3

# 3. Aplicar migrações novamente
python manage.py migrate

# 4. Popular novamente
python manage.py popular_db --completo

# 5. Criar superusuário (se necessário)
python manage.py createsuperuser
```

---

## 📝 Personalizar Dados

Para adicionar seus próprios dados de exemplo, edite o arquivo:
```
doacoes/management/commands/popular_db.py
```

### Adicionar Nova Categoria

```python
categorias = [
    # ... categorias existentes ...
    {'nome': 'Eletrônicos', 'descricao': 'Sua descrição', 'icone': 'bi-laptop'},
]
```

### Adicionar Novo Usuário

```python
usuarios_data = [
    # ... usuários existentes ...
    {
        'username': 'novo_usuario',
        'email': 'novo@example.com',
        'first_name': 'Nome',
        'last_name': 'Sobrenome',
        'perfil': {
            'tipo': 'doador',  # ou 'receptor' ou 'ambos'
            'telefone': '(11) 99999-9999',
            'cidade': 'Sua Cidade',
            'estado': 'SP',
            'endereco': 'Seu endereço',
            'cep': '00000-000'
        }
    },
]
```

### Adicionar Nova Doação

```python
doacoes_data = [
    # ... doações existentes ...
    {
        'doador': 'maria_silva',  # username do doador
        'titulo': 'Título da doação',
        'descricao': 'Descrição detalhada...',
        'categoria': 'Móveis',  # Nome da categoria
        'quantidade': 1,
        'condicao': 'Usado em bom estado',
        'status': 'disponivel',
        'urgencia': 'media',  # baixa, media, alta, urgente
        'endereco_retirada': 'Endereço completo',
        'cidade': 'Cidade',
        'estado': 'UF',
    },
]
```

---

## 🎯 Uso em Produção

⚠️ **ATENÇÃO:** Não use o comando `--completo` em produção!

### Produção (PythonAnywhere)
```bash
# Apenas categorias
python manage.py popular_db
```

### Desenvolvimento/Demonstração
```bash
# Com dados de exemplo
python manage.py popular_db --completo
```

---

## 💡 Dicas

1. **Sempre execute o comando básico primeiro** em um novo ambiente:
   ```powershell
   python manage.py popular_db
   ```

2. **Use `--completo` para ver o sistema funcionando** antes de adicionar dados reais

3. **Os usuários de exemplo são ótimos para demonstrações**, mas lembre de removê-los em produção

4. **Após popular, faça login no admin** para explorar os dados:
   - URL: http://127.0.0.1:8000/admin/
   - Explore cada model criado

5. **Teste o fluxo completo:**
   - Login como doador → Criar doação
   - Logout → Login como receptor → Buscar e reservar
   - Login como doador → Ver quem reservou

---

## 🐛 Troubleshooting

### Erro: "already exists"
**Solução:** Normal! O script não duplica dados. Ignore ou limpe o banco.

### Erro: "No such table"
**Solução:** Execute as migrações primeiro:
```powershell
python manage.py migrate
```

### Erro: "User matching query does not exist"
**Solução:** Execute o comando `--completo` para criar os usuários.

### Quero resetar tudo
**Solução:** Siga os passos em "Limpar Dados de Teste"

---

## 📊 Verificar Dados Criados

### Via Shell Django
```powershell
python manage.py shell
```

```python
from doacoes.models import Categoria, Perfil, Doacao
from django.contrib.auth.models import User

# Ver categorias
print(f"Categorias: {Categoria.objects.count()}")

# Ver usuários
print(f"Usuários: {User.objects.count()}")

# Ver doações
print(f"Doações: {Doacao.objects.count()}")

# Listar todas as doações
for doacao in Doacao.objects.all():
    print(f"- {doacao.titulo} ({doacao.doador.username})")
```

### Via Admin Django
1. Acesse: http://127.0.0.1:8000/admin/
2. Navegue por cada model
3. Veja todos os dados criados

---

## 🎉 Resultado Final

Após executar `python manage.py popular_db --completo`, você terá:

✅ Sistema completamente funcional  
✅ Dados reais para demonstração  
✅ Múltiplos cenários de teste  
✅ Diferentes tipos de usuários  
✅ Variedade de categorias e itens  
✅ Diferentes níveis de urgência  

**Pronto para demonstrar e testar todas as funcionalidades!** 🚀
