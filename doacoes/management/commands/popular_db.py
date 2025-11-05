from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from doacoes.models import (
    Categoria, Perfil, Doacao, PontoColeta, ItemEstoque, 
    SolicitacaoRetirada, PostComunidade, ComentarioPost
)
from django.utils import timezone
from datetime import timedelta


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
        
        # 4. ATUALIZAR ESTATÍSTICAS DOS PERFIS (DOAÇÕES LEGADAS)
        self.stdout.write('\n4. Atualizando estatísticas dos perfis (doações legadas)...')
        for username, user in usuarios_criados.items():
            perfil = user.perfil
            perfil.total_doacoes = Doacao.objects.filter(doador=user).count()
            perfil.save()
            self.stdout.write(f'   ✓ Perfil de "{username}" atualizado')
        
        # 5. CRIAR PONTOS DE COLETA
        self.stdout.write('\n5. Criando pontos de coleta...')
        pontos_data = [
            {
                'responsavel': 'maria_silva',
                'nome': 'Centro de Doações Zona Sul - SP',
                'descricao': 'Ponto de coleta localizado na zona sul de São Paulo. Recebemos roupas, alimentos não perecíveis, móveis pequenos e brinquedos. Funcionamos de segunda a sexta, das 9h às 18h.',
                'endereco': 'Rua das Flores, 123',
                'bairro': 'Vila Mariana',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'cep': '01234-567',
                'telefone': '(11) 98765-4321',
                'email': 'contato@centrodoacao.com',
                'horario_funcionamento': 'Segunda a Sexta: 9h às 18h | Sábado: 9h às 13h',
                'ativo': True,
            },
            {
                'responsavel': 'joao_santos',
                'nome': 'Ponto Solidário Copacabana',
                'descricao': 'Ponto de coleta comunitário em Copacabana. Priorizamos alimentos, produtos de higiene e roupas. Temos parceria com instituições locais para distribuição rápida.',
                'endereco': 'Av. Atlântica, 456',
                'bairro': 'Copacabana',
                'cidade': 'Rio de Janeiro',
                'estado': 'RJ',
                'cep': '22000-000',
                'telefone': '(21) 99876-5432',
                'email': 'pontosolidario@example.com',
                'horario_funcionamento': 'Todos os dias: 10h às 20h',
                'ativo': True,
            },
            {
                'responsavel': 'ana_costa',
                'nome': 'Espaço Doar - BH',
                'descricao': 'Espaço dedicado à coleta de livros, material escolar e eletrônicos. Fazemos triagem e destinamos para escolas e bibliotecas comunitárias. Aceitamos também móveis mediante agendamento.',
                'endereco': 'Rua da Liberdade, 789',
                'bairro': 'Savassi',
                'cidade': 'Belo Horizonte',
                'estado': 'MG',
                'cep': '30000-000',
                'telefone': '(31) 97654-3210',
                'email': 'espacodoar@example.com',
                'horario_funcionamento': 'Segunda a Sábado: 8h às 17h',
                'ativo': True,
            },
        ]
        
        pontos_criados = {}
        for ponto_data in pontos_data:
            responsavel = usuarios_criados[ponto_data['responsavel']]
            
            ponto, created = PontoColeta.objects.get_or_create(
                nome=ponto_data['nome'],
                defaults={
                    'responsavel': responsavel,
                    'descricao': ponto_data['descricao'],
                    'endereco': ponto_data['endereco'],
                    'bairro': ponto_data['bairro'],
                    'cidade': ponto_data['cidade'],
                    'estado': ponto_data['estado'],
                    'cep': ponto_data['cep'],
                    'telefone': ponto_data['telefone'],
                    'email': ponto_data['email'],
                    'horario_funcionamento': ponto_data['horario_funcionamento'],
                    'ativo': ponto_data['ativo'],
                }
            )
            pontos_criados[ponto_data['nome']] = ponto
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Ponto "{ponto.nome}" criado'))
            else:
                self.stdout.write(f'   - Ponto "{ponto.nome}" já existe')
        
        # 6. CRIAR ITENS DE ESTOQUE
        self.stdout.write('\n6. Criando itens de estoque...')
        itens_data = [
            # Centro de Doações Zona Sul - SP
            {
                'ponto': 'Centro de Doações Zona Sul - SP',
                'doador': 'maria_silva',
                'categoria': 'Roupas',
                'titulo': 'Roupas Femininas (Tamanhos P, M, G)',
                'descricao': 'Lote de roupas femininas variadas incluindo blusas, calças e vestidos. Todas as peças estão limpas e em bom estado.',
                'quantidade_disponivel': 45,
                'condicao': 'usado_bom',
                'urgencia': 'media',
            },
            {
                'ponto': 'Centro de Doações Zona Sul - SP',
                'doador': 'maria_silva',
                'categoria': 'Alimentos',
                'titulo': 'Cestas Básicas Completas',
                'descricao': 'Cestas básicas contendo arroz, feijão, óleo, macarrão, açúcar e café. Todos os produtos dentro da validade.',
                'quantidade_disponivel': 12,
                'condicao': 'novo',
                'urgencia': 'urgente',
            },
            {
                'ponto': 'Centro de Doações Zona Sul - SP',
                'doador': 'maria_silva',
                'categoria': 'Brinquedos',
                'titulo': 'Brinquedos Diversos (0-10 anos)',
                'descricao': 'Variedade de brinquedos para diferentes idades: carrinhos, bonecas, jogos educativos e pelúcias.',
                'quantidade_disponivel': 30,
                'condicao': 'usado_otimo',
                'urgencia': 'baixa',
            },
            # Ponto Solidário Copacabana
            {
                'ponto': 'Ponto Solidário Copacabana',
                'doador': 'joao_santos',
                'categoria': 'Alimentos',
                'titulo': 'Arroz (pacotes de 5kg)',
                'descricao': 'Pacotes de arroz tipo 1, lacrados e dentro da validade. Ideal para famílias.',
                'quantidade_disponivel': 25,
                'condicao': 'novo',
                'urgencia': 'urgente',
            },
            {
                'ponto': 'Ponto Solidário Copacabana',
                'doador': 'joao_santos',
                'categoria': 'Alimentos',
                'titulo': 'Feijão (pacotes de 1kg)',
                'descricao': 'Pacotes de feijão carioca, todos lacrados e dentro da validade.',
                'quantidade_disponivel': 30,
                'condicao': 'novo',
                'urgencia': 'alta',
            },
            {
                'ponto': 'Ponto Solidário Copacabana',
                'doador': 'joao_santos',
                'categoria': 'Roupas',
                'titulo': 'Roupas Infantis (2-8 anos)',
                'descricao': 'Coleção de roupas infantis para meninos e meninas. Inclui camisetas, shorts, calças e vestidos.',
                'quantidade_disponivel': 60,
                'condicao': 'usado_bom',
                'urgencia': 'media',
            },
            {
                'ponto': 'Ponto Solidário Copacabana',
                'doador': 'joao_santos',
                'categoria': 'Utensílios',
                'titulo': 'Pratos e Talheres (kits completos)',
                'descricao': 'Kits contendo pratos, copos, talheres. Alguns novos na embalagem, outros usados em bom estado.',
                'quantidade_disponivel': 15,
                'condicao': 'usado_bom',
                'urgencia': 'baixa',
            },
            # Espaço Doar - BH
            {
                'ponto': 'Espaço Doar - BH',
                'doador': 'ana_costa',
                'categoria': 'Livros',
                'titulo': 'Livros Didáticos Ensino Fundamental',
                'descricao': 'Livros didáticos de matemática, português, ciências e história para ensino fundamental completo.',
                'quantidade_disponivel': 80,
                'condicao': 'usado_otimo',
                'urgencia': 'alta',
            },
            {
                'ponto': 'Espaço Doar - BH',
                'doador': 'ana_costa',
                'categoria': 'Livros',
                'titulo': 'Literatura Infantil e Juvenil',
                'descricao': 'Coleção variada de livros de literatura para crianças e adolescentes. Clássicos e contemporâneos.',
                'quantidade_disponivel': 120,
                'condicao': 'usado_bom',
                'urgencia': 'media',
            },
            {
                'ponto': 'Espaço Doar - BH',
                'doador': 'ana_costa',
                'categoria': 'Eletrônicos',
                'titulo': 'Notebooks e Computadores',
                'descricao': 'Equipamentos de informática recondicionados. Testados e funcionando, ideais para estudo e trabalho.',
                'quantidade_disponivel': 8,
                'condicao': 'usado_bom',
                'urgencia': 'urgente',
            },
            {
                'ponto': 'Espaço Doar - BH',
                'doador': 'ana_costa',
                'categoria': 'Móveis',
                'titulo': 'Cadeiras e Mesas de Estudo',
                'descricao': 'Mobiliário para estudo: cadeiras, mesas e estantes. Em bom estado de conservação.',
                'quantidade_disponivel': 10,
                'condicao': 'usado_bom',
                'urgencia': 'media',
            },
        ]
        
        itens_criados = []
        for item_data in itens_data:
            ponto = pontos_criados[item_data['ponto']]
            doador = usuarios_criados[item_data['doador']]
            categoria = categorias_criadas[item_data['categoria']]
            
            item, created = ItemEstoque.objects.get_or_create(
                ponto_coleta=ponto,
                titulo=item_data['titulo'],
                defaults={
                    'doador': doador,
                    'categoria': categoria,
                    'descricao': item_data['descricao'],
                    'quantidade': item_data['quantidade_disponivel'],
                    'quantidade_disponivel': item_data['quantidade_disponivel'],
                    'condicao': item_data['condicao'],
                    'urgencia': item_data['urgencia'],
                }
            )
            itens_criados.append(item)
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Item "{item.titulo}" criado no ponto "{ponto.nome}"'))
            else:
                self.stdout.write(f'   - Item "{item.titulo}" já existe')
        
        # 7. CRIAR SOLICITAÇÕES DE RETIRADA
        self.stdout.write('\n7. Criando solicitações de retirada...')
        
        # Criar um usuário receptor adicional se não existir
        receptor_user, created = User.objects.get_or_create(
            username='pedro_receptor',
            defaults={
                'email': 'pedro@example.com',
                'first_name': 'Pedro',
                'last_name': 'Mendes',
            }
        )
        if created:
            receptor_user.set_password('senha123')
            receptor_user.save()
            Perfil.objects.create(
                usuario=receptor_user,
                tipo='receptor',
                telefone='(51) 95432-1098',
                cidade='Porto Alegre',
                estado='RS',
                endereco='Rua da Praia, 555',
                cep='90000-000'
            )
            self.stdout.write(self.style.SUCCESS(f'   ✓ Usuário receptor "pedro_receptor" criado'))
        
        solicitacoes_data = [
            {
                'solicitante': receptor_user,
                'item': 2,  # Cestas Básicas
                'quantidade_solicitada': 3,
                'observacao_solicitante': 'Precisamos de cestas básicas para 3 famílias atendidas pela nossa instituição. Todas estão em situação de vulnerabilidade.',
                'status': 'aprovada',
            },
            {
                'solicitante': usuarios_criados['carlos_oliveira'],
                'item': 4,  # Arroz
                'quantidade_solicitada': 5,
                'observacao_solicitante': 'Representando a Associação de Moradores do bairro, solicitamos arroz para distribuição entre 5 famílias carentes.',
                'status': 'aprovada',
            },
            {
                'solicitante': receptor_user,
                'item': 8,  # Livros Didáticos
                'quantidade_solicitada': 20,
                'observacao_solicitante': 'Somos uma biblioteca comunitária e precisamos de livros didáticos para nosso acervo. Atendemos mais de 100 crianças.',
                'status': 'pendente',
            },
            {
                'solicitante': usuarios_criados['carlos_oliveira'],
                'item': 10,  # Notebooks
                'quantidade_solicitada': 2,
                'observacao_solicitante': 'Precisamos de computadores para nossa sala de informática comunitária. Vamos oferecer cursos gratuitos.',
                'status': 'pendente',
            },
            {
                'solicitante': receptor_user,
                'item': 1,  # Roupas Femininas
                'quantidade_solicitada': 10,
                'observacao_solicitante': 'Atendemos mulheres em situação de vulnerabilidade. Precisamos de roupas para distribuição.',
                'status': 'recusada',
                'observacao_responsavel': 'Infelizmente não temos essa quantidade disponível no momento. Sugerimos solicitar uma quantidade menor.',
            },
            {
                'solicitante': usuarios_criados['carlos_oliveira'],
                'item': 7,  # Pratos e Talheres
                'quantidade_solicitada': 5,
                'observacao_solicitante': 'Vamos montar uma cozinha comunitária e precisamos de utensílios básicos.',
                'status': 'concluida',
                'data_conclusao': timezone.now() - timedelta(days=5),
            },
        ]
        
        for sol_data in solicitacoes_data:
            item = itens_criados[sol_data['item'] - 1]
            
            # Verificar se já existe
            exists = SolicitacaoRetirada.objects.filter(
                solicitante=sol_data['solicitante'],
                item=item,
                quantidade_solicitada=sol_data['quantidade_solicitada']
            ).exists()
            
            if not exists:
                solicitacao = SolicitacaoRetirada.objects.create(
                    solicitante=sol_data['solicitante'],
                    item=item,
                    quantidade_solicitada=sol_data['quantidade_solicitada'],
                    observacao_solicitante=sol_data['observacao_solicitante'],
                    status=sol_data['status'],
                )
                
                # Atualizar campos adicionais baseados no status
                if 'data_conclusao' in sol_data:
                    solicitacao.data_conclusao = sol_data['data_conclusao']
                if 'observacao_responsavel' in sol_data:
                    solicitacao.observacao_responsavel = sol_data['observacao_responsavel']
                    solicitacao.data_resposta = timezone.now()
                solicitacao.save()
                
                # Atualizar estoque se aprovada ou concluída
                if sol_data['status'] in ['aprovada', 'concluida']:
                    if item.quantidade_disponivel >= sol_data['quantidade_solicitada']:
                        item.quantidade_disponivel -= sol_data['quantidade_solicitada']
                        if sol_data['status'] == 'aprovada':
                            item.status = 'reservado'
                        item.save()
                
                self.stdout.write(self.style.SUCCESS(
                    f'   ✓ Solicitação de "{item.titulo}" por "{sol_data["solicitante"].username}" criada ({sol_data["status"]})'
                ))
            else:
                self.stdout.write(f'   - Solicitação já existe')
        
        # 8. CRIAR POSTS DA COMUNIDADE
        self.stdout.write('\n8. Criando posts da comunidade...')
        posts_data = [
            {
                'autor': 'maria_silva',
                'ponto_coleta': 'Centro de Doações Zona Sul - SP',
                'titulo': 'Campanha de Inverno 2025 - Precisamos de Agasalhos!',
                'conteudo': 'Estamos iniciando nossa campanha de inverno e precisamos urgentemente de agasalhos, cobertores e roupas de frio. Se você tem peças em bom estado que não usa mais, doe para quem precisa! Todas as doações serão triadas e distribuídas para famílias carentes da região.\n\nAceitamos:\n- Casacos e jaquetas\n- Cobertores e mantas\n- Meias e luvas\n- Cachecóis e toucas\n\nVenha nos visitar de segunda a sexta, das 9h às 18h!',
                'fixado': True,
            },
            {
                'autor': 'joao_santos',
                'ponto_coleta': 'Ponto Solidário Copacabana',
                'titulo': 'Ação Solidária de Natal - Como Participar',
                'conteudo': 'Nosso ponto está organizando uma grande ação de Natal para levar alegria a 200 crianças carentes da comunidade!\n\nComo você pode ajudar:\n1. Doando brinquedos novos ou usados em bom estado\n2. Doando alimentos para cestas de Natal\n3. Sendo voluntário na triagem e embalagem\n4. Divulgando nossa campanha\n\nPrazo: até 15 de dezembro\nEntrega dos presentes: 23 de dezembro\n\nContamos com você! 🎄',
                'fixado': True,
            },
            {
                'autor': 'ana_costa',
                'ponto_coleta': 'Espaço Doar - BH',
                'titulo': 'Novo Projeto: Biblioteca Comunitária',
                'conteudo': 'Estamos muito felizes em anunciar nosso novo projeto: a Biblioteca Comunitária do Espaço Doar!\n\nGraças às doações de livros que recebemos, conseguimos criar um acervo com mais de 500 títulos. A biblioteca estará aberta para toda a comunidade, gratuitamente.\n\nPrecisamos ainda de:\n- Mais livros (todos os gêneros)\n- Estantes e prateleiras\n- Mesas e cadeiras para área de leitura\n- Voluntários para catalogação\n\nInauguração prevista para março de 2025!',
                'fixado': False,
            },
            {
                'autor': 'maria_silva',
                'ponto_coleta': 'Centro de Doações Zona Sul - SP',
                'titulo': 'Dicas de Como Preparar suas Doações',
                'conteudo': 'Para facilitar nosso trabalho e garantir que suas doações cheguem em perfeito estado aos beneficiários, compartilhamos algumas dicas:\n\n**Roupas:**\n- Lave antes de doar\n- Separe por tipo e tamanho\n- Embale em sacos plásticos limpos\n\n**Alimentos:**\n- Verifique a validade\n- Prefira alimentos não perecíveis\n- Mantenha as embalagens lacradas\n\n**Móveis e Eletrônicos:**\n- Limpe antes de doar\n- Teste se está funcionando\n- Informe se há algum defeito\n\nObrigada pela colaboração! ❤️',
                'fixado': False,
            },
            {
                'autor': 'joao_santos',
                'ponto_coleta': 'Ponto Solidário Copacabana',
                'titulo': 'Agradecimento: 1000 Famílias Atendidas!',
                'conteudo': 'É com muita alegria que compartilhamos com vocês essa conquista: já atendemos mais de 1000 famílias desde a inauguração do nosso ponto!\n\nIsso só foi possível graças à generosidade de cada doador e ao trabalho incansável de nossos voluntários.\n\nQue venham mais 1000 famílias ajudadas! Juntos somos mais fortes! 💪\n\n#Gratidão #SolidariedadeSempreFoi necessária',
                'fixado': False,
            },
        ]
        
        posts_criados = []
        for post_data in posts_data:
            autor = usuarios_criados[post_data['autor']]
            ponto = pontos_criados[post_data['ponto_coleta']]
            
            post, created = PostComunidade.objects.get_or_create(
                titulo=post_data['titulo'],
                defaults={
                    'autor': autor,
                    'ponto_coleta': ponto,
                    'conteudo': post_data['conteudo'],
                    'fixado': post_data['fixado'],
                }
            )
            posts_criados.append(post)
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Post "{post.titulo}" criado'))
            else:
                self.stdout.write(f'   - Post "{post.titulo}" já existe')
        
        # 9. CRIAR COMENTÁRIOS NOS POSTS
        self.stdout.write('\n9. Criando comentários nos posts...')
        comentarios_data = [
            # Comentários no post "Campanha de Inverno"
            {
                'post': 0,
                'autor': 'joao_santos',
                'texto': 'Excelente iniciativa! Vou separar alguns cobertores aqui e levar pessoalmente. Quando posso passar aí?',
                'resposta_a': None,
            },
            {
                'post': 0,
                'autor': 'maria_silva',
                'texto': 'Que legal, João! Você pode vir qualquer dia no nosso horário de funcionamento. Obrigada! 😊',
                'resposta_a': 0,  # Resposta ao comentário anterior
            },
            {
                'post': 0,
                'autor': 'ana_costa',
                'texto': 'Aqui em BH também estamos fazendo campanha de inverno. Se alguém tiver doações mas morar longe do ponto da Maria, pode trazer no nosso Espaço Doar também!',
                'resposta_a': None,
            },
            # Comentários no post "Ação Solidária de Natal"
            {
                'post': 1,
                'autor': 'carlos_oliveira',
                'texto': 'Como faço para me voluntariar? Tenho disponibilidade aos sábados.',
                'resposta_a': None,
            },
            {
                'post': 1,
                'autor': 'joao_santos',
                'texto': 'Carlos, que ótimo! Entre em contato pelo telefone (21) 99876-5432 ou passe aqui no ponto para conversarmos. Precisamos muito de voluntários!',
                'resposta_a': 3,
            },
            # Comentários no post "Biblioteca Comunitária"
            {
                'post': 2,
                'autor': 'maria_silva',
                'texto': 'Parabéns, Ana! Projeto maravilhoso. Incentivo à leitura é fundamental. Vou divulgar aqui em SP também!',
                'resposta_a': None,
            },
            {
                'post': 2,
                'autor': 'pedro_receptor',
                'texto': 'Tenho uma coleção de livros infantis que posso doar. São mais de 50 livros. Como faço?',
                'resposta_a': None,
            },
            {
                'post': 2,
                'autor': 'ana_costa',
                'texto': 'Pedro, seria incrível! Entre em contato pelo email espacodoar@example.com ou telefone (31) 97654-3210 para agendarmos a retirada. Obrigada! 📚',
                'resposta_a': 6,
            },
            # Comentários no post "Dicas de Como Preparar"
            {
                'post': 3,
                'autor': 'carlos_oliveira',
                'texto': 'Dicas muito úteis! Não sabia que era importante lavar as roupas antes. Vou fazer isso nas próximas doações.',
                'resposta_a': None,
            },
            # Comentários no post "Agradecimento"
            {
                'post': 4,
                'autor': 'ana_costa',
                'texto': 'Parabéns pela marca, João! Vocês são inspiração para todos nós. Continue esse trabalho lindo! ❤️',
                'resposta_a': None,
            },
        ]
        
        comentarios_criados = []
        for coment_data in comentarios_data:
            post = posts_criados[coment_data['post']]
            
            # Determinar o autor
            if coment_data['autor'] == 'pedro_receptor':
                autor = receptor_user
            else:
                autor = usuarios_criados[coment_data['autor']]
            
            # Determinar se é resposta a outro comentário
            resposta_a = None
            if coment_data['resposta_a'] is not None:
                resposta_a = comentarios_criados[coment_data['resposta_a']]
            
            comentario, created = ComentarioPost.objects.get_or_create(
                post=post,
                autor=autor,
                texto=coment_data['texto'],
                defaults={
                    'resposta_a': resposta_a,
                }
            )
            comentarios_criados.append(comentario)
            if created:
                tipo = "resposta" if resposta_a else "comentário"
                self.stdout.write(self.style.SUCCESS(f'   ✓ {tipo.capitalize()} de "{autor.username}" criado'))
            else:
                self.stdout.write(f'   - Comentário já existe')
        
        # 10. ATUALIZAR ESTATÍSTICAS FINAIS
        self.stdout.write('\n10. Atualizando estatísticas finais...')
        for username, user in usuarios_criados.items():
            perfil = user.perfil
            perfil.total_doacoes = Doacao.objects.filter(doador=user).count()
            perfil.save()
        
        # RESUMO FINAL
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ BANCO DE DADOS POPULADO COM SUCESSO!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\n📊 Resumo Completo:')
        self.stdout.write(f'   • Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'   • Usuários: {User.objects.count()}')
        self.stdout.write(f'   • Perfis: {Perfil.objects.count()}')
        self.stdout.write(f'   • Doações (legado): {Doacao.objects.count()}')
        self.stdout.write(f'   • Pontos de Coleta: {PontoColeta.objects.count()}')
        self.stdout.write(f'   • Itens no Estoque: {ItemEstoque.objects.count()}')
        self.stdout.write(f'   • Solicitações de Retirada: {SolicitacaoRetirada.objects.count()}')
        self.stdout.write(f'   • Posts da Comunidade: {PostComunidade.objects.count()}')
        self.stdout.write(f'   • Comentários: {ComentarioPost.objects.count()}')
        
        self.stdout.write(self.style.WARNING(f'\n🔑 Credenciais dos usuários de exemplo:'))
        self.stdout.write(f'   Doadores/Gestores: maria_silva, joao_santos, ana_costa')
        self.stdout.write(f'   Receptores: carlos_oliveira, pedro_receptor')
        self.stdout.write(f'   Senha para todos: senha123')
        
        self.stdout.write(self.style.WARNING(f'\n📍 Pontos de Coleta Criados:'))
        for ponto in PontoColeta.objects.all():
            self.stdout.write(f'   • {ponto.nome} ({ponto.cidade}/{ponto.estado})')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sistema pronto para uso completo!\n'))
