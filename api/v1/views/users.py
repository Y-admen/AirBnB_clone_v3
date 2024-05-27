#!/usr/bin/python3
"""users"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    '''Retrieves a list of all User objects'''
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''Retrieves an User object'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        abort(400, 'Missing email')
    if not password:
        abort(400, 'Missing password')
    new_user = User(email=email, password=password)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Deletes'''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
