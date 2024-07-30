# Capstone 1

To view Capstone 1 click [here](https://lukes-capstone-one.onrender.com/)

Capstone 1 is a site where you can interact with other users through your passion of movies. 

## How To Use
First thing you want to do when you go to the site is make an account! After that you are free to explore the rest of the site. There is a lot of potential things to do! \
Such as: 
 - View the movies on the homepage to see if anything interests you
 - Find and follow other users and see what kind of movies they are interested in
 - Search for movies you might be interested in 
 - Add movies to a watch later list
 - Add movies to a favorites list and give them a rating

## Running Code Locally

 1. Python version 3.10.12 was used for the project
 1. Get api key from [watchmode](https://api.watchmode.com/)
 1. Clone the repository 
 2. Set up a database with postgres
 2. Go to the root directory
 3. Add a ```.env``` file in the root directory with ```MY_API_KEY, DB_URI, SECRET_KEY``` variables in it. Database uri should look like this ```'postgresql:///your_db_name_here'```
 3. Run ```python3 -m venv venv``` to set up virtual enviorment
 4. Run ```source venv/bin/activate``` to start virtual enviorment
 5. Install requirements ```pip3 install -r requirements.txt```
 6. Start server ```flask run```
 7. Stop server ``` Ctrl c```
 8. Leave virtual enviorment ``` deactivate ``` 

API used for all movie data [watchmode](https://api.watchmode.com/) \
Tech stack used to create the site: Python, Flask, SQL, Sqlalchemy, HTML, CSS
