import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, LoginForm, EditUserForm, SearchMovieByName
from models import db, connect_db, User, Follows, Watch_Later, Favorites
from my_secrets import MY_API_KEY, DB_URI, SECRET_KEY
from api_call_functions import get_basic_info, get_all_info

import requests

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
    """Home Page for logged in and logged out users"""
    
    if g.user:

        return render_template('home_page.html')

    return render_template('home_page_anon.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Handle user register."""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username = form.username.data,
                password = form.password.data,
                email = form.email.data
            )

            db.session.commit()

        except IntegrityError:
            flash('Username is already taken', 'danger')
            return render_template('register.html', form = form)

        do_login(user)
        flash(f'Welcome, {user.username}!', 'success')


        return redirect('/')

    return render_template('users/register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Handle logging in a user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect('/')

        flash('Invalid username or password', 'danger')

    return render_template('users/login.html', form = form)

@app.route('/logout')
def logout():
    """Handle logging out a user"""

    do_logout()

    flash('You were succssfully logged out!', 'success')

    return redirect('/')

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Show user profile"""
    
    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Display edit user form"""

    form = EditUserForm(obj = g.user)

    if not g.user:
        flash('Access unauthorized', 'danger')

    if form.validate_on_submit():
        if g.user.check_password(form.password.data):
            g.user.username = form.username.data
            g.user.email = form.email.data
            g.first_name = form.first_name.data
            g.last_name = form.last_name.data

            db.session.add(g.user)
            db.session.commit()

            flash('Info successfully updated!', 'success')
            return redirect('/')

        flash('Incorrect Password', 'danger')
        return render_template('edit.html', form = form, user = g.user)

    return render_template('edit.html', form = form, user = g.user)

@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people user is following"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    print(user.followers, user.following)
    return render_template('users/following.html', user=user)

@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)   

@app.route('/movies_search', methods=['GET', 'POST'])
def search_movies():
    """Search for a movie by actor or title"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchMovieByName()

    if form.validate_on_submit():
        name = form.name.data
        res = get_basic_info(name, 'autocomplete-search/')
        # res_list = [r['name'] for r in res['results']]
        return render_template('movie_search_list.html', res = res['results'])

    return render_template('movies_search.html', form = form)

@app.route('/movies_search/<int:id>')
def movie_info(id):
    """Get all info for a single movie based on passed in id"""

    movie = get_all_info(id)

    return render_template('single_movie_info.html', movie = movie)













@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')