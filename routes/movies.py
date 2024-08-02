from flask import Blueprint, render_template, redirect, session, g, flash

from forms import AddToFav
from models.users import User
from db import db
from models.favorites import Favorites
from models.watch_later import Watch_Later
from api_calls import Api_calls

movies = Blueprint('movies', __name__, static_folder='static', template_folder='templates')

@movies.route('/<int:id>', methods=['GET','POST'])
def movie_info(id):
    """Get all info for a single movie based on passed in id"""
    movie = Api_calls.get_all_info(id)
    fav = Favorites.get_fav(g.user.id, movie['id'])

    form = AddToFav(obj=fav) # pre populate form with db movie rating if fav exists

    if form.validate_on_submit():

        movie_rating = form.movie_rating.data

        if not Favorites.is_valid_rating(movie_rating):
            flash('Movie rating must be between 0 and 100!', 'danger')
            return redirect(f'/movies/{id}')

        if fav:
            fav.update_fav(movie_rating)

        else:
            g.user.add_fav(id, movie['title'], movie_rating)

        return redirect(f'/movies/{id}')

    # display 5 similar movies        
    sim_titles_info = Api_calls.get_similar_titles(movie['similar_titles'][:1])

    return render_template('single_movie_info.html', movie = movie, form = form,  sim_titles_info = sim_titles_info, fav = fav)

@movies.route('<int:id>/watch-later', methods=['POST'])
def add_to_watch_later(id):

    movie = Api_calls.get_all_info(id)

    # queries watch_later to check if movie is already there
    if Api_calls.is_on_list(g.user.id, movie['id'], Watch_Later):
        flash('Movie already in watch later', 'danger')
        return redirect(f'/movies/{id}')
    
    g.user.add_watch_later(id, movie['title'])
    flash('Added to Watch Later List!', 'success')

    return redirect(f'/movies/{id}')