# 🚀 Comandos Rápidos - Doação Inteligente

## ⚡ Início Rápido

### Primeira vez rodando o projeto:
```powershell
# 1. Ativar ambiente virtual
.venv\Scripts\activate

# 2. Criar superusuário (admin)
python manage.py createsuperuser

# 3. Iniciar servidor
python manage.py runserver
```

### Acessos:
- **Site:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 📋 Comandos do Django

### Servidor
```powershell
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Iniciar em porta diferente
python manage.py runserver 8080

# Parar servidor: Ctrl+C
```

### Banco de Dados
```powershell
# Criar migrações (após alterar models)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Popular apenas categorias
python manage.py popular_db

# Popular com dados completos (usuários + doações de exemplo)
python manage.py popular_db --completo

# Shell interativo
python manage.py shell
```

### Usuários
```powershell
# Criar superusuário
python manage.py createsuperuser

# Alterar senha de usuário
python manage.py changepassword username
```

### Arquivos Estáticos
```powershell
# Coletar todos os arquivos estáticos (para deploy)
python manage.py collectstatic

# Coletar sem confirmação
python manage.py collectstatic --noinput
```

---

## 🔧 Desenvolvimento

### Criar novo app
```powershell
python manage.py startapp nome_do_app
```

### Verificar problemas
```powershell
python manage.py check
```

### Limpar sessões expiradas
```powershell
python manage.py clearsessions
```

---

## 🐍 Python/pip

### Ambiente Virtual
```powershell
# Ativar
.venv\Scripts\activate

# Desativar
deactivate
```

### Dependências
```powershell
# Instalar dependências
pip install -r requirements.txt

# Instalar nova biblioteca
pip install nome-biblioteca

# Atualizar requirements.txt
pip freeze > requirements.txt

# Listar pacotes instalados
pip list
```

---

## 📦 Git (Controle de Versão)

### Configuração Inicial
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/smart-donation.git
git push -u origin main
```

### Dia a Dia
```powershell
# Ver status
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "Descrição das mudanças"

# Push
git push

# Pull (baixar atualizações)
git pull
```

### Branches
```powershell
# Criar nova branch
git checkout -b nome-feature

# Mudar de branch
git checkout main

# Listar branches
git branch

# Merge
git merge nome-feature
```

---

## 🌐 PythonAnywhere (Deploy)

### Console Bash
```bash
# Navegar para projeto
cd smart-donation

# Ativar ambiente virtual
workon smart-donation-env

# Pull atualizações
git pull

# Aplicar migrações
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput
```

### Recarregar Web App
```bash
# Via comando (se disponível)
touch /var/www/seuusuario_pythonanywhere_com_wsgi.py

# Ou: Web tab > Reload button
```

---

## 🧪 Testes e Debug

### Shell Python
```powershell
# Abrir shell Django
python manage.py shell

# Exemplo de uso no shell:
>>> from doacoes.models import Doacao, Categoria
>>> Doacao.objects.all()
>>> Categoria.objects.count()
```

### Verificar URLs
```powershell
python manage.py show_urls  # Se instalado django-extensions
```

### SQL queries
```powershell
# Ver SQL das migrações
python manage.py sqlmigrate doacoes 0001
```

---

## 📊 Dados de Teste

### Via Shell
```python
python manage.py shell

# Criar categoria
from doacoes.models import Categoria
cat = Categoria.objects.create(nome="Teste", descricao="Categoria de teste")

# Criar doação
from django.contrib.auth.models import User
from doacoes.models import Doacao, Categoria

doador = User.objects.first()
cat = Categoria.objects.first()

doacao = Doacao.objects.create(
    doador=doador,
    titulo="Item de Teste",
    descricao="Descrição do item",
    categoria=cat,
    quantidade=1,
    condicao="Novo",
    status="disponivel",
    urgencia="media",
    endereco_retirada="Rua Teste, 123",
    cidade="São Paulo",
    estado="SP"
)
```

---

## 🔍 Troubleshooting

### Erro: ModuleNotFoundError
```powershell
# Certifique-se de ativar o ambiente virtual
.venv\Scripts\activate
```

### Erro: No such table
```powershell
# Aplicar migrações
python manage.py migrate
```

### Erro: Static files não carregam
```powershell
# Coletar arquivos estáticos
python manage.py collectstatic
```

### Limpar cache do navegador
```
Ctrl + F5 ou Ctrl + Shift + R
```

### Ver logs de erro (Django)
```powershell
# Terminal onde o runserver está rodando mostra os erros
# Ou verificar arquivo de log se configurado
```

---

## 📝 Atalhos Úteis

### VS Code
- `Ctrl + `` - Abrir terminal
- `Ctrl + P` - Buscar arquivo
- `Ctrl + Shift + F` - Buscar em todos os arquivos
- `F5` - Debug

### Terminal
- `Ctrl + C` - Parar processo
- `Ctrl + L` - Limpar terminal
- `Tab` - Autocompletar
- `↑` - Comando anterior

---

## 🎯 Workflow Recomendado

### Desenvolvimento Local
```powershell
# 1. Ativar venv
.venv\Scripts\activate

# 2. Iniciar servidor
python manage.py runserver

# 3. Fazer alterações no código

# 4. Se alterou models:
python manage.py makemigrations
python manage.py migrate

# 5. Testar no navegador

# 6. Commit das mudanças
git add .
git commit -m "Descrição"
git push
```

### Deploy (PythonAnywhere)
```bash
# 1. Conectar via SSH ou console web

# 2. Navegar e atualizar
cd smart-donation
git pull

# 3. Aplicar mudanças
workon smart-donation-env
python manage.py migrate
python manage.py collectstatic --noinput

# 4. Recarregar web app
touch /var/www/seuusuario_pythonanywhere_com_wsgi.py
```

---

## 💾 Backup

### Backup do Banco SQLite
```powershell
# Copiar arquivo do banco
copy db.sqlite3 backups\db_backup_2025-11-05.sqlite3

# Ou usar timestamp
copy db.sqlite3 backups\db_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sqlite3
```

### Backup de Media Files
```powershell
xcopy media backups\media_%date:~-4,4%%date:~-10,2%%date:~-7,2% /E /I
```

---

## 📞 Comandos de Diagnóstico

```powershell
# Versão do Python
python --version

# Versão do Django
python -m django --version

# Verificar instalação de pacotes
pip check

# Info do sistema
python manage.py diffsettings

# Verificar configuração
python manage.py check --deploy
```

---

**Mantenha este arquivo aberto durante o desenvolvimento! 📌**
