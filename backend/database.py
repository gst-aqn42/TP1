# C:\Projetos\TP1\backend\database.py

from pymongo import MongoClient
# Importamos a exceção correta para problemas de timeout/conexão no PyMongo V4+
from pymongo.errors import ServerSelectionTimeoutError 

# Variáveis de Configuração
# URL padrão para o MongoDB rodando localmente (seja direto ou via Docker)
MONGO_DETAILS = "mongodb://localhost:27017/"
DATABASE_NAME = "biblioteca_digital"

client = None
db = None

try:
    # 1. Inicializa o Cliente PyMongo
    # serverSelectionTimeoutMS=5000: Define um timeout de 5 segundos para não travar o servidor Uvicorn
    client = MongoClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)
    
    # 2. Seleciona o Banco de Dados
    db = client[DATABASE_NAME]

    # Verifica a conexão enviando um comando trivial ao servidor
    # Se o DB não estiver rodando, esta linha levantará um ServerSelectionTimeoutError
    client.admin.command('ping')
    print("Conexão bem-sucedida ao MongoDB!")

# Captura o erro específico de timeout, que indica que o DB não está acessível
except ServerSelectionTimeoutError as e:
    print(f"ERRO DE CONEXÃO: Não foi possível conectar ao MongoDB em {MONGO_DETAILS}. Certifique-se de que o MongoDB/Docker está rodando. Erro: {e}")
except Exception as e:
    # Captura outros erros de inicialização, como credenciais incorretas (se implementadas)
    print(f"Ocorreu um erro inesperado na conexão com o MongoDB: {e}")
    
# ----------------- Mapeamento e Exportação das Coleções -----------------

# CORREÇÃO FINAL (PyMongo V4+): Checamos explicitamente se o objeto 'db' foi preenchido.
if db is not None:
    # Os objetos de coleção que serão importados e usados no main.py (Task 4)
    event_collection = db.get_collection("events")
    edition_collection = db.get_collection("editions")
    article_collection = db.get_collection("articles")
    author_collection = db.get_collection("authors")
    subscription_collection = db.get_collection("subscriptions")
else:
    # Se a conexão falhar, define os objetos de coleção como None
    # Isso é usado no main.py para retornar 503 (Serviço Indisponível)
    event_collection = None
    edition_collection = None
    article_collection = None
    author_collection = None
    subscription_collection = None