from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from doacoes.models import Categoria, Perfil, Doacao
from django.utils import timezone


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais (categorias, usuários e doações de exemplo)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--completo',
            action='store_true',
            help='Popula com usuários e doações de exemplo (além das categorias)',
        )

    def handle(self, *args, **kwargs):
        completo = kwargs.get('completo', False)
        
        self.stdout.write(self.style.WARNING('\n=== POPULANDO BANCO DE DADOS ===\n'))
        
        # 1. CRIAR CATEGORIAS
        self.stdout.write('1. Criando categorias...')
        categorias = [
            {'nome': 'Roupas', 'descricao': 'Roupas infantis, femininas e masculinas', 'icone': 'bi-bag'},
            {'nome': 'Alimentos', 'descricao': 'Alimentos não perecíveis e cestas básicas', 'icone': 'bi-basket'},
            {'nome': 'Móveis', 'descricao': 'Móveis para casa e escritório', 'icone': 'bi-house'},
            {'nome': 'Eletrônicos', 'descricao': 'Computadores, celulares e eletrônicos', 'icone': 'bi-laptop'},
            {'nome': 'Brinquedos', 'descricao': 'Brinquedos infantis e jogos', 'icone': 'bi-controller'},
            {'nome': 'Livros', 'descricao': 'Livros, revistas e material educativo', 'icone': 'bi-book'},
            {'nome': 'Utensílios', 'descricao': 'Utensílios domésticos e cozinha', 'icone': 'bi-cup-straw'},
            {'nome': 'Outros', 'descricao': 'Outros itens diversos', 'icone': 'bi-three-dots'},
        ]
        
        categorias_criadas = {}
        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={
                    'descricao': cat_data['descricao'],
                    'icone': cat_data['icone']
                }
            )
            categorias_criadas[cat_data['nome']] = categoria
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Categoria "{categoria.nome}" criada'))
            else:
                self.stdout.write(f'   - Categoria "{categoria.nome}" já existe')
        
        if not completo:
            self.stdout.write(self.style.SUCCESS('\n✓ Categorias carregadas com sucesso!'))
            self.stdout.write(self.style.WARNING('\nPara popular com dados de exemplo (usuários e doações), use:'))
            self.stdout.write(self.style.WARNING('python manage.py popular_db --completo\n'))
            return
        
        # 2. CRIAR USUÁRIOS DE EXEMPLO
        self.stdout.write('\n2. Criando usuários de exemplo...')
        usuarios_data = [
            {
                'username': 'maria_silva',
                'email': 'maria@example.com',
                'first_name': 'Maria',
                'last_name': 'Silva',
                'perfil': {
                    'tipo': 'doador',
                    'telefone': '(11) 98765-4321',
                    'cidade': 'São Paulo',
                    'estado': 'SP',
                    'endereco': 'Rua das Flores, 123',
                    'cep': '01234-567'
                }
            },
            {
                'username': 'joao_santos',
                'email': 'joao@example.com',
                'first_name': 'João',
                'last_name': 'Santos',
                'perfil': {
                    'tipo': 'ambos',
                    'telefone': '(21) 99876-5432',
                    'cidade': 'Rio de Janeiro',
                    'estado': 'RJ',
                    'endereco': 'Av. Atlântica, 456',
                    'cep': '22000-000'
                }
            },
            {
                'username': 'ana_costa',
                'email': 'ana@example.com',
                'first_name': 'Ana',
                'last_name': 'Costa',
                'perfil': {
                    'tipo': 'doador',
                    'telefone': '(31) 97654-3210',
                    'cidade': 'Belo Horizonte',
                    'estado': 'MG',
                    'endereco': 'Rua da Liberdade, 789',
                    'cep': '30000-000'
                }
            },
            {
                'username': 'carlos_oliveira',
                'email': 'carlos@example.com',
                'first_name': 'Carlos',
                'last_name': 'Oliveira',
                'perfil': {
                    'tipo': 'receptor',
                    'telefone': '(41) 96543-2109',
                    'cidade': 'Curitiba',
                    'estado': 'PR',
                    'endereco': 'Rua XV de Novembro, 321',
                    'cep': '80000-000'
                }
            },
        ]
        
        usuarios_criados = {}
        for user_data in usuarios_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password('senha123')  # Senha padrão para usuários de exemplo
                user.save()
                self.stdout.write(self.style.SUCCESS(f'   ✓ Usuário "{user.username}" criado (senha: senha123)'))
            else:
                self.stdout.write(f'   - Usuário "{user.username}" já existe')
            
            # Criar ou atualizar perfil
            perfil, perfil_created = Perfil.objects.get_or_create(
                usuario=user,
                defaults=user_data['perfil']
            )
            
            if not perfil_created:
                for key, value in user_data['perfil'].items():
                    setattr(perfil, key, value)
                perfil.save()
            
            usuarios_criados[user_data['username']] = user
        
        # 3. CRIAR DOAÇÕES DE EXEMPLO
        self.stdout.write('\n3. Criando doações de exemplo...')
        doacoes_data = [
            {
                'doador': 'maria_silva',
                'titulo': 'Sofá 3 lugares em bom estado',
                'descricao': 'Sofá de 3 lugares, cor marrom, tecido em bom estado. Apenas alguns sinais de uso. Medidas: 2m x 0,90m x 0,80m. Precisa de carro grande para retirada.',
                'categoria': 'Móveis',
                'quantidade': 1,
                'condicao': 'Usado em bom estado',
                'status': 'disponivel',
                'urgencia': 'media',
                'endereco_retirada': 'Rua das Flores, 123 - Apto 45',
                'cidade': 'São Paulo',
                'estado': 'SP',
            },
            {
                'doador': 'maria_silva',
                'titulo': 'Roupas infantis (2-4 anos)',
                'descricao': 'Lote com 15 peças de roupas infantis para crianças de 2 a 4 anos. Inclui camisetas, calças, vestidos e macacões. Todas as peças estão limpas e em ótimo estado.',
                'categoria': 'Roupas',
                'quantidade': 15,
                'condicao': 'Usado em ótimo estado',
                'status': 'disponivel',
                'urgencia': 'baixa',
                'endereco_retirada': 'Rua das Flores, 123',
                'cidade': 'São Paulo',
                'estado': 'SP',
            },
            {
                'doador': 'joao_santos',
                'titulo': 'Notebook Dell - i5, 8GB RAM',
                'descricao': 'Notebook Dell Inspiron, processador Intel i5, 8GB de RAM, HD 500GB. Funcionando perfeitamente, apenas a bateria não segura mais carga (funciona apenas na tomada). Ideal para estudos.',
                'categoria': 'Eletrônicos',
                'quantidade': 1,
                'condicao': 'Usado - bateria com defeito',
                'status': 'disponivel',
                'urgencia': 'alta',
                'endereco_retirada': 'Av. Atlântica, 456 - Ed. Sol',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
            },
            {
                'doador': 'joao_santos',
                'titulo': 'Cesta básica completa',
                'descricao': 'Cesta básica com arroz (5kg), feijão (2kg), óleo, macarrão, açúcar, café, sal e biscoitos. Todos os produtos estão lacrados e dentro da validade.',
                'categoria': 'Alimentos',
                'quantidade': 1,
                'condicao': 'Novo - lacrado',
                'status': 'disponivel',
                'urgencia': 'urgente',
                'endereco_retirada': 'Av. Atlântica, 456',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
            },
            {
                'doador': 'ana_costa',
                'titulo': 'Kit livros didáticos ensino médio',
                'descricao': 'Coleção completa de livros didáticos do ensino médio. Inclui matemática, português, história, geografia, biologia, física e química. Pouquíssimo uso, apenas alguns grifos a lápis.',
                'categoria': 'Livros',
                'quantidade': 21,
                'condicao': 'Usado em ótimo estado',
                'status': 'disponivel',
                'urgencia': 'alta',
                'endereco_retirada': 'Rua da Liberdade, 789',
                'cidade': 'Belo Horizonte',
                'estado': 'MG',
            },
            {
                'doador': 'ana_costa',
                'titulo': 'Mesa de jantar 4 lugares',
                'descricao': 'Mesa de jantar redonda de madeira com 4 cadeiras estofadas. Mesa tem 1m de diâmetro. Móvel em excelente estado, apenas marcas leves de uso.',
                'categoria': 'Móveis',
                'quantidade': 1,
                'condicao': 'Usado em excelente estado',
                'status': 'disponivel',
                'urgencia': 'media',
                'endereco_retirada': 'Rua da Liberdade, 789 - Casa',
                'cidade': 'Belo Horizonte',
                'estado': 'MG',
            },
            {
                'doador': 'maria_silva',
                'titulo': 'Brinquedos diversos (carrinho, bonecas, jogos)',
                'descricao': 'Lote com aproximadamente 20 brinquedos variados: carrinhos, bonecas, jogos de tabuleiro, pelúcias e quebra-cabeças. Todos limpos e funcionando. Ideal para creches ou famílias.',
                'categoria': 'Brinquedos',
                'quantidade': 20,
                'condicao': 'Usado em bom estado',
                'status': 'disponivel',
                'urgencia': 'baixa',
                'endereco_retirada': 'Rua das Flores, 123',
                'cidade': 'São Paulo',
                'estado': 'SP',
            },
            {
                'doador': 'joao_santos',
                'titulo': 'Jogo de panelas 5 peças',
                'descricao': 'Jogo de panelas antiaderentes com 5 peças de tamanhos variados. Usado mas em bom estado de conservação. Todas as tampas incluídas.',
                'categoria': 'Utensílios',
                'quantidade': 1,
                'condicao': 'Usado em bom estado',
                'status': 'disponivel',
                'urgencia': 'media',
                'endereco_retirada': 'Av. Atlântica, 456',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
            },
        ]
        
        doacoes_count = 0
        for doacao_data in doacoes_data:
            doador = usuarios_criados[doacao_data['doador']]
            categoria = categorias_criadas[doacao_data['categoria']]
            
            # Verificar se já existe uma doação similar
            exists = Doacao.objects.filter(
                doador=doador,
                titulo=doacao_data['titulo']
            ).exists()
            
            if not exists:
                Doacao.objects.create(
                    doador=doador,
                    titulo=doacao_data['titulo'],
                    descricao=doacao_data['descricao'],
                    categoria=categoria,
                    quantidade=doacao_data['quantidade'],
                    condicao=doacao_data['condicao'],
                    status=doacao_data['status'],
                    urgencia=doacao_data['urgencia'],
                    endereco_retirada=doacao_data['endereco_retirada'],
                    cidade=doacao_data['cidade'],
                    estado=doacao_data['estado'],
                )
                doacoes_count += 1
                self.stdout.write(self.style.SUCCESS(f'   ✓ Doação "{doacao_data["titulo"]}" criada'))
            else:
                self.stdout.write(f'   - Doação "{doacao_data["titulo"]}" já existe')
        
        # 4. ATUALIZAR ESTATÍSTICAS DOS PERFIS
        self.stdout.write('\n4. Atualizando estatísticas dos perfis...')
        for username, user in usuarios_criados.items():
            perfil = user.perfil
            perfil.total_doacoes = Doacao.objects.filter(doador=user).count()
            perfil.save()
            self.stdout.write(f'   ✓ Perfil de "{username}" atualizado')
        
        # RESUMO
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✓ BANCO DE DADOS POPULADO COM SUCESSO!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'\n📊 Resumo:')
        self.stdout.write(f'   • Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'   • Usuários: {User.objects.count()}')
        self.stdout.write(f'   • Doações: {Doacao.objects.count()}')
        
        if doacoes_count > 0:
            self.stdout.write(self.style.WARNING(f'\n🔑 Credenciais dos usuários de exemplo:'))
            self.stdout.write(f'   Username: maria_silva, joao_santos, ana_costa, carlos_oliveira')
            self.stdout.write(f'   Senha: senha123 (para todos)')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Pronto para usar!\n'))
