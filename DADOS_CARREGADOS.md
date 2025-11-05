# 🎯 DADOS CARREGADOS NO BANCO

## ✅ Status: Banco Populado com Sucesso!

---

## 📊 Estatísticas

- **Categorias:** 8
- **Usuários:** 6 (2 do sistema + 4 de exemplo)
- **Doações:** 8
- **Perfis:** 4 (completos com telefone e endereço)

---

## 🔑 Credenciais de Acesso

### Usuários de Exemplo (senha: `senha123`)

| Username | Nome | Tipo | Cidade | Doações |
|----------|------|------|--------|---------|
| maria_silva | Maria Silva | Doador | São Paulo - SP | 3 |
| joao_santos | João Santos | Doador e Receptor | Rio de Janeiro - RJ | 3 |
| ana_costa | Ana Costa | Doador | Belo Horizonte - MG | 2 |
| carlos_oliveira | Carlos Oliveira | Receptor | Curitiba - PR | 0 |

---

## 🎁 Doações Disponíveis

### 1. Sofá 3 lugares em bom estado 🛋️
- **Doador:** Maria Silva (São Paulo - SP)
- **Categoria:** Móveis
- **Urgência:** 🟡 Média
- **Condição:** Usado em bom estado

### 2. Roupas infantis (2-4 anos) 👕
- **Doador:** Maria Silva (São Paulo - SP)
- **Categoria:** Roupas
- **Quantidade:** 15 peças
- **Urgência:** 🟢 Baixa
- **Condição:** Usado em ótimo estado

### 3. Notebook Dell - i5, 8GB RAM 💻
- **Doador:** João Santos (Rio de Janeiro - RJ)
- **Categoria:** Eletrônicos
- **Urgência:** 🟠 Alta
- **Condição:** Usado - bateria com defeito
- **Nota:** Funciona apenas na tomada, ideal para estudos

### 4. Cesta básica completa 🍎
- **Doador:** João Santos (Rio de Janeiro - RJ)
- **Categoria:** Alimentos
- **Urgência:** 🔴 **URGENTE**
- **Condição:** Novo - lacrado
- **Conteúdo:** Arroz, feijão, óleo, macarrão, açúcar, café, sal, biscoitos

### 5. Kit livros didáticos ensino médio 📚
- **Doador:** Ana Costa (Belo Horizonte - MG)
- **Categoria:** Livros
- **Quantidade:** 21 livros
- **Urgência:** 🟠 Alta
- **Condição:** Usado em ótimo estado
- **Conteúdo:** Matemática, português, história, geografia, biologia, física, química

### 6. Mesa de jantar 4 lugares 🪑
- **Doador:** Ana Costa (Belo Horizonte - MG)
- **Categoria:** Móveis
- **Urgência:** 🟡 Média
- **Condição:** Usado em excelente estado

### 7. Brinquedos diversos 🧸
- **Doador:** Maria Silva (São Paulo - SP)
- **Categoria:** Brinquedos
- **Quantidade:** 20 itens
- **Urgência:** 🟢 Baixa
- **Condição:** Usado em bom estado
- **Conteúdo:** Carrinhos, bonecas, jogos de tabuleiro, pelúcias, quebra-cabeças

### 8. Jogo de panelas 5 peças 🍳
- **Doador:** João Santos (Rio de Janeiro - RJ)
- **Categoria:** Utensílios
- **Urgência:** 🟡 Média
- **Condição:** Usado em bom estado

---

## 🗂️ Categorias Ativas

1. 👕 **Roupas** - Roupas infantis, femininas e masculinas
2. 🍎 **Alimentos** - Alimentos não perecíveis e cestas básicas
3. 🛋️ **Móveis** - Móveis para casa e escritório
4. 💻 **Eletrônicos** - Computadores, celulares e eletrônicos
5. 🧸 **Brinquedos** - Brinquedos infantis e jogos
6. 📚 **Livros** - Livros, revistas e material educativo
7. 🍽️ **Utensílios** - Utensílios domésticos e cozinha
8. ➕ **Outros** - Outros itens diversos

---

## 🎭 Cenários de Teste Disponíveis

### Cenário 1: Buscar Doação Urgente
1. Login como: `carlos_oliveira` / `senha123`
2. Veja a **Cesta básica** com badge vermelho URGENTE
3. Reserve o item
4. Veja os dados do doador para contato

### Cenário 2: Gerenciar Suas Doações
1. Login como: `maria_silva` / `senha123`
2. Acesse "Minhas Doações"
3. Veja suas 3 doações ativas
4. Edite uma delas
5. Verifique se alguém reservou

### Cenário 3: Buscar por Categoria
1. Página inicial
2. Filtre por categoria "Eletrônicos"
3. Encontre o Notebook Dell
4. Veja detalhes completos

