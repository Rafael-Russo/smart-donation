# 🎯 Smart Donation - Sistema de Gestão de Doações

> **Progressive Web App (PWA) inteligente que conecta doadores e receptores através de pontos de coleta organizados, facilitando a distribuição solidária de recursos para comunidades em situação de vulnerabilidade.**

[![PWA Ready](https://img.shields.io/badge/PWA-Ready-success?style=flat-square&logo=pwa)](https://web.dev/progressive-web-apps/)
[![Django 4.2](https://img.shields.io/badge/Django-4.2.7-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3.2-purple?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

## 📋 Sobre o Projeto

O Smart Donation é uma **Progressive Web App (PWA)** desenvolvida em Django que revoluciona a forma como doações são realizadas. Ao invés de doações diretas pessoa-a-pessoa, o sistema utiliza **pontos de coleta** como centros de distribuição, permitindo:

- ✅ **Gestão centralizada** de doações por responsáveis de pontos de coleta
- ✅ **Controle de estoque** em tempo real com rastreabilidade completa
- ✅ **Sistema de aprovação** para solicitações de retirada
- ✅ **Comunidade ativa** com posts, comentários e engajamento
- ✅ **Transparência total** no fluxo de doações
- ✨ **PWA instalável** - Funciona offline e pode ser instalado como app nativo
- ✨ **Botão flutuante de instalação** - Experiência intuitiva para instalação
- ✨ **Performance otimizada** - Cache inteligente e carregamento rápido

## 🚀 Funcionalidades Principais

### 🏢 Pontos de Coleta
- Cadastro e gerenciamento de pontos de coleta por usuários
- Informações completas: endereço, horário de funcionamento, contatos
- Visualização de todos os pontos disponíveis com sistema de busca
- Perfil detalhado de cada ponto com itens disponíveis

### 📦 Gestão de Estoque
- Adição de itens ao estoque do ponto de coleta
- Categorização automática (Roupas, Alimentos, Móveis, Eletrônicos, etc.)
- Controle de quantidade disponível em tempo real
- Indicação de urgência (baixa, média, alta, urgente)
- Dashboard personalizado para gestão do estoque

### 📝 Solicitações de Retirada
- Receptores solicitam itens com justificativa
- Sistema de aprovação por responsáveis do ponto
- Workflow completo: pendente → aprovada → concluída
- Possibilidade de recusa com observações
- Histórico completo de todas as solicitações

### 💬 Comunidade
- Posts públicos relacionados aos pontos de coleta
- Sistema de comentários com respostas aninhadas
- Posts fixados para campanhas e avisos importantes
- Contador de visualizações
- Engajamento entre doadores, gestores e receptores

### 👤 Perfis de Usuário
- Tipos de usuário: Doador, Receptor ou Ambos
- Estatísticas de doações e recebimentos
- Histórico completo de atividades
- Perfil editável com informações de contato

## 🛠️ Tecnologias Utilizadas

### Backend
- **Framework:** Django 4.2.7
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Environment:** python-dotenv 1.0.0
- **Forms:** django-crispy-forms + crispy-bootstrap5
- **Imagens:** Pillow (processamento de uploads)
- **Static Files:** whitenoise (servir arquivos estáticos)

### Frontend & PWA
- **UI Framework:** Bootstrap 5.3.2 + Bootstrap Icons 1.11.1
- **PWA:** Service Worker + Web App Manifest
- **Cache Strategy:** Network First com Cache Fallback
- **Offline Support:** Página offline customizada
- **Install Prompt:** Botão flutuante inteligente

## � Progressive Web App (PWA)

### ✨ Recursos PWA Implementados

#### Service Worker
- ✅ **Cache inteligente** - Network First com fallback para cache
- ✅ **Modo offline** - Funciona sem conexão com página customizada
- ✅ **Background sync** - Sincronização automática ao reconectar
- ✅ **Update detection** - Notifica usuário sobre novas versões
- ✅ **Cache versioning** - Gerenciamento automático de cache

#### Instalação
- ✅ **Botão flutuante** - Ícone verde no canto inferior direito
- ✅ **Auto-detecção** - Esconde automaticamente se já instalado
- ✅ **Prompt nativo** - Integração com beforeinstallprompt API
- ✅ **Multi-plataforma** - Chrome, Edge, Safari (iOS limitado)

#### Manifest
- ✅ **8 ícones PWA** - De 72x72 até 512x512 pixels
- ✅ **Shortcuts** - Atalhos para páginas principais
- ✅ **Theme color** - Verde (#2E7D32) integrado ao SO
- ✅ **Display standalone** - Abre como app nativo
- ✅ **Share Target** - Integração com compartilhamento nativo

#### UX Features
- ✅ **Online/offline banner** - Feedback visual de conexão
- ✅ **Lazy loading** - Carregamento eficiente de imagens
- ✅ **Fade-in animations** - Transições suaves
- ✅ **Web Share API** - Compartilhamento nativo
- ✅ **Auto-hide alerts** - Mensagens desaparecem automaticamente

### 🎨 Customizar Ícones PWA

Os ícones atuais usam as iniciais "SD". Para personalizar:

```bash
# 1. Coloque uma imagem quadrada (512x512 ou maior) como icon_base.png na raiz
# 2. Execute o gerador automático:
python generate_icons.py

# 3. Recoletar arquivos estáticos:
python manage.py collectstatic --noinput
```

O script gerará automaticamente:
- 8 ícones PWA (72px a 512px)
- favicon.ico multi-size
- Otimização automática

### 📊 Testar PWA

#### Chrome DevTools (F12)
```
Application → Manifest ✅ Válido
Application → Service Workers ✅ Ativo
Application → Cache Storage ✅ Populado
Network → Offline → Reload ✅ Página offline
```

#### Lighthouse Audit
```
DevTools → Lighthouse → PWA
Meta: Score 90+ pontos
```

#### Instalação Desktop
1. Clique no botão flutuante verde (canto inferior direito)
2. OU clique no ícone ➕ na barra de endereço
3. Confirme "Instalar"
4. App abre em janela separada

#### Instalação Mobile
1. Chrome Android: Menu ⋮ → "Instalar aplicativo"
2. Safari iOS: Compartilhar → "Adicionar à Tela Inicial"
3. Ícone aparece na tela inicial

### 🚀 PWA em Produção

**⚠️ HTTPS Obrigatório** - PWA requer SSL certificado

Configure o arquivo `.env`:
```bash
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
SECRET_KEY=sua_chave_secreta_aqui
```

Certifique-se de ter HTTPS configurado (Let's Encrypt, Cloudflare, etc.)

---

## ��� Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/smart-donation.git
cd smart-donation
```

2. **Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```bash
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Ou gere uma SECRET_KEY automaticamente:
```bash
python generate_secret_key.py
```

5. **Configure o banco de dados**
```bash
python manage.py migrate
```

6. **Colete arquivos estáticos (PWA)**
```bash
python manage.py collectstatic --noinput
```

7. **Crie um superusuário (admin)**
```bash
python manage.py createsuperuser
```

8. **Popule o banco com dados de teste (opcional)**
```bash
python manage.py popular_db --completo
```

Isso criará:
- 8 categorias de itens
- 5 usuários de exemplo (senha: senha123)
- 3 pontos de coleta
- 11 itens no estoque
- 6 solicitações de retirada (vários status)
- 5 posts da comunidade
- 10 comentários com respostas

9. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

10. **Acesse a aplicação**
- Interface principal: http://127.0.0.1:8000/
- Painel administrativo: http://127.0.0.1:8000/admin/
- **Botão de instalação PWA**: Aparece automaticamente no canto inferior direito 🎯

## 📁 Estrutura do Projeto

```
smart-donation/
├── config/                  # Configurações do Django
│   ├── settings.py         # Configurações principais (com .env)
│   ├── urls.py             # URLs raiz
│   └── wsgi.py             # WSGI para deploy
├── doacoes/                 # App principal
│   ├── models.py           # 10 modelos do sistema
│   ├── views.py            # 28 views organizadas
│   ├── urls.py             # 43 rotas mapeadas
│   ├── forms.py            # 8 formulários com validação
│   ├── admin.py            # Interface administrativa
│   ├── management/         # Comandos personalizados
│   │   └── commands/
│   │       └── popular_db.py
│   └── migrations/         # Migrações do banco
├── templates/               # Templates HTML
│   ├── base.html           # Template base (com PWA)
│   ├── offline.html        # Página offline (PWA)
│   ├── home.html           # Página inicial
│   ├── ponto_coleta_*.html # Templates de pontos
│   ├── *_estoque.html      # Templates de estoque
│   ├── solicitacao_*.html  # Templates de solicitações
│   ├── comunidade.html     # Templates da comunidade
│   └── perfil.html         # Perfil do usuário
├── static/                  # Arquivos estáticos (PWA)
│   ├── css/
│   │   └── style.css       # 300+ linhas (com estilos PWA)
│   ├── js/
│   │   └── app.js          # 350+ linhas (PWA features)
│   ├── icons/              # Ícones PWA (8 tamanhos)
│   │   ├── icon-72x72.png
│   │   ├── icon-192x192.png
│   │   └── icon-512x512.png
│   ├── sw.js               # Service Worker (200+ linhas)
│   ├── manifest.json       # Web App Manifest
│   └── favicon.ico         # Favicon multi-size
├── staticfiles/             # Arquivos coletados (produção)
├── media/                   # Uploads de usuários
├── .env                     # Variáveis de ambiente (não versionado)
├── requirements.txt         # Dependências Python
├── generate_icons.py        # Gerador automático de ícones PWA
├── generate_secret_key.py   # Gerador de SECRET_KEY
├── manage.py               # CLI do Django
└── README.md               # Este arquivo (documentação completa)
```

## 📊 Modelos do Sistema

### Core Models
- **Categoria**: Categorização de itens (Roupas, Alimentos, Móveis, etc.)
- **Perfil**: Extensão do User com dados adicionais

### Pontos de Coleta
- **PontoColeta**: Centros de distribuição gerenciados por usuários
- **ItemEstoque**: Itens disponíveis em cada ponto
- **SolicitacaoRetirada**: Pedidos de retirada com workflow de aprovação

### Comunidade
- **PostComunidade**: Posts públicos relacionados aos pontos
- **ComentarioPost**: Comentários com sistema de respostas aninhadas

## 🔐 Usuários de Teste

Após executar `python manage.py popular_db --completo`:

| Username | Tipo | Senha | Ponto de Coleta |
|----------|------|-------|-----------------|
| maria_silva | Doador | senha123 | Centro de Doações Zona Sul - SP |
| joao_santos | Ambos | senha123 | Ponto Solidário Copacabana |
| ana_costa | Doador | senha123 | Espaço Doar - BH |
| carlos_oliveira | Receptor | senha123 | - |
| pedro_receptor | Receptor | senha123 | - |

## 🎯 Botão Flutuante de Instalação PWA

### Como Funciona

Um **botão verde circular** aparece no canto inferior direito da tela quando:
- ✅ O app **não está instalado**
- ✅ O navegador **suporta instalação** (Chrome, Edge, Safari)
- ✅ Todos os **requisitos PWA** estão atendidos

### Comportamento Inteligente

O botão:
- 🎨 Tem **animação pulsante** para chamar atenção
- 🔴 Exibe um **badge vermelho** indicando ação disponível
- 💬 Mostra **tooltip "Instalar App"** ao passar o mouse
- ✨ **Desaparece automaticamente** após instalação
- 📱 É **responsivo** - menor em mobile (56px vs 60px)

### Ao Clicar

1. Exibe o prompt nativo do navegador
2. Usuário confirma instalação
3. App é instalado como aplicativo nativo
4. Botão desaparece com animação suave
5. Próximos acessos já serão no modo standalone

### Detecção de Instalação

O sistema detecta automaticamente se o app já está instalado via:
- `display-mode: standalone` (Chrome/Edge)
- `window.navigator.standalone` (Safari iOS)
- `document.referrer` (Android WebAPK)

---

## 🐛 Troubleshooting

### Botão de instalação não aparece

**Possíveis causas:**
- ✅ App já está instalado (comportamento normal)
- ❌ Navegador não suporta PWA (use Chrome/Edge)
- ❌ Faltam ícones obrigatórios (192x192 e 512x512)
- ❌ Manifest.json inválido ou não carregado
- ❌ Service Worker não registrou

**Solução:**
```bash
# 1. Verificar ícones
python generate_icons.py

# 2. Recoletar estáticos
python manage.py collectstatic --noinput

# 3. Limpar cache do navegador
# DevTools (F12) → Application → Clear Storage

# 4. Hard reload
# Ctrl + Shift + R (Windows/Linux)
# Cmd + Shift + R (Mac)
```

### Service Worker não registra

**Sintomas:** Console mostra erro de registro

**Solução:**
```bash
# 1. Verificar se está em localhost ou HTTPS
# PWA só funciona em ambiente seguro

# 2. Limpar Service Workers antigos
# DevTools → Application → Service Workers → Unregister

# 3. Verificar erros no console (F12)

# 4. Verificar arquivo sw.js
# http://localhost:8000/static/sw.js deve retornar 200
```

### Página offline não funciona

**Sintomas:** Mostra erro do Chrome em vez da página customizada

**Solução:**
```bash
# 1. Aguardar Service Worker instalar (5-10 segundos)

# 2. Verificar cache no DevTools
# Application → Cache Storage → smart-donation-v1

# 3. Garantir que /offline/ está em cache

# 4. Testar:
# Network → Offline → Reload
```

### Ícones não aparecem no manifest

**Sintomas:** Manifest mostra ícones sem preview

**Solução:**
```bash
# 1. Verificar se arquivos existem
ls static/icons/

# 2. Regerar ícones
python generate_icons.py

# 3. Recoletar
python manage.py collectstatic --noinput

# 4. Verificar no navegador
# http://localhost:8000/static/icons/icon-192x192.png
```

### Erro ao gerar ícones

**Sintomas:** `ModuleNotFoundError: No module named 'PIL'`

**Solução:**
```bash
pip install Pillow
python generate_icons.py
```

---

## 📊 Status do Projeto

| Categoria | Status | Detalhes |
|-----------|--------|----------|
| **Backend** | ✅ Estável | Django 4.2.7 |
| **Frontend** | ✅ Estável | Bootstrap 5.3.2 |
| **PWA** | ✅ Completo | 100% funcional |
| **Mobile** | ✅ Responsivo | PWA instalável |
| **Offline** | ✅ Funciona | Service Worker ativo |
| **Performance** | ✅ Otimizado | Lighthouse 90+ |
| **Segurança** | ✅ .env | SECRET_KEY protegida |