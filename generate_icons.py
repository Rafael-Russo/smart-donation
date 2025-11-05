"""
Script para gerar ícones PWA em múltiplos tamanhos
Requer: pip install Pillow

Como usar:
1. Coloque uma imagem quadrada (512x512 ou maior) chamada 'icon_base.png' na raiz do projeto
2. Execute: python generate_icons.py
3. Os ícones serão gerados na pasta static/icons/
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Erro: Pillow não está instalado!")
    print("📦 Instale com: pip install Pillow")
    exit(1)


# Tamanhos de ícones necessários para PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Cores do tema Smart Donation
PRIMARY_COLOR = (46, 125, 50)  # Verde #2E7D32
BACKGROUND_COLOR = (255, 255, 255)  # Branco


def create_icon_folder():
    """Cria a pasta de ícones se não existir"""
    icons_path = Path('static/icons')
    icons_path.mkdir(parents=True, exist_ok=True)
    return icons_path


def create_simple_icon(size, icons_path):
    """
    Cria um ícone simples com as iniciais SD (Smart Donation)
    """
    # Criar imagem com fundo verde
    img = Image.new('RGB', (size, size), PRIMARY_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Adicionar círculo branco no centro
    margin = size // 8
    circle_bbox = [margin, margin, size - margin, size - margin]
    draw.ellipse(circle_bbox, fill=BACKGROUND_COLOR)
    
    # Adicionar texto "SD"
    try:
        # Tenta usar uma fonte do sistema
        font_size = size // 3
        try:
            # Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                # Linux
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                # Fallback para fonte padrão
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    text = "SD"
    
    # Centralizar texto
    # Para fontes antigas do PIL que não têm textbbox
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback para versões antigas do Pillow
        text_width, text_height = draw.textsize(text, font=font)
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - (size // 20)  # Ajuste para centralizar melhor
    
    draw.text((x, y), text, fill=PRIMARY_COLOR, font=font)
    
    return img


def generate_from_base_image(base_image_path, icons_path):
    """
    Gera ícones a partir de uma imagem base fornecida pelo usuário
    """
    try:
        base_img = Image.open(base_image_path)
        print(f"✅ Imagem base carregada: {base_image_path}")
        print(f"   Tamanho original: {base_img.size}")
        
        # Converter para RGB se necessário
        if base_img.mode != 'RGB':
            base_img = base_img.convert('RGB')
        
        # Garantir que é quadrada
        width, height = base_img.size
        if width != height:
            # Crop para quadrado (centro)
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            base_img = base_img.crop((left, top, left + size, top + size))
            print(f"   ⚠️  Imagem ajustada para quadrado: {size}x{size}")
        
        # Gerar ícones em todos os tamanhos
        for size in ICON_SIZES:
            resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
            output_path = icons_path / f"icon-{size}x{size}.png"
            resized.save(output_path, 'PNG', optimize=True)
            print(f"   ✅ Gerado: icon-{size}x{size}.png")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {base_image_path}")
        return False
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        return False


def generate_simple_icons(icons_path):
    """
    Gera ícones simples com as iniciais SD
    """
    print("🎨 Gerando ícones simples com iniciais 'SD'...")
    
    for size in ICON_SIZES:
        img = create_simple_icon(size, icons_path)
        output_path = icons_path / f"icon-{size}x{size}.png"
        img.save(output_path, 'PNG', optimize=True)
        print(f"   ✅ Gerado: icon-{size}x{size}.png")
    
    return True


def generate_favicon(icons_path):
    """
    Gera favicon.ico a partir do ícone 192x192
    """
    try:
        icon_192 = Image.open(icons_path / "icon-192x192.png")
        # Redimensionar para tamanhos comuns de favicon
        favicon_sizes = [(16, 16), (32, 32), (48, 48)]
        favicon_images = [icon_192.resize(size, Image.Resampling.LANCZOS) for size in favicon_sizes]
        
        # Salvar como .ico multi-size
        favicon_path = Path('static') / 'favicon.ico'
        favicon_images[0].save(
            favicon_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in favicon_images]
        )
        print(f"✅ Favicon gerado: favicon.ico")
        return True
    except Exception as e:
        print(f"⚠️  Erro ao gerar favicon: {e}")
        return False


def main():
    """Função principal"""
    print("=" * 60)
    print("🚀 Smart Donation - Gerador de Ícones PWA")
    print("=" * 60)
    print()
    
    # Criar pasta de ícones
    icons_path = create_icon_folder()
    print(f"📁 Pasta de ícones: {icons_path.absolute()}")
    print()
    
    # Verificar se existe imagem base
    base_image_options = ['icon_base.png', 'icon_base.jpg', 'logo.png', 'logo.jpg']
    base_image_path = None
    
    for option in base_image_options:
        if os.path.exists(option):
            base_image_path = option
            break
    
    if base_image_path:
        print(f"🖼️  Imagem base encontrada: {base_image_path}")
        print()
        success = generate_from_base_image(base_image_path, icons_path)
    else:
        print("⚠️  Nenhuma imagem base encontrada (icon_base.png, logo.png, etc.)")
        print("   Gerando ícones simples com iniciais 'SD'...")
        print()
        success = generate_simple_icons(icons_path)
    
    if success:
        # Tentar gerar favicon
        print()
        generate_favicon(icons_path)
        
        print()
        print("=" * 60)
        print("✅ ÍCONES GERADOS COM SUCESSO!")
        print("=" * 60)
        print()
        print("📋 Próximos passos:")
        print("   1. Verifique os ícones em: static/icons/")
        print("   2. Execute: python manage.py collectstatic")
        print("   3. Teste a PWA: python manage.py runserver")
        print("   4. Abra o Chrome DevTools → Application → Manifest")
        print()
        print("💡 Dica: Para ícones personalizados, coloque uma imagem")
        print("   quadrada (512x512 ou maior) como 'icon_base.png'")
        print("   na raiz do projeto e execute novamente este script.")
        print()
    else:
        print()
        print("❌ Erro ao gerar ícones!")
        print("   Verifique as mensagens de erro acima.")
        print()


if __name__ == "__main__":
    main()
