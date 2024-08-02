from flask import Blueprint, render_template, redirect, session, g, flash

from forms import RegisterForm, LoginForm
from models.users import User
from db import db

auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

CURR_USER_KEY = "curr_user"

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    flash(f'Welcome, {user.username}!', 'success')

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash('You were succssfully logged out!', 'success')
    else:
        return redirect('/')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    """Handle user register."""

    form = RegisterForm()

    if CURR_USER_KEY in session:
        return redirect('/')

    if form.validate_on_submit():
        try:
            user = User.register(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
            )

        except Exception:
            db.session.rollback()
            flash('Username is already taken', 'danger')
            return render_template('users/register.html', form = form)

        do_login(user)

        return redirect('/')

    return render_template('users/register.html', form = form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """Handle logging in a user"""

    form = LoginForm()

    if CURR_USER_KEY in session:
        return redirect('/')

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect('/')

        flash('Invalid username or password', 'danger')

    return render_template('users/login.html', form = form)

@auth.route('/logout')
def logout():
    """Handle logging out a user"""

    do_logout()
    return redirect('/register')