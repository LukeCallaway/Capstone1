from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    """User register form."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form for editing user profile"""

    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [Length(min=6)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

class SearchMovie(FlaskForm):
    """search credenitals for api request"""

    # all optional but 1 required?
    movie_name = StringField('Movie Name')
    year = StringField('Year of Release')
    actor = StringField('Actor Name')

class SearchMovieByName(FlaskForm):
    """search api by movie title or actor name"""

    name = StringField('Search By Movie Title')

class AddToFav(FlaskForm):
    """search api by actors"""

    movie_rating = IntegerField('Give Movie A Rating')