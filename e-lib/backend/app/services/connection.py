from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        self.uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/simple-lib')
        self.client = None
        self.db = None
    
    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client.get_database()
            print("Conectado ao MongoDB com sucesso!")
            return self.db
        except Exception as e:
            print(f"Erro ao conectar com MongoDB: {e}")
            return None
    
    def get_collection(self, collection_name):
        if self.db is None:
            self.connect()
        return self.db[collection_name]

mongo = MongoDB()
