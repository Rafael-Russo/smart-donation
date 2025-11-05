# 📖 Guia Completo de Uso - Smart Donation

## 🎯 Visão Geral

O Smart Donation funciona através de **Pontos de Coleta** gerenciados por usuários. O fluxo básico é:

1. **Doadores** criam pontos de coleta e adicionam itens ao estoque
2. **Receptores** navegam pelos itens disponíveis e fazem solicitações
3. **Gestores** dos pontos aprovam ou recusam solicitações
4. **Comunidade** interage através de posts e comentários

## 🚀 Começando

### Instalação e Primeiro Acesso

```bash
# 1. Ative o ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Execute o servidor
python manage.py runserver

# 3. Acesse no navegador
http://127.0.0.1:8000/
```

### Criar Conta

1. Clique em **"Cadastrar"** no menu superior
2. Preencha:
   - Nome de usuário
   - Email
   - Senha (2x para confirmar)
   - Nome e sobrenome
3. Clique em **"Cadastrar"**
4. Você será automaticamente logado

### Completar Perfil

1. Clique no seu nome no menu → **"Meu Perfil"**
2. Preencha as informações:
   - **Tipo de usuário:**
     - `Doador`: Cria pontos e doa itens
     - `Receptor`: Solicita itens
     - `Ambos`: Pode fazer as duas coisas
   - **Telefone** para contato
   - **Endereço completo**
   - **Foto de perfil** (opcional)
3. Clique em **"Salvar Alterações"**

---

## 🏢 Guia para Gestores de Pontos de Coleta

### 1. Criar um Ponto de Coleta

1. Menu: **"Pontos de Coleta"** → **"Criar Ponto"**
2. Preencha os dados:
   - **Nome:** Nome do seu ponto (ex: "Centro de Doações Zona Norte")
   - **Descrição:** O que o ponto faz, quem atende, etc.
   - **Endereço completo:**
     - Endereço, Bairro, Cidade, Estado, CEP
   - **Contatos:**
     - Telefone
     - Email
   - **Horário de funcionamento:** Quando está aberto para doações/retiradas
3. Clique em **"Criar Ponto de Coleta"**

### 2. Adicionar Itens ao Estoque

#### Opção A: Pelo Menu Principal
1. Menu: **"Estoque"** → **"Adicionar Item"**

#### Opção B: Pelo Seu Estoque
1. Menu: **"Estoque"** → **"Meu Estoque"**
2. Clique em **"+ Adicionar Novo Item"**

#### Preenchendo o Formulário:
- **Título:** Nome do item (ex: "Roupas Infantis 2-6 anos")
- **Descrição:** Detalhes completos
- **Categoria:** Escolha de 8 opções (Roupas, Alimentos, Móveis, etc.)
- **Quantidade:** Quantidade total disponível
- **Condição:** 
  - Novo
  - Usado em ótimo estado
  - Usado em bom estado  
  - Usado - precisa reparos
- **Urgência:**
  - Baixa
  - Média
  - Alta
  - Urgente
- **Foto:** Imagem do item (opcional mas recomendado)

3. Clique em **"Adicionar ao Estoque"**

### 3. Gerenciar Solicitações de Retirada

#### Ver Solicitações Recebidas
1. Menu: **"Solicitações"** → **"Gerenciar Solicitações"**
2. Você verá todas as solicitações para itens do seu ponto
3. Filtros disponíveis:
   - Por status (Pendente, Aprovada, Recusada, etc.)
   - Por item específico

#### Aprovar uma Solicitação
1. Na lista, clique em **"Ver Detalhes"**
2. Analise:
   - Quem está solicitando
   - Quantidade pedida
   - Justificativa do solicitante
3. Clique em **"Aprovar"**
4. Digite observações (opcional) sobre como/quando retirar
5. Confirme

**O que acontece:**
- Quantidade é reservada automaticamente no estoque
- Status muda para "Aprovada"
- Solicitante recebe notificação visual

#### Recusar uma Solicitação
1. Clique em **"Recusar"**
2. Digite o **motivo da recusa** (obrigatório)
3. Confirme

#### Marcar como Concluída
1. Após a pessoa retirar os itens, clique em **"Concluir"**
2. O estoque é atualizado definitivamente

### 4. Dashboard de Estoque

Acesse: Menu → **"Estoque"** → **"Meu Estoque"**

**Você verá:**
- **Estatísticas:**
  - Total de itens cadastrados
  - Quantidade total disponível
  - Itens urgentes
  - Solicitações pendentes
  
- **Lista de itens** com:
  - Visualizações
  - Quantidade disponível
  - Status
  - Ações rápidas (Editar/Excluir)

- **Filtros:**
  - Por categoria
  - Por urgência
  - Por status

---

## 🤲 Guia para Receptores

### 1. Encontrar Itens Disponíveis

#### Opção A: Página Inicial
- A home mostra **itens urgentes** em destaque
- Clique em qualquer item para ver detalhes

#### Opção B: Navegar por Pontos de Coleta
1. Menu: **"Pontos de Coleta"** → **"Ver Todos"**
2. Use filtros:
   - Por cidade
   - Por estado
   - Pontos ativos
3. Clique em um ponto para ver todos os itens disponíveis

### 2. Solicitar Retirada de Item

1. Entre na página de detalhes do item
2. Verifique:
   - Quantidade disponível
   - Condição
   - Descrição completa
   - Localização do ponto
3. Clique em **"Solicitar Retirada"**
4. Preencha:
   - **Quantidade solicitada:** Máximo = quantidade disponível
   - **Tipo de recebimento:**
     - Retirada no local (você busca)
     - Entrega (se disponível, forneça endereço)
   - **Justificativa:** Por que precisa desse item
