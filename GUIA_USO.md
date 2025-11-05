# 📖 Guia Rápido de Uso - Doação Inteligente

## 🚀 Como Começar

### 1. Executar o Projeto Localmente

```bash
# Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Executar servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

### 2. Acessar o Painel Administrativo

URL: http://127.0.0.1:8000/admin/

Criar superusuário (se ainda não criou):
```bash
python manage.py createsuperuser
```

## 👥 Para Usuários

### Cadastro e Login
1. Acesse a página inicial
2. Clique em "Cadastrar" no menu superior
3. Preencha o formulário de registro
4. Faça login com suas credenciais

### Completar Perfil
1. Após login, clique em seu nome no menu
2. Selecione "Meu Perfil"
3. Preencha informações como:
   - Tipo (Doador, Receptor ou Ambos)
   - Telefone
   - Endereço completo
   - Foto (opcional)

## 🎁 Para Doadores

### Cadastrar Nova Doação
1. Clique em "+ Nova Doação" no menu
2. Preencha os dados:
   - **Título:** Nome do item (ex: "Sofá 3 lugares usado")
   - **Descrição:** Detalhes do item
   - **Categoria:** Selecione a categoria apropriada
   - **Quantidade:** Número de itens
   - **Condição:** Estado do item (Novo, Usado em bom estado, etc.)
   - **Urgência:** Baixa, Média, Alta ou Urgente
   - **Foto:** Adicione uma imagem do item
   - **Localização:** Endereço, cidade e estado
3. Clique em "Salvar"

### Gerenciar Doações
1. Acesse "Minhas Doações" no menu
2. Visualize doações feitas e recebidas
3. Edite doações disponíveis
4. Veja quem reservou suas doações

### Status das Doações
- 🟢 **Disponível:** Item está disponível para reserva
- 🟡 **Reservado:** Alguém demonstrou interesse
- 🔵 **Entregue:** Item foi entregue
- ⚫ **Cancelado:** Doação foi cancelada

## 🎯 Para Receptores

### Buscar Doações
1. Use a barra de busca na página inicial
2. Ou acesse "Buscar" no menu
3. Filtre por:
   - Categoria
   - Cidade
   - Urgência

### Reservar Item
1. Clique em "Ver Detalhes" na doação desejada
2. Leia todas as informações
3. Clique em "Tenho Interesse"
4. Entre em contato com o doador pelos dados disponíveis

### Acompanhar Doações Recebidas
1. Acesse "Minhas Doações"
2. Veja aba "Doações Recebidas"
3. Acompanhe status das suas reservas

## 🏷️ Categorias Disponíveis

- 👕 **Roupas:** Roupas infantis, femininas e masculinas
- 🍎 **Alimentos:** Alimentos não perecíveis e cestas básicas
- 🛋️ **Móveis:** Móveis para casa e escritório
- 💻 **Eletrônicos:** Computadores, celulares e eletrônicos
- 🧸 **Brinquedos:** Brinquedos infantis e jogos
- 📚 **Livros:** Livros, revistas e material educativo
- 🍽️ **Utensílios:** Utensílios domésticos e cozinha
- ➕ **Outros:** Outros itens diversos

## 🔍 Dicas de Uso

### Para Doadores
✅ Tire fotos claras e bem iluminadas dos itens
✅ Seja detalhado na descrição
✅ Indique claramente a condição do item
✅ Marque como "Urgente" apenas se realmente for
✅ Responda rapidamente aos interessados
✅ Mantenha o status da doação atualizado

### Para Receptores
✅ Leia toda a descrição antes de reservar
✅ Verifique a localização do item
✅ Entre em contato rapidamente com o doador
✅ Seja pontual e respeitoso no contato
✅ Confirme o recebimento após retirar o item

## 🔐 Segurança

- ✅ Nunca compartilhe sua senha
- ✅ Use senhas fortes
- ✅ Verifique a reputação do usuário
- ✅ Prefira encontros em locais públicos
- ✅ Leve alguém junto na retirada
- ✅ Reporte comportamentos suspeitos ao admin

## 📱 Funcionalidades do Sistema

### Filtros Inteligentes
- Filtre por categoria, cidade e urgência
- Busca por texto em título e descrição
- Ordenação por data de publicação

### Sistema de Urgência
- 🔴 **Urgente:** Necessidade imediata (ex: alimentos perecíveis)
- 🟠 **Alta:** Importante, mas não urgente
- 🟡 **Média:** Prioridade normal
- 🟢 **Baixa:** Sem pressa

### Estatísticas do Perfil
- Total de doações realizadas
- Avaliação média recebida
- Tempo como membro

## 🛠️ Resolução de Problemas

### Não consigo fazer login
1. Verifique usuário e senha
2. Use "Esqueceu sua senha?" se necessário
3. Certifique-se de ter confirmado o email (se ativado)

### Não consigo adicionar foto
1. Verifique o tamanho (máximo recomendado: 5MB)
2. Use formatos: JPG, PNG, GIF
3. Tente redimensionar a imagem

### Não vejo minhas doações
1. Verifique se está logado
2. Clique em "Minhas Doações" no menu
3. Confira se a doação foi salva corretamente

### Erro ao reservar item
1. Certifique-se de estar logado
2. Verifique se o item ainda está disponível
3. Atualize a página

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este guia primeiro
2. Consulte o FAQ (em breve)
3. Entre em contato com o administrador

## 🎯 Melhores Práticas

### Descrição de Itens
```
✅ BOM:
"Sofá 3 lugares em tecido azul marinho, usado por 2 anos,
em bom estado de conservação. Medidas: 2m x 0,9m x 0,8m.
Retirada no Centro."

❌ RUIM:
"Sofá velho"
```

### Fotos
- ✅ Tire várias fotos de ângulos diferentes
- ✅ Mostre detalhes e defeitos (se houver)
- ✅ Use boa iluminação
- ❌ Evite fotos muito escuras ou desfocadas

### Comunicação
- ✅ Seja educado e respeitoso
- ✅ Responda prontamente
- ✅ Seja claro sobre disponibilidade
- ✅ Confirme horários e locais

## 📊 Dashboard (Admin)

O administrador pode:
- Ver todas as doações
- Gerenciar usuários
- Moderar conteúdo
- Visualizar estatísticas
- Adicionar categorias
- Enviar mensagens em massa (futuro)

---

**Aproveite o sistema e ajude a fazer a diferença na comunidade! ❤️**
