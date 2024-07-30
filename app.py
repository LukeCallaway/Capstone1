import os
from dotenv import dotenv_values

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError
import requests

from db import db, connect_db
from forms import RegisterForm, LoginForm, EditUserForm, SearchMovieByName, AddToFav
from api_calls import Api_calls

from models.favorites import Favorites
from models.follows import Follows
from models.users import User
from models.watch_later import Watch_Later

from routes.auth import auth, CURR_USER_KEY
from routes.movies import movies
from routes.users import users

app = Flask(__name__)

secrets = dotenv_values('.env')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL') or secrets['DB_URI'])
app.config['SECRET_KEY'] = (
    os.environ.get('SECRET_KEY') or secrets['SECRET_KEY'])
app.config['MY_API_KEY'] = (
    os.environ.get('MY_API_KEY') or secrets['MY_API_KEY'])

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

app.register_blueprint(auth, url_prefix='')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(movies, url_prefix='/movies')

@app.route('/', methods = ['GET','POST'])
def home_page():
    """Home Page for logged in users"""
    if not g.user:
        return redirect('/register')

    suggestions = Api_calls.get_suggestions(g.user.id)
    form = SearchMovieByName()

    if form.validate_on_submit():
        res = Api_calls.get_basic_info(form.name.data)

        return render_template('movie_search_list.html', name = form.name.data, res = res['results'], list_length = len(res['results']))

    return render_template('home_page.html', form = form, followings = g.user.following, suggestions = suggestions)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')