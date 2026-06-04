from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Booking, Review
from .forms import BookingForm


views_bp = Blueprint('views', __name__)
#главная страница
@views_bp.route('/')
def index():
   #перенаправления на страницы
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.admin_panel'))
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('auth.login'))

#личный кабинет
@views_bp.route('/dashboard')
@login_required  # только для авторизованных
def dashboard():

    #проверка на админа
    if current_user.is_admin():
        return redirect(url_for('admin.admin_panel'))
    
    #получение заявок
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    
   #для отзывов
    for booking in bookings:
        booking.can_review = (booking.status == 'мероприятие завершено' and not booking.review)
    
    return render_template('dashboard.html', bookings=bookings)

#страница для создания заявки
@views_bp.route('/new_booking', methods=['GET', 'POST'])
@login_required
def new_booking():

    if current_user.is_admin():
        return redirect(url_for('admin.admin_panel'))
    
    form = BookingForm()
    
    if form.validate_on_submit():
        #создаем новую заявку
        booking = Booking(
            user_id=current_user.id,
            room=form.room.data,
            date=form.date.data,
            payment_method=form.payment_method.data,
            status='новая'  #новые заявки всегда имеют статус 'новая'
        )
        db.session.add(booking)
        db.session.commit()
        
        flash('Заявка успешно создана и отправлена на согласование!', 'success')
        return redirect(url_for('views.dashboard'))
    
    return render_template('new_booking.html', form=form)

#обработка отправки отзыва
@views_bp.route('/review/<int:booking_id>', methods=['POST'])
@login_required
def add_review(booking_id):
    
    #находим заявку по ID
    booking = Booking.query.get_or_404(booking_id)
    
    #проверяем что отзыв оставляет владелец заявки
    if booking.user_id != current_user.id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Доступ запрещен'}), 403
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('views.dashboard'))
    
    #проверяем что мероприятие завершено
    if booking.status != 'мероприятие завершено':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Отзыв можно оставить только после завершения мероприятия'}), 400
        flash('Отзыв можно оставить только после завершения мероприятия', 'warning')
        return redirect(url_for('views.dashboard'))
    
    # проверяем не оставлен ли уже отзыв
    if booking.review:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Отзыв уже оставлен'}), 400
        flash('Отзыв уже оставлен', 'info')
        return redirect(url_for('views.dashboard'))
    
    #получаем текст отзыва из формы
    text = request.form.get('text', '')
    
    # проверка текста
    if not text.strip():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Введите текст отзыва'}), 400
        flash('Введите текст отзыва', 'danger')
        return redirect(url_for('views.dashboard'))
    
    #создаем новый отзыв
    review = Review(
        user_id=current_user.id,
        booking_id=booking.id,
        rating=5,  # Оценка по умолчанию 5 (убрали звезды)
        text=text.strip()
    )
    db.session.add(review)
    db.session.commit()
    
    #возвращаем ответ в зависимости от типа запроса
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Спасибо за отзыв!'})
    
    flash('Спасибо за ваш отзыв!', 'success')
    return redirect(url_for('views.dashboard'))