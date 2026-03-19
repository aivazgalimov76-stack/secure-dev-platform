from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import db, User

# Создаем blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # логируем попытку регистрации
        from flask import current_app
        current_app.logger.info('Registration attempt', extra={
            'event': 'register_attempt',
            'username': username,
            'email': email,
            'ip': request.remote_addr
        })
        
        # Проверяем, существует ли пользователь
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Пользователь уже существует')
            return redirect(url_for('auth.register'))
        
        # Хешируем пароль и создаем пользователя
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()

        # логируем успешную регистрацию
        current_app.logger.info('Registration successful', extra={
            'event': 'register_success',
            'username': username,
            'user_id': new_user.id
        })
        
        flash('Регистрация успешна!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        # логируем попытку входа
        from flask import current_app
        current_app.logger.info('Login attempt', extra={
            'event': 'login_attempt',
            'username': username,
            'ip': request.remote_addr
        })
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            # логируем неудачный вход
            current_app.logger.warning('Login failed', extra={
                'event': 'login_failed',
                'username': username,
                'ip': request.remote_addr
            })
            flash('Неверные данные')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        
        # логируем успешный вход
        current_app.logger.info('Login successful', extra={
            'event': 'login_success',
            'username': username,
            'user_id': user.id,
            'ip': request.remote_addr
        })
        
        return redirect(url_for('blog.index'))
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('blog.index'))
