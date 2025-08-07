import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://shomer_user:shomer_pass_123@localhost:27017/shomerdb?authSource=shomerdb")

# Lazy connection - só conecta quando necessário
_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        try:
            _client = AsyncIOMotorClient(MONGODB_URI)
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            # Fallback para URI simples
            _client = AsyncIOMotorClient("mongodb://localhost:27017/shomerdb")
    return _client

def get_db():
    global _db
    if _db is None:
        _db = get_client().get_default_database()
    return _db

def get_users_collection():
    return get_db()["users"]

def get_logs_collection():
    return get_db()["logs"]

# Para compatibilidade com código existente - removido para evitar conexão durante importação
