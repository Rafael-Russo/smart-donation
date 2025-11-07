# 🐬 Configuração MySQL para Produção - PythonAnywhere

## ✅ Mudanças Implementadas

### 1. **requirements.txt** atualizado
```diff
+ mysqlclient==2.2.0
```

### 2. **.env.example** atualizado
```bash
# MySQL (produção - PythonAnywhere)
DB_ENGINE=django.db.backends.mysql
DB_NAME=seuusuario$smart_donation
DB_USER=seuusuario
DB_PASSWORD=sua-senha-mysql-aqui
DB_HOST=seuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

### 3. **DEPLOY.md** atualizado
- ✅ Novo Passo 5: Configurar MySQL no PythonAnywhere
- ✅ Instruções para criar banco de dados
- ✅ Instalação do mysqlclient
- ✅ Troubleshooting específico para MySQL
- ✅ Comandos para testar conexão

---

## 🎯 Configuração do .env para Produção

### Template Completo

```bash
# ========================================
# DJANGO
# ========================================
SECRET_KEY=sua-chave-secreta-super-complexa-e-aleatoria-de-50-chars
DEBUG=False
ALLOWED_HOSTS=seuusuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://seuusuario.pythonanywhere.com

# ========================================
# MYSQL (PythonAnywhere)
# ========================================
DB_ENGINE=django.db.backends.mysql
DB_NAME=seuusuario$smart_donation
DB_USER=seuusuario
DB_PASSWORD=sua-senha-mysql-definida-no-painel
DB_HOST=seuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

### Exemplo Real (substitua os valores)

Se seu username do PythonAnywhere é `rafael`:

```bash
SECRET_KEY=gere-com-python-generate-secret-key-py
DEBUG=False
ALLOWED_HOSTS=rafael.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://rafael.pythonanywhere.com

DB_ENGINE=django.db.backends.mysql
DB_NAME=rafael$smart_donation
DB_USER=rafael
DB_PASSWORD=MinhaS3nh@MySQL123
DB_HOST=rafael.mysql.pythonanywhere-services.com
DB_PORT=3306
```

---

## 📋 Passo a Passo Resumido

### No PythonAnywhere Dashboard

1. **Aba "Databases"**
   ```
   → Defina uma senha MySQL (anote!)
   → Click "Initialize MySQL"
   → Create database: seuusuario$smart_donation
   ```

2. **Anote as credenciais:**
   - Database: `seuusuario$smart_donation`
   - User: `seuusuario`
   - Password: (sua senha)
   - Host: `seuusuario.mysql.pythonanywhere-services.com`

### No Console Bash

3. **Instalar mysqlclient:**
   ```bash
   pip install mysqlclient
   ```

4. **Configurar .env:**
   ```bash
   cp .env.example .env
   nano .env
   # Cole as configurações acima
   ```

5. **Testar conexão:**
   ```bash
   python manage.py check --database default
   ```

6. **Criar tabelas:**
   ```bash
   python manage.py migrate
   ```

---

## 🔍 Verificação

### Checar se MySQL está configurado

```bash
# Ver variáveis do .env
cat .env | grep DB_

# Deve retornar:
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=seuusuario$smart_donation
# DB_USER=seuusuario
# DB_PASSWORD=******
# DB_HOST=seuusuario.mysql.pythonanywhere-services.com
# DB_PORT=3306
```

### Testar conexão MySQL

```bash
# Opção 1: Via Django
python manage.py check --database default

# Opção 2: Via MySQL CLI
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p
# Digite a senha quando solicitar
# Se conectar, digite: SHOW DATABASES;
```

### Verificar tabelas criadas

```bash
python manage.py showmigrations

# Deve mostrar [X] em todas as migrações
```

---

## ⚠️ Pontos Críticos

### 1. Formato do Nome do Banco

**✅ CORRETO:**
```
seuusuario$smart_donation
rafael$smart_donation
joao$smart_donation
```

**❌ ERRADO:**
```
smart_donation          (falta prefixo)
seuusuario_smart_donation  (usa _ em vez de $)
seuusuario-smart_donation  (usa - em vez de $)
```

### 2. Host Correto

