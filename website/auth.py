"""
Конференции.РФ - Модуль авторизации
Регистрация, вход и выход из системы
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm


auth_bp = Blueprint('auth', __name__)

#страница входа
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  
    #если пользователь уже авторизован перенаправляет на свои страницы
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.admin_panel'))
        return redirect(url_for('views.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        #ищет пользователя по логину
        user = User.query.filter_by(login=form.login.data).first()
        
        #проверяет существование пользователя и правильность пароля
        if user and user.check_password(form.password.data):
            login_user(user)  #сохраняет пользователя в сессии
            flash('Добро пожаловать!', 'success')
            
            #перенапровляет на страницу в зависимости от роли
            if user.is_admin():
                return redirect(url_for('admin.admin_panel'))
            return redirect(url_for('views.dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('login.html', form=form)

#страница регистрации
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
 
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        #создание нового пользователя
        user = User(
            login=form.login.data,
            fullname=form.fullname.data,
            phone=form.phone.data,
            email=form.email.data,
            role='user'  
        )
        user.set_password(form.password.data)  #хэшируем пароль
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь войдите в систему', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

#выход из системы
@auth_bp.route('/logout')
@login_required  
def logout():
   
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))