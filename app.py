import os

from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError

from forms import RegisterForm, LoginForm, EditUserForm, SearchMovieByName, AddToFav
from models import db, connect_db, User, Follows, Watch_Later, Favorites
from api_calls import get_basic_info, get_all_info, is_on_list,get_sim_to_favs, get_similar_titles, list_titles_by_genre, get_suggestions

import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

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

@app.route('/', methods = ['GET','POSt'])
def home_page():
    """Home Page for logged in users"""
    
    if g.user:
        suggestions = get_suggestions(g.user.id)
        form = SearchMovieByName()
        followings = g.user.following

        if form.validate_on_submit():
            name = form.name.data
            res = get_basic_info(name)
            list_length = len(res['results'])

            return render_template('movie_search_list.html', name = name, res = res['results'], list_length = list_length)

        return render_template('home_page.html', form = form, followings = followings, suggestions = suggestions)

    return redirect('/register')
#*************************************************************// auth routes
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

#*************************************************************\ user routes
@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Show user profile"""
    
    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user = user)

@app.route('/users/<int:user_id>/search')
def list_users(user_id):
    """Return list of users"""
    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    search = request.args.get('q')

    if not search:
        users = User.query.filter(User.id != g.user.id).all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%"), User.id != g.user.id).all()

    return render_template('users/index.html', users = users, user = g.user.id)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Display edit user form"""

    form = EditUserForm(obj = g.user)

    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    if form.validate_on_submit():
        if g.user.check_password(form.password.data):
            g.user.username = form.username.data
            g.user.email = form.email.data
            g.first_name = form.first_name.data
            g.last_name = form.last_name.data

            db.session.add(g.user)
            db.session.commit()

            flash('Info successfully updated!', 'success')
            return redirect(f'/users/{g.user.id}')

        flash('Incorrect Password', 'danger')
        return render_template('/users/edit.html', form = form, user = g.user)

    return render_template('/users/edit.html', form = form, user = g.user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def del_user(user_id):
    """Deletes User"""

    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    db.session.delete(user)
    db.session.commit()

    flash('Account deleted successfully', 'success')
    return redirect('/register')


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people user is following"""
    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    user = User.query.get_or_404(user_id)
    following_list_len = len(user.following)

    return render_template('users/following.html', user=user, following_list_len = following_list_len)

@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    user = User.query.get_or_404(user_id)
    follower_list_len = len(user.followers)
    print(follower_list_len, user.followers)
    return render_template('users/followers.html', user=user, follower_list_len = follower_list_len)   

@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):

    if not g.user:
        flash('Unauthorized', 'danger')
        return redirect('/')

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")

@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not g.user:
        flash('Unauthorized', 'danger')
        return redirect('/')

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")

@app.route('/users/<int:user_id>/favorites')
def user_favorites(user_id):

    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    favorites = (Favorites.query.filter(Favorites.user_id == user_id)
                                .order_by(Favorites.movie_rating.desc())
                                .all())
    list_length = (favorites)                                

    return render_template('users/favorites.html', user = user, favorites = favorites, list_length = list_length)

@app.route('/users/<int:user_id>/watch_later')
def user_watch_later(user_id):

    user = User.query.get_or_404(user_id)

    if g.user != user:
        flash('Access unauthorized', 'danger')
        return redirect(f'/users/{g.user.id}')

    watch_later = (Watch_Later.query.filter(Watch_Later.user_id == user_id)
                                .order_by(Watch_Later.movie_name)
                                .all())
    list_length = len(watch_later)

    return render_template('users/watch-later.html', user = user, watch_later = watch_later, list_length = list_length)

#****************************************************************************\ movie routes    

@app.route('/movies/<int:id>', methods=['GET','POST'])
def movie_info(id):
    """Get all info for a single movie based on passed in id"""
    movie = get_all_info(id)
    form = AddToFav()

    if form.validate_on_submit():
        movie_rating = form.movie_rating.data

        if movie_rating < 0 or movie_rating > 100:
            flash('movie rating must be between 0 and 100!', 'danger')
            return redirect(f'/movies/{id}')

        # queries favorites to check if movie is already in there
        if(is_on_list(g.user.id, movie['id'], Favorites)):
            flash('Movie already in favorites', 'danger')
            return redirect(f'/movies/{id}')

        new_fav = Favorites(user_id = g.user.id, movie_id = id, movie_name = movie['title'], movie_rating = movie_rating)

        db.session.add(new_fav)
        db.session.commit()

        flash('Added to Favorites List!', 'success')

        return redirect(f'/movies/{id}')

    # display 5 similar movies        
    similar_titles = movie['similar_titles'][:5]
    sim_titles_info = get_similar_titles(similar_titles)

    return render_template('single_movie_info.html', movie = movie, form = form,  sim_titles_info = sim_titles_info)



@app.route('/movies/<int:id>/watch-later', methods=['POST'])
def add_to_watch_later(id):

    movie = get_all_info(id)

    # queries watch_later to check if movie is already there
    if(is_on_list(g.user.id, movie['id'], Watch_Later)):
        flash('Movie already in watch later', 'danger')
        return redirect(f'/movies/{id}')
    
    new_watch_later = Watch_Later(user_id = g.user.id, movie_id = id, movie_name = movie['title'])
    
    db.session.add(new_watch_later)
    db.session.commit()

    flash('Added to Watch Later List!', 'success')

    return redirect(f'/movies/{id}')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')