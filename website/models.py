from . import db, bcrypt
from flask_login import UserMixin

#таблица с пользователями
class User(db.Model, UserMixin):

    __tablename__ = 'user'
    
    #поля таблицы
    id = db.Column(db.Integer, primary_key=True)           
    login = db.Column(db.String(80), unique=True, nullable=False)   
    password = db.Column(db.String(200), nullable=False)   
    fullname = db.Column(db.String(200), nullable=False)   
    phone = db.Column(db.String(20), nullable=False)       
    email = db.Column(db.String(120), nullable=False)      
    role = db.Column(db.String(20), default='user')        
    
    #связи с другими таблицами
    bookings = db.relationship('Booking', backref='user', lazy=True)  
    reviews = db.relationship('Review', backref='user', lazy=True)    
    
    def set_password(self, password):
        #хеширует перед сохранением пароль
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        #проверяет введенный пароль с хэшем в бд
        return bcrypt.check_password_hash(self.password, password)
    
    def is_admin(self):
        #проверка на права админа
        return self.role == 'admin'

#таблица заявок
class Booking(db.Model):

    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)          
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    room = db.Column(db.String(50), nullable=False)        
    date = db.Column(db.String(20), nullable=False)        
    time_start = db.Column(db.String(10), default='10:00') 
    payment_method = db.Column(db.String(50), nullable=False)  
    status = db.Column(db.String(50), default='новая')    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    
  
    review = db.relationship('Review', backref='booking', uselist=False)

#таблица отзывов
class Review(db.Model):
  
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)           
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)  
    rating = db.Column(db.Integer, default=5)             
    text = db.Column(db.Text, nullable=False)             
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  