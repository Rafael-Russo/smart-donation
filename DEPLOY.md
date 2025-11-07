# 🚀 Guia de Deploy no PythonAnywhere

Este guia mostrará como fazer o deploy gratuito do projeto Smart Donation (PWA) no PythonAnywhere.

## ✅ Checklist Rápido

Antes de começar, certifique-se de ter:
- [ ] Conta no PythonAnywhere (gratuita)
- [ ] Código do projeto (Git ou ZIP)
- [ ] Arquivo `.env.example` no projeto (template)
- [ ] Script `generate_secret_key.py` disponível

## 📋 Pré-requisitos

1. Conta no PythonAnywhere (gratuita): https://www.pythonanywhere.com/registration/register/beginner/
2. Código do projeto no GitHub (recomendado) ou arquivo ZIP
3. Conhecimento básico de terminal Linux

## 🔧 Passo a Passo

### 1. Criar Conta no PythonAnywhere
- Acesse: https://www.pythonanywhere.com/registration/register/beginner/
- Crie sua conta gratuita (Beginner Account)
- Faça login

### 2. Abrir Console Bash
- No Dashboard, clique em "Consoles"
- Abra um novo console "Bash"

### 3. Fazer Upload do Código

#### Opção A: Usando Git (Recomendado)
```bash
git clone https://github.com/seu-usuario/smart-donation.git
cd smart-donation
```

#### Opção B: Upload Manual
- Use a aba "Files" para fazer upload do arquivo ZIP
- Extraia o arquivo no diretório home

### 4. Criar Ambiente Virtual
```bash
mkvirtualenv --python=/usr/bin/python3.10 smart-donation-env
```

### 5. Configurar MySQL no PythonAnywhere

**No Dashboard do PythonAnywhere:**

1. Vá para a aba **"Databases"**
2. Na seção **"MySQL"**, defina uma senha (anote!)
3. Clique em **"Initialize MySQL"** (se ainda não inicializou)
4. Em **"Create a database"**, crie: `seuusuario$smart_donation`
   - Substitua `seuusuario` pelo seu username
   - Exemplo: `rafael$smart_donation`

**Anote as informações:**
- 📝 Database name: `seuusuario$smart_donation`
- 📝 Database user: `seuusuario` (mesmo que seu username)
- 📝 Database password: (a senha que você definiu)
- 📝 Database host: `seuusuario.mysql.pythonanywhere-services.com`

### 6. Instalar Dependências
```bash
cd smart-donation
pip install -r requirements.txt
```

**⚠️ Importante: Instale o driver MySQL:**
```bash
pip install mysqlclient
```

### 7. Configurar Arquivo .env (Variáveis de Ambiente)

**O projeto já tem um arquivo `.env.example` como template!**

Copie o arquivo de exemplo e edite:

```bash
# Copie o template
cp .env.example .env

# Edite o arquivo
nano .env
```

**Configure as seguintes variáveis para PRODUÇÃO:**

```bash
# Django
SECRET_KEY=sua-chave-secreta-super-complexa-aqui
DEBUG=False
ALLOWED_HOSTS=seuusuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://seuusuario.pythonanywhere.com

# MySQL (PythonAnywhere)
DB_ENGINE=django.db.backends.mysql
DB_NAME=seuusuario$smart_donation
DB_USER=seuusuario
DB_PASSWORD=sua-senha-mysql-aqui
DB_HOST=seuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**⚠️ Importante sobre MySQL no PythonAnywhere:**
1. O nome do banco deve seguir o padrão: `seuusuario$nome_do_banco`
2. O host é: `seuusuario.mysql.pythonanywhere-services.com`
3. Você precisa criar o banco no painel do PythonAnywhere primeiro!

**⚠️ IMPORTANTE:**
1. **SECRET_KEY**: Gere uma nova chave segura (não use a do desenvolvimento!)
2. **DEBUG**: Deve ser `False` em produção
3. **ALLOWED_HOSTS**: Substitua `seuusuario` pelo seu username do PythonAnywhere

**Para gerar uma SECRET_KEY segura:**
```bash
python generate_secret_key.py
```

Ou use Python diretamente:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Salve o arquivo:
- `Ctrl + O` (Enter para confirmar)
- `Ctrl + X` (para sair)

### 8. Configurar Charset do Banco (UTF-8 para emojis)

**⚠️ IMPORTANTE: Execute antes de criar as tabelas!**

```bash
# Conectar ao MySQL
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p

