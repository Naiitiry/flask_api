from flask import Blueprint, request, jsonify, abort
from flask_login import login_user, current_user, login_required, logout_user
from .models import db, Users, Post, Role

routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    user = Users(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    login_user(user)
    return jsonify({'message': 'Logged in successfully'}), 200

@routes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@routes.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    title = data['title']
    description = data['description']
    price = data['price']
    quantity = data['quantity']
    post = Post(title=title, description=description, price=price, quantity=quantity)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@routes.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'price': post.price,
        'quantity': post.quantity
    } for post in posts]), 200

@routes.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'price': post.price,
        'quantity': post.quantity
    }), 200

@routes.route('/posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    data = request.get_json()
    post.title = data['title']
    post.description = data['description']
    post.price = data['price']
    post.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'}), 200

@routes.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.role != Role.ADMIN:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200
