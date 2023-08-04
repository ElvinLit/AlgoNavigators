from flask import Blueprint, render_template, request, flash, redirect, url_for
from .db_objs import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        testsuck = "hello world"
        user = User.query.filter_by(email=email).first() # Query (think SQL ig)
        if user:
            if check_password_hash(user.password, password): # Compares equality with first and second parameter
                login_user(user, remember=True) # Sets a user as being logged in
                return redirect(url_for('chat.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user) #Inside login.html, we can access variable 'user'!

@auth.route('/logout')
@login_required # Users can only logout after logging in (makes sense)
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST']) # We can specify different types of requests
def sign_up():
    if request.method == 'POST': # Specifying POST
        # See sign_up.html for where this is used
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 

        # Creating error messages
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 charracters', category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) # Adding this jit to our db
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('chat.home')) # Redirecting to our homepage

    return render_template("sign_up.html", user=current_user)