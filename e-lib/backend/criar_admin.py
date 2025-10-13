#!/usr/bin/env python3
"""
Script para criar usuário admin no banco de dados
"""

from app.services.connection import mongo
from app.models.usuario import Usuario
import sys

def criar_admin():
    """Cria ou atualiza usuário admin"""
    try:
        db = mongo.db
        
        # Verificar se já existe
        admin_existente = Usuario.find_by_email('admin@admin.com')
        
        if admin_existente:
            print('ℹ️  Usuário admin já existe!')
            print(f'   Email: {admin_existente["email"]}')
            print(f'   Nome: {admin_existente["nome"]}')
            print(f'   Admin: {admin_existente.get("is_admin", False)}')
            
            # Atualizar para garantir que é admin
            db.usuarios.update_one(
                {'email': 'admin@admin.com'},
                {'$set': {'is_admin': True, 'senha': 'admin'}}
            )
            print('✅ Usuário atualizado para admin!')
        else:
            print('Criando usuário admin...')
            
            # Criar novo usuário admin
            admin = Usuario(
                email='admin@admin.com',
                nome='Administrador',
                is_admin=True,
                senha='admin'  # Em produção, isso seria hash
            )
            
            result = admin.save()
            
            if result:
                print('✅ Usuário admin criado com sucesso!')
            else:
                print('❌ Erro ao criar usuário admin')
                return False
        
        print('\n' + '='*60)
        print('📋 CREDENCIAIS DE LOGIN:')
        print('='*60)
        print('  Username: admin')
        print('  Senha: admin')
        print('='*60)
        
        return True
        
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print('='*60)
    print('🔧 Criando usuário administrador')
    print('='*60)
    print()
    
    if criar_admin():
        sys.exit(0)
    else:
        sys.exit(1)