**✅ CORRETO:**
```
seuusuario.mysql.pythonanywhere-services.com
```

**❌ ERRADO:**
```
localhost
127.0.0.1
mysql.pythonanywhere.com
seuusuario.pythonanywhere.com
```

### 3. mysqlclient Instalado

```bash
# Verificar instalação
pip list | grep mysqlclient

# Se não aparecer:
pip install mysqlclient

# Se houver erro de compilação (Linux):
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

---

## 🐛 Troubleshooting MySQL

### Erro: "Can't connect to MySQL server"

**Causas:**
1. DB_HOST incorreto
2. DB_USER incorreto
3. Senha errada
4. Banco não foi criado no painel

**Solução:**
```bash
# 1. Verificar .env
cat .env | grep DB_

# 2. Testar conexão manual
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p

# 3. Se funcionar, problema está no .env
# Recrie o arquivo .env com as credenciais corretas
```

### Erro: "(1049, "Unknown database 'smart_donation'")"

**Causa:** Nome do banco sem prefixo do usuário

**Solução:**
```bash
# Mudar de:
DB_NAME=smart_donation

# Para:
DB_NAME=seuusuario$smart_donation
```

### Erro: "No module named 'MySQLdb'"

**Causa:** mysqlclient não instalado

**Solução:**
```bash
pip install mysqlclient
```

### Erro: "Access denied for user"

**Causa:** Senha incorreta ou usuário errado

**Solução:**
```bash
# 1. Confirme a senha no painel do PythonAnywhere
# Aba "Databases" → MySQL password

# 2. Atualize o .env com a senha correta
nano .env
# Edite DB_PASSWORD=senha-correta-aqui
```

---

## 📊 Diferenças SQLite vs MySQL

| Aspecto | SQLite (Dev) | MySQL (Prod) |
|---------|-------------|--------------|
| **Arquivo** | db.sqlite3 | Servidor remoto |
| **Concorrência** | Limitada | Alta |
| **Tamanho** | Sem limite local | 512MB (free) |
| **Backup** | Copiar arquivo | mysqldump |
| **Performance** | Boa (local) | Melhor (otimizado) |
| **Conexões** | 1 por vez | Múltiplas |

---

## 🔄 Migração SQLite → MySQL

Se já tem dados no SQLite e quer migrar:

```bash
# 1. Exportar dados do SQLite
python manage.py dumpdata --natural-foreign --natural-primary > backup.json

# 2. Configurar MySQL no .env
nano .env
# Adicionar configurações MySQL

# 3. Criar tabelas no MySQL
python manage.py migrate

# 4. Importar dados
python manage.py loaddata backup.json
```

**⚠️ Atenção:** Alguns tipos de dados podem precisar ajustes manuais.

---

## 📝 Checklist de Configuração

Antes de fazer deploy, confirme:

- [ ] MySQL criado no painel do PythonAnywhere
- [ ] Nome do banco: `seuusuario$smart_donation`
- [ ] Senha MySQL definida e anotada
- [ ] mysqlclient adicionado ao requirements.txt
- [ ] .env configurado com credenciais MySQL
- [ ] DB_ENGINE = `django.db.backends.mysql`
- [ ] DB_NAME com prefixo correto
- [ ] DB_HOST correto (*.mysql.pythonanywhere-services.com)
- [ ] Testado: `python manage.py check --database default`
- [ ] Executado: `python manage.py migrate`
- [ ] Criado superusuário

---

## 🎓 Comandos Úteis MySQL

```bash
# Conectar ao MySQL
mysql -h seuusuario.mysql.pythonanywhere-services.com -u seuusuario -p

# Dentro do MySQL:
SHOW DATABASES;                    # Listar bancos
USE seuusuario$smart_donation;     # Selecionar banco
SHOW TABLES;                       # Listar tabelas
SELECT COUNT(*) FROM auth_user;    # Contar usuários
EXIT;                              # Sair
```

---

## 📚 Referências

- [PythonAnywhere MySQL](https://help.pythonanywhere.com/pages/UsingMySQL/)
- [Django MySQL Backend](https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes)
- [mysqlclient](https://pypi.org/project/mysqlclient/)

---

**✅ Configuração MySQL completa e pronta para produção!**
