
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from .models import User

#форма для регистрации
class RegistrationForm(FlaskForm):
    
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=6, message='Логин должен быть минимум 6 символов'),
        Regexp(r'^[A-Za-z0-9]+$', message='Логин должен содержать только латинские буквы и цифры')
    ])
    
    password = StringField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=8, message='Пароль должен быть минимум 8 символов')
    ])
    
    fullname = StringField('ФИО', validators=[
        DataRequired(message='ФИО обязательно')
    ])
    
    phone = StringField('Телефон', validators=[
        DataRequired(message='Телефон обязателен')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email обязателен'),
        Email(message='Введите корректный email')
    ])
    
    def validate_login(self, field):
        #проверка на уникальность
        if User.query.filter_by(login=field.data).first():
            raise ValidationError('Логин уже существует')
#форма входа
class LoginForm(FlaskForm):

    login = StringField('Логин', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])

class BookingForm(FlaskForm):
    
    #варианты помещений для выбора
    ROOMS = [
        ('auditorium', 'Аудитория'),
        ('coworking', 'Коворкинг'),
        ('cinema', 'Кинозал')
    ]
    
    #варианты оплаты для выбора
    PAYMENT_METHODS = [
        ('qr', 'Предоплата по QR-коду'),
        ('mir', 'Оплата картой МИР'),
        ('postpay', 'Постоплата в офисе')
    ]
    
    room = SelectField('Помещение', choices=ROOMS, validators=[DataRequired()])
    date = StringField('Дата', validators=[DataRequired(message='Дата обязательна')], 
                       render_kw={"placeholder": "дд.мм.гггг"})
    payment_method = SelectField('Способ оплаты', choices=PAYMENT_METHODS, validators=[DataRequired()])

#форма для отзыва
class ReviewForm(FlaskForm):
   
    rating = IntegerField('Оценка', validators=[DataRequired()], default=5)
    text = TextAreaField('Отзыв', validators=[DataRequired(message='Введите текст отзыва')])