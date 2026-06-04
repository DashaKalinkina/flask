import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()         
bcrypt = Bcrypt()       
login_manager = LoginManager()  

# путь к папке
def get_base_path():

    if getattr(sys, 'frozen', False):

        return sys._MEIPASS
    else:
 
        return os.path.dirname(os.path.abspath(__file__))

# путь к файлу бд
def get_db_path():
   
    if getattr(sys, 'frozen', False):
       
        user_dir = os.path.expanduser('~')
        db_dir = os.path.join(user_dir, 'ConferencesRu_data')
    else:
       
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    

    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'conferences.db')

# инициализ. всех компонентов
def create_app():
  
    app = Flask(__name__, 
                template_folder=os.path.join(get_base_path(), 'templates'),
                static_folder=os.path.join(get_base_path(), 'static'))
    
    app.config['SECRET_KEY'] = 'your-secret-key-here'  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{get_db_path()}' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # настройка LoginManager
    login_manager.login_view = 'auth.login'  
    login_manager.login_message = 'Пожалуйста, войдите в систему' 
    
 
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Загружает пользователя по ID из сессии"""
        return User.query.get(int(user_id))
    
    # регистрация модулей приложения(blueprint)
    from .auth import auth_bp      
    from .views import views_bp    
    from .admin import admin_bp    
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(views_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
    
    # создание таблиц
    with app.app_context():
        db.create_all()
        
        # создание админа, если нет
        admin = User.query.filter_by(login='Admin26').first()
        if not admin:
            admin = User(
                login='Admin26',
                fullname='Администратор',
                phone='+70000000000',
                email='admin@conferences.ru',
                role='admin'  # Роль определяет права доступа
            )
            admin.set_password('Demo20')  # Устанавливаем хэшированный пароль
            db.session.add(admin)
            db.session.commit()
    
    return app