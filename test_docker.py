#!/usr/bin/env python3
"""
Script para testar o Docker localmente antes do deploy
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso!")
            return True
        else:
            print(f"❌ {description} - Erro!")
            print(f"   Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def main():
    print("🐳 TESTE DO DOCKER LOCAL")
    print("=" * 40)
    
    # Verificar se Docker está instalado
    if not run_command("docker --version", "Verificando Docker"):
        print("❌ Docker não está instalado!")
        print("   Instale o Docker Desktop: https://www.docker.com/products/docker-desktop")
        return False
    
    # Verificar se Dockerfile existe
    if not os.path.exists("Dockerfile"):
        print("❌ Dockerfile não encontrado!")
        return False
    
    # Build da imagem
    if not run_command("docker build -t prestige-clinic-dashboard .", "Construindo imagem Docker"):
        return False
    
    # Teste da aplicação
    print("🚀 Iniciando aplicação em container...")
    print("   Acesse: http://localhost:10000")
    print("   Pressione Ctrl+C para parar")
    print()
    
    try:
        # Executar container
        subprocess.run([
            "docker", "run", "-p", "10000:10000",
            "-e", "GOOGLE_CREDENTIALS_JSON={\"type\":\"test\"}",
            "-e", "SECRET_KEY=test-key",
            "prestige-clinic-dashboard"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário")
    
    print("✅ Teste do Docker concluído!")
    print()
    print("📋 Próximos passos:")
    print("1. Se o teste funcionou, faça commit das mudanças")
    print("2. Push para o repositório Git")
    print("3. Configure o deploy no Render.com")
    print("4. Configure as variáveis de ambiente")

if __name__ == "__main__":
    main()

