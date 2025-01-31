from flask import Flask, Blueprint, render_template, request, redirect, jsonify, url_for, session
from app.controllers.users_controller import UsersController

users = UsersController()
user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
def create():
    response, status = users.create(request.form)
    return jsonify(response), status

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response, status = users.login(request.form)

        if status == 200:
            session['user'] = response['user']

        return jsonify(response), status
    return render_template('users/login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('user.login'))

@user_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('users/signup.html')