### Cenário 4: Criar Nova Doação
1. Login como: `joao_santos` / `senha123`
2. Clique em "+ Nova Doação"
3. Preencha todos os campos
4. Adicione foto (opcional)
5. Salve e veja na listagem

### Cenário 5: Perfil Completo
1. Login com qualquer usuário de exemplo
2. Acesse "Meu Perfil"
3. Veja estatísticas (total de doações, avaliação)
4. Edite informações de contato
5. Adicione foto de perfil

---

## 📱 Testando no Navegador

### Página Inicial
**URL:** http://127.0.0.1:8000/

✅ Deve mostrar:
- Hero section com call-to-action
- Filtros (categoria, cidade, urgência)
- Grid com as 8 doações
- Cards com fotos, título, localização
- Badge de urgência nos itens urgentes/alta prioridade

### Admin
**URL:** http://127.0.0.1:8000/admin/

✅ Login com superusuário
✅ Veja todos os dados organizados
✅ Edite/adicione/remova dados

### Detalhes de uma Doação
**Exemplo:** http://127.0.0.1:8000/doacao/1/

✅ Deve mostrar:
- Foto ou placeholder
- Informações completas do item
- Dados do doador (nome, avaliação, total de doações)
- Botão de reserva (se logado)
- Localização completa

---

## 🔍 Verificar Dados via Shell

```powershell
python manage.py shell
```

```python
# Importar models
from doacoes.models import Categoria, Perfil, Doacao
from django.contrib.auth.models import User

# Ver todas as categorias
for cat in Categoria.objects.all():
    print(f"📂 {cat.nome} - {cat.doacoes.count()} doações")

# Ver todos os usuários com perfil
for user in User.objects.all():
    if hasattr(user, 'perfil'):
        print(f"👤 {user.username} - {user.perfil.cidade}/{user.perfil.estado}")

# Ver doações por urgência
urgentes = Doacao.objects.filter(urgencia='urgente')
print(f"🔴 {urgentes.count()} doações urgentes")

# Ver doações disponíveis
disponiveis = Doacao.objects.filter(status='disponivel')
print(f"✅ {disponiveis.count()} doações disponíveis")

# Doação mais visualizada
mais_vista = Doacao.objects.order_by('-visualizacoes').first()
if mais_vista:
    print(f"👀 Mais vista: {mais_vista.titulo} ({mais_vista.visualizacoes} views)")
```

---

## 🎨 Interface Visual

### Home Page
- ✅ Design responsivo (mobile-friendly)
- ✅ Cores verde (tema solidariedade)
- ✅ Cards com efeito hover
- ✅ Badges coloridos por urgência
- ✅ Ícones Bootstrap Icons
- ✅ Filtros funcionais

### Detalhes da Doação
- ✅ Layout em 2 colunas
- ✅ Imagem grande do item
- ✅ Sidebar com info do doador
- ✅ Badges de status e urgência
- ✅ Botões de ação contextuais

### Minhas Doações
- ✅ Tabs separando "Feitas" e "Recebidas"
- ✅ Grid responsivo
- ✅ Status visual claro
- ✅ Ações rápidas (Ver, Editar)

---

## 📈 Próximos Passos Sugeridos

1. ✅ **Testar todos os cenários** acima
2. ✅ **Adicionar mais doações** via interface ou admin
3. ✅ **Testar reservas** e comunicação entre usuários
4. ✅ **Criar seu próprio superusuário** para gerenciar
5. ✅ **Personalizar dados** editando o script `popular_db.py`
6. ✅ **Fazer deploy** no PythonAnywhere quando estiver satisfeito

---

## 🎯 Funcionalidades Testáveis

### Como Visitante (não logado)
- ✅ Ver todas as doações
- ✅ Buscar e filtrar
- ✅ Ver detalhes dos itens
- ❌ Não pode reservar (pede login)

### Como Doador
- ✅ Criar doações
- ✅ Editar suas doações
- ✅ Ver quem reservou
- ✅ Gerenciar status
- ✅ Ver estatísticas do perfil

### Como Receptor
- ✅ Buscar doações
- ✅ Reservar itens
- ✅ Ver contato do doador (após reserva)
- ✅ Acompanhar itens reservados

### Como Admin
- ✅ Acesso total ao Django Admin
- ✅ Moderar conteúdo
- ✅ Gerenciar usuários
- ✅ Ver todas as transações

---

## 💡 Dicas de Teste

1. **Abra múltiplas janelas anônimas** para testar com diferentes usuários simultaneamente

2. **Use o filtro de urgência** para ver como os badges se comportam

3. **Teste a busca** com termos como: "notebook", "brinquedo", "são paulo"

4. **Reserve um item** e veja como aparece em "Minhas Doações" para ambos os usuários

5. **Edite uma doação** e mude o status para ver as mudanças refletidas

---

**Banco de dados populado e pronto para testes completos! 🚀**