# No prompt do MySQL, executar:
ALTER DATABASE `seuusuario$smart_donation` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verificar a configuração:
SHOW CREATE DATABASE `seuusuario$smart_donation`;

# Sair do MySQL
exit
```

**Por que fazer isso?**
- Suporta emojis e caracteres especiais (🎄, 🎁, ❤️, etc.)
- Evita erro: "Incorrect string value: '\\xF0\\x9F\\x8E\\x84'"

### 9. Configurar Banco de Dados (MySQL)
```bash
# Testar conexão com MySQL
python manage.py check --database default

# Criar tabelas no MySQL
python manage.py migrate

# Popular com dados de exemplo (opcional)
python manage.py popular_db --completo

# Criar superusuário
python manage.py createsuperuser
```

**Se houver erro de conexão MySQL:**
```bash
# Verificar se mysqlclient está instalado
pip list | grep mysqlclient

# Se não estiver, instale:
pip install mysqlclient
```

### 10. Coletar Arquivos Estáticos (PWA)
```bash
python manage.py collectstatic --noinput
```

### 11. Configurar Web App

#### Na aba "Web":
1. Clique em "Add a new web app"
2. Escolha "Manual configuration"
3. Selecione Python 3.10

#### Configurar Virtual Environment:
- Na seção "Virtualenv"
- Cole o caminho: `/home/seuusuario/.virtualenvs/smart-donation-env`
- Substitua `seuusuario` pelo seu username do PythonAnywhere

#### Configurar WSGI:
1. Clique no link do arquivo WSGI
2. Apague todo o conteúdo
3. Cole o seguinte código:

```python
import os
import sys

# Adicionar o projeto ao path
path = '/home/seuusuario/smart-donation'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Importar aplicação Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Importante:** Substitua `seuusuario` pelo seu username!

#### Configurar Arquivos Estáticos:
Na seção "Static files", adicione:

| URL | Directory |
|-----|-----------|
| /static/ | /home/seuusuario/smart-donation/staticfiles |
| /media/ | /home/seuusuario/smart-donation/media |

**Lembre-se de substituir `seuusuario`!**

### 12. Verificar Configurações

O arquivo `.env` já foi configurado no passo 7, mas verifique se o `config/settings.py` está carregando corretamente:

```bash
nano config/settings.py
```

Verifique se tem estas linhas no início do arquivo:

```python
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

✅ Se já estiver configurado assim, está tudo certo!

### 13. Recarregar a Aplicação
- Na aba "Web", clique no botão verde "Reload"
- Aguarde alguns segundos

### 14. Acessar seu Site
Acesse: `https://seuusuario.pythonanywhere.com`

## 🎉 Pronto!
Seu aplicativo PWA está no ar! 

**Teste:**
- ✅ Home: `https://seuusuario.pythonanywhere.com/`
- ✅ Admin: `https://seuusuario.pythonanywhere.com/admin`
- ✅ PWA: Clique no botão verde flutuante para instalar
- ✅ Offline: Teste desconectando a internet

## 🔄 Atualizando o Código

Quando fizer alterações no código:

