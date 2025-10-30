"""
Script para exportar e importar clínicas (clientes) entre ambientes.

Uso:
  - Exportar:  python seed_clients.py --export --file data/clinics_seed.json
  - Importar:  python seed_clients.py --import --file data/clinics_seed.json [--default-password "Senha@123"]

Notas:
  - Exporta apenas clientes ativos e não-admin.
  - Na importação, se o email já existir, atualiza campos principais (não muda senha por padrão).
  - Se não existir, cria o cliente com a senha padrão fornecida via --default-password (ou variável DEFAULT_CLIENT_PASSWORD).
"""

import argparse
import json
import os
from typing import List, Dict
from datetime import datetime

from database import cliente_crud, db_manager
from models import Cliente

DEFAULT_FILE = os.path.join('data', 'clinics_seed.json')
DEFAULT_PASSWORD = os.getenv('DEFAULT_CLIENT_PASSWORD', 'Senha@123')


def serialize_cliente(c: Cliente) -> Dict:
    return {
        "nome": c.nome,
        "email": c.email,
        "cnpj": c.cnpj,
        "nome_da_clinica": c.nome_da_clinica,
        "telefone": c.telefone,
        "endereco": c.endereco,
        "link_empresa": c.link_empresa,
        "is_admin": bool(c.is_admin),
        "ativo": bool(c.ativo),
    }


def export_clients(file_path: str) -> None:
    clientes = cliente_crud.get_all_clientes()
    export_list = [serialize_cliente(c) for c in clientes if not c.is_admin and c.ativo]

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(
            {
                "exported_at": datetime.utcnow().isoformat() + "Z",
                "count": len(export_list),
                "clientes": export_list,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"✅ Exportados {len(export_list)} clientes para {file_path}")


def import_clients(file_path: str, default_password: str) -> None:
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)

    clientes_data: List[Dict] = payload.get('clientes', []) if isinstance(payload, dict) else payload

    created, updated, skipped = 0, 0, 0

    # Precisamos de uma sessão direta para checar existência por email rapidamente
    session = db_manager.get_session()
    try:
        existing_by_email = {c.email: c for c in session.query(Cliente).all()}
    finally:
        db_manager.close_session(session)

    for data in clientes_data:
        email = data.get('email')
        if not email:
            skipped += 1
            continue

        exists = existing_by_email.get(email)
        if exists:
            # Atualiza campos principais sem alterar senha
            ok = cliente_crud.update_cliente(
                exists.id,
                nome=data.get('nome'),
                cnpj=data.get('cnpj'),
                nome_da_clinica=data.get('nome_da_clinica'),
                telefone=data.get('telefone'),
                endereco=data.get('endereco'),
                link_empresa=data.get('link_empresa'),
                is_admin=bool(data.get('is_admin', False)),
            )
            if ok:
                updated += 1
            else:
                skipped += 1
        else:
            created_obj = cliente_crud.create_cliente(
                nome=data.get('nome') or data.get('nome_da_clinica') or 'Cliente',
                email=email,
                senha=default_password,
                cnpj=data.get('cnpj'),
                nome_da_clinica=data.get('nome_da_clinica') or data.get('nome') or '',
                telefone=data.get('telefone'),
                endereco=data.get('endereco'),
                link_empresa=data.get('link_empresa'),
                is_admin=bool(data.get('is_admin', False)),
            )
            if created_obj:
                created += 1
            else:
                skipped += 1

    print(f"✅ Importação concluída: {created} criados, {updated} atualizados, {skipped} ignorados")
    if created > 0:
        print("ℹ️ Senha padrão utilizada para novos clientes:")
        print(f"   {default_password}  (altere depois em produção)")


def main():
    parser = argparse.ArgumentParser(description='Exportar/Importar clínicas (clientes) do dashboard')
    parser.add_argument('--export', action='store_true', help='Exporta clientes ativos e não-admin para JSON')
    parser.add_argument('--import', dest='do_import', action='store_true', help='Importa clientes a partir de JSON')
    parser.add_argument('--file', type=str, default=DEFAULT_FILE, help='Caminho do arquivo JSON')
    parser.add_argument('--default-password', type=str, default=DEFAULT_PASSWORD, help='Senha padrão para novos clientes')

    args = parser.parse_args()

    if args.export and args.do_import:
        print('❌ Use apenas uma opção: --export OU --import')
        return

    if not args.export and not args.do_import:
        print('❌ Informe uma ação: --export ou --import')
        return

    if args.export:
        export_clients(args.file)
    else:
        import_clients(args.file, args.default_password)


if __name__ == '__main__':
    main()
