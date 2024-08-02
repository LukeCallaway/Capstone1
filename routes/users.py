from flask import Blueprint, render_template, redirect, g, flash, request
from forms import EditUserForm

from models.favorites import Favorites
from models.users import User
from models.watch_later import Watch_Later
from db import db

users = Blueprint('users', __name__, static_folder='static', template_folder='templates')

@users.before_request
def check_for_user():
    """Checks if global user"""
    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

@users.route('/<int:user_id>')
def user_profile(user_id):
    """Show user profile"""
    
    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user = user)

@users.route('/<int:user_id>/search')
def list_users(user_id):
    """Return list of users"""
    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    search = request.args.get('q')

    if not search:
        users = User.query.filter(User.id != g.user.id).all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%"), User.id != g.user.id).all()

    return render_template('users/index.html', users = users, user = g.user.id)

@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Display edit user form"""

    form = EditUserForm(obj = g.user)
    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    if form.validate_on_submit():
        if g.user.check_password(form.password.data):
            g.user.update(form.username.data,
                          form.email.data,
                          form.first_name.data, 
                          form.last_name.data)

            flash('Info successfully updated!', 'success')
            return redirect(f'/users/{g.user.id}')

        flash('Incorrect Password', 'danger')
        return render_template('/users/edit.html', form = form, user = g.user)

    return render_template('/users/edit.html', form = form, user = g.user)

@users.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes User"""

    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    user.delete_user()
    flash('Account deleted successfully', 'success')
    
    return redirect('/register')


@users.route('/<int:user_id>/following')
def show_following(user_id):
    """Show list of people user is following"""

    user = User.query.get_or_404(user_id)
    
    user.check_user(g.user, f'/users/{g.user.id}')

    return render_template('users/following.html', user=user, following_list_len = len(user.following))

@users.route('/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    return render_template('users/followers.html', user=user, follower_list_len = len(user.followers))   

@users.route('/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):

    g.user.add_follow(follow_id)

    return redirect(f"/users/{g.user.id}/following")

@users.route('/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    g.user.remove_follow(follow_id)

    return redirect(f"/users/{g.user.id}/following")

@users.route('/<int:user_id>/favorites')
def user_favorites(user_id):
    """Displays all of a user's favorites"""

    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    favorites = Favorites.get_all_favs(user_id)
    return render_template('users/favorites.html', user = user, favorites = favorites, list_length = len(favorites))

@users.route('/<int:user_id>/watch_later')
def user_watch_later(user_id):
    """Displays all of a user's watch later movies"""

    user = User.query.get_or_404(user_id)

    user.check_user(g.user, f'/users/{g.user.id}')

    watch_later = Watch_Later.get_all_watch_laters(user_id)

    return render_template('users/watch-later.html', user = user, watch_later = watch_later, list_length = len(watch_later))