```bash
# No console Bash do PythonAnywhere
cd smart-donation
git pull  # Se estiver usando Git

# Ativar ambiente virtual
workon smart-donation-env

# Aplicar novas migrações (se houver)
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

Depois, vá na aba "Web" e clique em "Reload"

## 🐛 Troubleshooting

### Erro 500 - Internal Server Error
1. **Verifique o arquivo .env:**
   ```bash
   # Confirme que o arquivo existe
   ls -la .env
   
   # Verifique o conteúdo (sem expor valores sensíveis)
   cat .env | grep -v SECRET_KEY
   ```
2. **Verifique as variáveis de ambiente:**
   - SECRET_KEY está definida?
   - DEBUG=False (não True)?
   - ALLOWED_HOSTS contém seu domínio?
3. Verifique o log de erros na aba "Web" → "Log files" → "Error log"
4. Confirme se o ALLOWED_HOSTS está correto
5. Verifique se o caminho no arquivo WSGI está correto

### Erro: "SECRET_KEY não definida" ou "ALLOWED_HOSTS vazio"
1. **Arquivo .env não foi criado:**
   ```bash
   # Crie o arquivo
   nano .env
   # Cole o conteúdo do passo 6
   ```
2. **python-dotenv não instalado:**
   ```bash
   pip install python-dotenv
   ```
3. **Arquivo .env no lugar errado:**
   ```bash
   # Deve estar na raiz do projeto, junto com manage.py
   pwd  # Confirme que está em /home/seuusuario/smart-donation
   ls -la .env  # Deve listar o arquivo
   ```

### Arquivos estáticos não carregam
1. Execute `python manage.py collectstatic` novamente
2. Verifique os caminhos na seção "Static files"
3. Certifique-se de ter recarregado a aplicação

### Erro de importação
1. Verifique se o ambiente virtual está ativado
2. Confirme se todas as dependências foram instaladas: `pip list`
3. Verifique o caminho no arquivo WSGI

### Erro de conexão MySQL
1. **Verifique as credenciais no .env:**
   ```bash
   cat .env | grep DB_
   ```
2. **Formato correto do nome do banco:**
   - ✅ Correto: `seuusuario$smart_donation`
   - ❌ Errado: `smart_donation` (sem prefixo)
3. **Host correto:**
   - ✅ Correto: `seuusuario.mysql.pythonanywhere-services.com`
   - ❌ Errado: `localhost` ou `127.0.0.1`
4. **Instalar mysqlclient:**
   ```bash
   pip install mysqlclient
   ```
5. **Verificar se o banco foi criado:**
   - Aba "Databases" → deve aparecer `seuusuario$smart_donation`

### Erro: "Can't connect to MySQL server"
```bash
# Testar conexão manualmente
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p

# Se funcionar, o problema está no .env
# Verifique DB_HOST, DB_USER, DB_PASSWORD
```

### Erro: "Incorrect string value" com emojis
**Erro completo:**
```
MySQLdb.OperationalError: (1366, "Incorrect string value: '\\xF0\\x9F\\x8E\\x84' for column 'conteudo'")
```

**Causa:** Banco não configurado com charset utf8mb4

**Solução:**
```bash
# 1. Conectar ao MySQL
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p

# 2. Alterar charset do banco
ALTER DATABASE `seuusuario$smart_donation` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. Se as tabelas já existem, pode ser necessário recriá-las:
exit
python manage.py migrate --run-syncdb

# 4. Ou popular novamente
python manage.py popular_db --completo
```

**Nota:** O settings.py já está configurado com `'charset': 'utf8mb4'`, mas o banco precisa ser configurado também.

### Banco de dados não encontrado (SQLite antigo)
Se estava usando SQLite e migrou para MySQL:
1. Exporte dados do SQLite (se necessário):
   ```bash
   python manage.py dumpdata > backup.json
   ```
2. Configure MySQL no .env
3. Execute migrate
4. Importe dados (se necessário):
   ```bash
   python manage.py loaddata backup.json
   ```

## 📝 Notas Importantes

1. **Conta Gratuita:** Limites da conta gratuita
   - 1 aplicação web
   - 512 MB de espaço em disco
   - 1 banco MySQL com 512 MB
   - Aplicação "dorme" após inatividade (acorda automaticamente ao acessar)

2. **Segurança (⚠️ CRÍTICO):**
   - ✅ **Arquivo .env configurado** com SECRET_KEY única
   - ✅ **DEBUG=False** em produção
   - ✅ **ALLOWED_HOSTS** restrito ao seu domínio
   - ❌ **NUNCA commite o arquivo .env** no Git!
   - ✅ Use o arquivo `.env.example` como template (sem valores reais)

3. **Arquivo .env:**
   ```bash
   # Adicione ao .gitignore se ainda não estiver
   echo ".env" >> .gitignore
   
   # Crie um template para referência (sem valores sensíveis)
   cp .env .env.example
   # Edite .env.example e remova os valores reais
   ```

4. **Backup:**
   - Faça backup regular do banco de dados
   - Faça backup do arquivo `.env` em local seguro
   - Use Git para controle de versão (exceto .env)

## 🔗 Links Úteis

- [Documentação PythonAnywhere](https://help.pythonanywhere.com/)
- [Deploy Django no PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Documentação Django](https://docs.djangoproject.com/)

## 💡 Dicas

1. Use o console Bash para testar comandos
2. Monitore os logs de erro regularmente
3. Teste localmente antes de fazer deploy
4. Mantenha o código no Git para facilitar atualizações

---

**Boa sorte com seu deploy! 🚀**
