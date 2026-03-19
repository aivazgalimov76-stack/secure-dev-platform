from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flaskr.logger import setup_logging  
# Создаем объекты расширений
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Фабрика приложений Flask"""
    
    # Создаем экземпляр Flask
    app = Flask(__name__)
    
    # Загружаем конфигурацию
    app.config.from_object(config_class)
    
    # Инициализируем расширения
    db.init_app(app)
    login_manager.init_app(app)

    # настройка логирования
    setup_logging(app)
    
    # Настройка login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа'
    
    # Регистрируем blueprint'ы
    from flaskr.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from flaskr.blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    
    # Создаем таблицы базы данных
    with app.app_context():
        db.create_all()
    
    return app
