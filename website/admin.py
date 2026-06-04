"""
Конференции.РФ - Админ-панель
Управление заявками, фильтрация, сортировка, статистика
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Booking, User

# Создаем Blueprint для админ-маршрутов
admin_bp = Blueprint('admin', __name__)

#декоратор для проверки прав админа
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Доступ запрещен. Требуются права администратора.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

#главная страница админа
@admin_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
   
    #получает параметры из URL
    page = request.args.get('page', 1, type=int)           # Номер страницы
    status_filter = request.args.get('status', '')         # Фильтр по статусу
    room_filter = request.args.get('room', '')             # Фильтр по помещению
    sort = request.args.get('sort', 'newest')              # Сортировка
    
    #базовый запрос
    query = Booking.query
    
    #фильтры
    if status_filter:
        query = query.filter_by(status=status_filter)
    if room_filter:
        query = query.filter_by(room=room_filter)
    
    #сортировка
    if sort == 'newest':
        query = query.order_by(Booking.created_at.desc()) 
    elif sort == 'oldest':
        query = query.order_by(Booking.created_at.asc())  
    elif sort == 'date_asc':
        query = query.order_by(Booking.date.asc())       
    elif sort == 'date_desc':
        query = query.order_by(Booking.date.desc())       
    
    # Пагинация (10 заявок)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    bookings = pagination.items
    
    #получает всех пользователей для отображения ФИО
    users = {u.id: u for u in User.query.all()}
    
    return render_template('admin.html', 
                         bookings=bookings, 
                         pagination=pagination,
                         status_filter=status_filter,
                         room_filter=room_filter,
                         sort=sort,
                         users=users)

  #API endpoint для изменения статуса заявки. Принимает JSON с новым статусом
@admin_bp.route('/admin/update_status/<int:booking_id>', methods=['POST'])
@login_required
@admin_required
def update_status(booking_id):

   
    data = request.get_json()
    new_status = data.get('status')
    
    #yаходиn заявку и обновляеn статус
    booking = Booking.query.get_or_404(booking_id)
    booking.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'status': new_status})

