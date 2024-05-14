import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, LoginForm, EditUserForm
from models import db, connect_db, User, Follows, Watch_Later, Favorites
from my_secrets import MY_API_KEY, DB_URI, SECRET_KEY

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET_KEY'] = SECRET_KEY

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/', methods = ['GET'])
def home_page():
    return render_template('home_page.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Handle user register."""

    form = RegisterForm()

    if form.validate_on_submit():
    # if form.is_submitted() and form.validate():
        try:
            user = User.signup(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
            )

            db.session.commit()

        except IntegrityError:
            flash('Username is already taken', 'danger')
            return render_template('register.html', form = form)

        do_login(user)

        return redirect('/')

    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Handle logging in a user"""
    form = LoginForm
    return render_template('login.html', form = form)
    