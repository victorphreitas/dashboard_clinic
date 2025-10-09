#!/usr/bin/env python3
"""
Script para gerar uma chave secreta segura para produção
"""

import secrets
import string

def generate_secret_key(length=50):
    """Gera uma chave secreta segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔐 GERADOR DE CHAVE SECRETA PARA PRODUÇÃO")
    print("=" * 50)
    
    # Gerar chave secreta
    secret_key = generate_secret_key(50)
    
    print(f"🔑 Chave Secreta Gerada:")
    print(f"   {secret_key}")
    print()
    print("📋 Como usar no Render.com:")
    print("1. Acesse o painel do Render.com")
    print("2. Vá em Environment Variables")
    print("3. Adicione a variável SECRET_KEY")
    print("4. Cole a chave gerada acima")
    print()
    print("⚠️  IMPORTANTE:")
    print("- Mantenha esta chave segura")
    print("- Não compartilhe publicamente")
    print("- Use apenas em produção")
    print()
    print("✅ Chave pronta para uso!")

if __name__ == "__main__":
    main()
