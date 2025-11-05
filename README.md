# Doação Inteligente

Aplicativo que conecta doadores de roupas, móveis, alimentos e outros itens a famílias e instituições em situação de vulnerabilidade social.

## Funcionalidades

- 📍 Localização de pontos de doação por geolocalização
- 🔍 Busca e filtro de itens por categoria
- 💬 Comunicação direta entre doadores e receptores
- ⭐ Sistema de avaliação e confiabilidade
- 🔔 Notificações sobre necessidades urgentes
- 📦 Categorização de itens doados

## Tecnologias

- Django 4.2
- SQLite
- Bootstrap 5
- PythonAnywhere (hospedagem gratuita)

## Instalação Local

1. Clone o repositório
```bash
git clone <seu-repositorio>
cd smart-donation
```

2. Crie um ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Execute o servidor
```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Deploy no PythonAnywhere

1. Faça upload dos arquivos
2. Configure o virtualenv com `requirements.txt`
3. Execute as migrações
4. Configure o arquivo WSGI conforme `pythonanywhere_wsgi.py`
5. Recarregue a aplicação

## Estrutura do Projeto

- `donations/` - App principal com models, views e templates
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `media/` - Upload de imagens de itens
- `templates/` - Templates base

## Licença

MIT
