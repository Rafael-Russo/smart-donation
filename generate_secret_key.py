#!/usr/bin/env python
"""
Script para gerar uma nova SECRET_KEY do Django.
Útil ao configurar um novo ambiente ou ao comprometer a chave atual.

Uso:
    python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*70)
    print("Nova SECRET_KEY gerada com sucesso!")
    print("="*70)
    print(f"\n{secret_key}\n")
    print("="*70)
    print("Copie e cole no seu arquivo .env:")
    print(f"SECRET_KEY={secret_key}")
    print("="*70 + "\n")
