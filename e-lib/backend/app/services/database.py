# Este arquivo importa e exporta o objeto mongo de connection.py
# Permite manter a compatibilidade com imports existentes
from app.services.connection import mongo

__all__ = ['mongo']
