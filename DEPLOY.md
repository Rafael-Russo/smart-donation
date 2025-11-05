# 🚀 Guia de Deploy no PythonAnywhere

Este guia mostrará como fazer o deploy gratuito do projeto Doação Inteligente no PythonAnywhere.

## 📋 Pré-requisitos

1. Conta no PythonAnywhere (gratuita): https://www.pythonanywhere.com/registration/register/beginner/
2. Código do projeto no GitHub (recomendado) ou arquivo ZIP

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

### 5. Instalar Dependências
```bash
cd smart-donation
pip install -r requirements.txt
```

### 6. Configurar Banco de Dados
```bash
python manage.py migrate
python manage.py popular_db
python manage.py createsuperuser
```

### 7. Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### 8. Configurar Web App

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

### 9. Atualizar Settings.py

No arquivo `config/settings.py`, adicione seu domínio ao ALLOWED_HOSTS:

```python
ALLOWED_HOSTS = ['seuusuario.pythonanywhere.com', 'localhost', '127.0.0.1']
```

Para editar o arquivo no PythonAnywhere:
```bash
nano config/settings.py
# ou use a aba "Files" para editar pelo navegador
```

### 10. Recarregar a Aplicação
- Na aba "Web", clique no botão verde "Reload"
- Aguarde alguns segundos

### 11. Acessar seu Site
Acesse: `https://seuusuario.pythonanywhere.com`

## 🎉 Pronto!
Seu aplicativo está no ar! Acesse o admin em `/admin` com as credenciais que você criou.

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
1. Verifique o log de erros na aba "Web" → "Log files" → "Error log"
2. Confirme se o ALLOWED_HOSTS está correto
3. Verifique se o caminho no arquivo WSGI está correto

### Arquivos estáticos não carregam
1. Execute `python manage.py collectstatic` novamente
2. Verifique os caminhos na seção "Static files"
3. Certifique-se de ter recarregado a aplicação

### Erro de importação
1. Verifique se o ambiente virtual está ativado
2. Confirme se todas as dependências foram instaladas: `pip list`
3. Verifique o caminho no arquivo WSGI

### Banco de dados não encontrado
1. Verifique se executou `python manage.py migrate`
2. Confirme que o arquivo `db.sqlite3` existe no diretório do projeto

## 📝 Notas Importantes

1. **Conta Gratuita:** Limites da conta gratuita
   - 1 aplicação web
   - 512 MB de espaço em disco
   - Aplicação "dorme" após inatividade (acorda automaticamente ao acessar)

2. **Segurança:**
   - Mude o SECRET_KEY em produção
   - Configure DEBUG=False em produção
   - Use variáveis de ambiente para dados sensíveis

3. **Backup:**
   - Faça backup regular do banco de dados
   - Use Git para controle de versão

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
