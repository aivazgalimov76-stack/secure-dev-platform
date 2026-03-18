from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flaskr.models import db, Post

# Создаем blueprint
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        post = Post(
            title=title,
            body=body,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Пост создан!')
        return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    
    if post.user_id != current_user.id:
        flash('Нет прав')
        return redirect(url_for('blog.index'))
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']
        db.session.commit()
        flash('Пост обновлен')
        return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    
    if post.user_id != current_user.id:
        flash('Нет прав')
        return redirect(url_for('blog.index'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Пост удален')
    return redirect(url_for('blog.index'))
