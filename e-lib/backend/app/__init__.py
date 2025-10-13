from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-muito-longa-aqui-123')
    app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/simple-lib')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # Criar diretório de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Importar e configurar database
    try:
        from app.services.database import mongo
        mongo.connect()
        print("Database configurado com sucesso!")
    except ImportError as e:
        print(f"Erro ao importar database: {e}")
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.eventos import eventos_bp
    from app.routes.edicoes import edicoes_bp
    from app.routes.artigos import artigos_bp
    from app.routes.public import public_bp
    from app.routes.notificacoes import notificacoes_bp
    from app.routes.batch_upload import batch_upload_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(eventos_bp, url_prefix='/api/eventos')
    app.register_blueprint(edicoes_bp, url_prefix='/api/edicoes')
    app.register_blueprint(artigos_bp, url_prefix='/api/artigos')
    app.register_blueprint(public_bp, url_prefix='/api/public')
    app.register_blueprint(notificacoes_bp, url_prefix='/api/notificacoes')
    app.register_blueprint(batch_upload_bp, url_prefix='/api/batch')
    
    # Rota raiz
    @app.route('/')
    def home():
        return {
            "message": "API da Biblioteca Digital de Artigos",
            "status": "online",
            "version": "1.0.0"
        }
    
    @app.route('/health')
    def health():
        return {"status": "healthy"}
    
    return app