5. Clique em **"Enviar Solicitação"**

### 3. Acompanhar Suas Solicitações

Menu: **"Solicitações"** → **"Minhas Solicitações"**

**Status possíveis:**
- 🟡 **Pendente:** Aguardando análise do gestor
- 🟢 **Aprovada:** Aprovada! Veja observações sobre retirada
- 🔴 **Recusada:** Leia o motivo da recusa
- ✅ **Concluída:** Item já foi retirado
- ⚫ **Cancelada:** Você cancelou

**Ações disponíveis:**
- **Ver detalhes** de qualquer solicitação
- **Cancelar** solicitações pendentes

**Filtros:**
- Por status
- Por ponto de coleta
- Por datas

### 4. Cancelar uma Solicitação

1. Em **"Minhas Solicitações"**
2. Localize a solicitação **pendente**
3. Clique em **"Cancelar"**
4. Confirme o cancelamento

---

## 💬 Guia da Comunidade

### 1. Navegar nos Posts

Menu: **"Comunidade"**

**O que você verá:**
- Posts **fixados** no topo (campanhas importantes)
- Posts recentes de todos os pontos
- Filtros por ponto de coleta

### 2. Criar um Post

**Quem pode:** Usuários com ponto de coleta

1. Na página da Comunidade, clique em **"Criar Post"**
2. Preencha:
   - **Ponto de coleta:** Selecione seu ponto
   - **Título:** Título chamativo
   - **Conteúdo:** Texto formatado (suporte a Markdown)
   - **Imagem:** Foto ilustrativa (opcional)
   - **Fixar post:** ☑️ (apenas staff) para manter no topo
3. Clique em **"Publicar"**

**Dicas de conteúdo:**
- Campanhas especiais (Ex: "Campanha de Inverno")
- Agradecimentos
- Novos projetos
- Dicas para doadores
- Histórias de impacto

### 3. Comentar em Posts

1. Entre na página de detalhes do post
2. Role até a seção de comentários
3. Digite seu comentário na caixa de texto
4. Clique em **"Comentar"**

### 4. Responder Comentários

1. Em qualquer comentário, clique em **"Responder"**
2. Digite sua resposta
3. Clique em **"Responder"**
4. A resposta aparecerá aninhada abaixo do comentário original

### 5. Gerenciar Seus Posts

**Ver seus posts:**
- Vá até o post que criou
- Clique em **"Editar"** ou **"Excluir"**

**Editar:**
- Modifique título/conteúdo/imagem
- Salve alterações

**Excluir:**
- Confirme a exclusão
- ⚠️ Todos os comentários serão perdidos

---

## ⚙️ Recursos Avançados

### Sistema de Busca e Filtros

#### Na Lista de Pontos:
- Filtre por cidade/estado
- Veja apenas pontos ativos
- Ordenação por relevância

#### No Estoque:
- Filtre por categoria
- Filtre por urgência
- Filtre por status (disponível/reservado/retirado)

#### Em Solicitações:
- Filtre por status
- Filtre por ponto de coleta
- Filtre por período (últimos 7/30 dias)

### Estatísticas na Home

A página inicial mostra:
- **Total de pontos ativos**
- **Total de itens disponíveis**
- **Total de solicitações** em andamento
- **Total de usuários** cadastrados
- **Pontos recentes** (últimos 3)
- **Itens urgentes** (últimos 4)
- **Posts recentes** (últimos 4)

### Painel Administrativo

**Acesso:** http://127.0.0.1:8000/admin/

**Recursos extras:**
- Edição em massa de registros
- Filtros avançados
- Histórico de mudanças
- Ações personalizadas

---

## 🔐 Credenciais de Teste

Após executar `python manage.py popular_db --completo`:

### Gestores de Pontos:
- **maria_silva** (Centro de Doações Zona Sul - SP)
- **joao_santos** (Ponto Solidário Copacabana - RJ)
- **ana_costa** (Espaço Doar - BH)

### Receptores:
- **carlos_oliveira** (fez várias solicitações)
- **pedro_receptor** (comentou em posts)

**Senha para todos:** `senha123`

---

## ❓ Perguntas Frequentes

### Como faço para criar um ponto de coleta?
Você precisa estar logado e ir em: Pontos de Coleta → Criar Ponto

### Posso ter mais de um ponto de coleta?
Sim! Cada usuário pode criar e gerenciar múltiplos pontos.

### Como sei se minha solicitação foi aprovada?
Acesse "Minhas Solicitações" e veja o status. Quando aprovada, haverá observações do gestor.

### Posso editar um item depois de adicionado?
Sim! Vá em "Meu Estoque", encontre o item e clique em "Editar".

### O que acontece quando aprovo uma solicitação?
A quantidade solicitada é automaticamente reduzida do estoque disponível.

### Posso cancelar uma solicitação aprovada?
Não. Apenas solicitações pendentes podem ser canceladas. Entre em contato com o gestor do ponto.

### Como excluir meu ponto de coleta?
Vá em "Meus Pontos", selecione o ponto e clique em "Excluir". ⚠️ Todos os itens serão perdidos.

### Os uploads de imagem têm limite de tamanho?
Sim, recomendamos imagens de até 5MB para melhor performance.

---

## 📞 Suporte

Para dúvidas técnicas ou problemas:
- Abra uma issue no GitHub
- Envie email para: suporte@smartdonation.com
- Consulte a documentação técnica em `PROJETO_COMPLETO.md`

---

**Última atualização:** Novembro 2025  
**Versão do Sistema:** 2.0 (Arquitetura de Pontos de Coleta)
