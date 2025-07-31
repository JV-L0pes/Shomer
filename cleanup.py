#!/usr/bin/env python3
"""
Script de Limpeza - Remove arquivos __pycache__ e .pyc
Este script remove todos os diretórios __pycache__ e arquivos .pyc do projeto
"""

import os
import shutil
import glob
from pathlib import Path


def cleanup_pycache():
    """
    Remove todos os diretórios __pycache__ e arquivos .pyc do projeto
    """
    print("🧹 Iniciando limpeza do projeto...")

    # Contador para estatísticas
    removed_dirs = 0
    removed_files = 0

    # Obter o diretório raiz do projeto
    project_root = Path(__file__).parent

    print(f"📁 Procurando em: {project_root}")

    # Remover diretórios __pycache__
    for pycache_dir in project_root.rglob("__pycache__"):
        try:
            if pycache_dir.is_dir():
                shutil.rmtree(pycache_dir)
                print(f"🗑️  Removido diretório: {pycache_dir}")
                removed_dirs += 1
        except Exception as e:
            print(f"❌ Erro ao remover {pycache_dir}: {e}")

    # Remover arquivos .pyc
    for pyc_file in project_root.rglob("*.pyc"):
        try:
            if pyc_file.is_file():
                pyc_file.unlink()
                print(f"🗑️  Removido arquivo: {pyc_file}")
                removed_files += 1
        except Exception as e:
            print(f"❌ Erro ao remover {pyc_file}: {e}")

    # Remover arquivos .pyo (se existirem)
    for pyo_file in project_root.rglob("*.pyo"):
        try:
            if pyo_file.is_file():
                pyo_file.unlink()
                print(f"🗑️  Removido arquivo: {pyo_file}")
                removed_files += 1
        except Exception as e:
            print(f"❌ Erro ao remover {pyo_file}: {e}")

    # Exibir estatísticas
    print("\n📊 Estatísticas da limpeza:")
    print(f"   📁 Diretórios __pycache__ removidos: {removed_dirs}")
    print(f"   📄 Arquivos .pyc/.pyo removidos: {removed_files}")
    print(f"   🎯 Total de itens removidos: {removed_dirs + removed_files}")

    if removed_dirs + removed_files == 0:
        print("✨ Projeto já está limpo! Nenhum arquivo cache encontrado.")
    else:
        print("✅ Limpeza concluída com sucesso!")


def main():
    """
    Função principal do script
    """
    print("=" * 50)
    print("🧹 SCRIPT DE LIMPEZA - REMOÇÃO DE CACHE PYTHON")
    print("=" * 50)

    # Confirmar com o usuário
    response = input("\n⚠️  Deseja continuar com a limpeza? (s/N): ").strip().lower()

    if response in ["s", "sim", "y", "yes"]:
        cleanup_pycache()
    else:
        print("❌ Operação cancelada pelo usuário.")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
