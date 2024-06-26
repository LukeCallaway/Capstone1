# Project Proposal

Use this template to help get you started right away! Once the proposal is complete, please let your mentor know that this is ready to be reviewed.

## Get Started

|            | Description                                                                                                                                                                                                                                                                                                                                              | Fill in |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| Tech Stack | What tech stack will you use for your final project? It is recommended to use the following technologies in this project: Python/Flask, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful APIs, JavaScript, HTML, CSS. Depending on your idea, you might end up using WTForms and other technologies discussed in the course.                               |HTML, CSS, Javascript, Python, Flask, Jinja, Bcyrpt, RESTful APIs, WTForms, SQL, SQLAlchemy, PostgreSQL|
| Type       | Will this be a website? A mobile app? Something else?                                                                                                                                                                                                                                                                                                    |     Website    |
| Goal       | What goal will your project be designed to achieve?                                                                                                                                                                                                                                                                                                      |Let users save favorites, get reccomendations, share their personal favorite movies with other users.|
| Users      | What kind of users will visit your app? In other words, what is the demographic of your users?                                                                                                                                                                                                                                                           |Anyone who is a movie lover, or wanting to become one.|
| Data       | What data do you plan on using? How are you planning on collecting your data? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. You are welcome to create your own API and populate it with data. If you are using a Python/Flask stack, you are required to create your own API. |Data about movies including title, release year, preview, summary, cast, rating|

# Breaking down your project

When planning your project, break down your project into smaller tasks, knowing that you may not know everything in advance and that these details might change later. Some common tasks might include:

- Determining the database schema
- Sourcing your data
- Determining user flow(s)
  - Browse the home page
    - Get info on popular or new movie releases
    - find other people's created list for potential movies to watch
  - After logging in
    - Have the home page more curated to their taste
    - Create or edit a list of movies to share with others
      - All found on the users personal page
      - Removing a movie off of their watch later list after watching it
      - Adding a movie they really like to their favorites list
      - Seeing lists of people they follow
    - Browse the movie lists others have made 
      - Found on other people's pages can view by serch bar
      - Have a search for certain types of lists?
      - like the lists so they can see it at a later date
- Setting up the backend and database
- Setting up the frontend
- What functionality will your app include?
  - User login and sign up
  - Uploading a user profile picture
  - Home page with:
    - popular and / or newest movies
    - show user created lists either randomly / most upvoted / based on users preferences
    - search function with various filters
  - User's page with:
    - All user created lists of favorites, watch later etc
    - Any lists from other uses that they have viewed, liked, or saved
    - to be continued
  - Movie page with:
    - Info about a movie
    - Ways to add it to any user's list
    - Potentially add a clip of the movie trailer
    - Reviews / how many likes from other users of the platform

Here are a few examples to get you started with. During the proposal stage, you just need to create the tasks. Description and details can be edited at a later time. In addition, more tasks can be added in at a later time.

| Task Name                   | Description                                                                                                   | Example                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Design Database schema      | Determine the models and database schema required for your project.                                           | [Link](https://github.com/LukeCallaway/Capstone1/issues/2) |
| Choosing API                | Determine which API to use. Create an API aswell from personal users data.                                    | [Link](https://github.com/LukeCallaway/Capstone1/issues/3) |
| User Flows                  | Determine user flow(s) - think about what you want a user’s experience to be like as they navigate your site. | [Link](https://github.com/LukeCallaway/Capstone1/issues/10) |
| Set up backend and database | Configure the model classes and set up database.                                                              | [Link](https://github.com/LukeCallaway/Capstone1/issues/9) |
| Set up frontend             | Create all HTML, CSS, and Javascript files necesary. Including any templates / base files.                    | [Link](https://github.com/LukeCallaway/Capstone1/issues) Issues 6,7 ,and 8|
| User Authentication         | Fullstack feature - ability to authenticate (login and sign up) as a user                                     | [Link](https://github.com/LukeCallaway/Capstone1/issues/1) |
| Forums                      | Create the ability for users to interact with each other and discuss various topics                           | [Link](https://github.com/LukeCallaway/Capstone1/issues/11)|
| WTForms                     | Make all the necassery form classes need for the whole website                                                | [Link](https://github.com/LukeCallaway/Capstone1/issues/4) |

## Labeling

Labeling is a great way to separate out your tasks and to track progress. Here’s an [example](https://github.com/hatchways/sb-capstone-example/issues) of a list of issues that have labels associated.

| Label Type    | Description                                                                                                                                                                                                                                                                                                                     | Example                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Difficulty    | Estimating the difficulty level will be helpful to determine if the project is unique and ready to be showcased as part of your portfolio - having a mix of task difficultlies will be essential.                                                                                                                               | Easy, Medium, Hard           |
| Type          | If a frontend/backend task is large at scale (for example: more than 100 additional lines or changes), it might be a good idea to separate these tasks out into their own individual task. If a feature is smaller at scale (not more than 10 files changed), labeling it as fullstack would be suitable to review all at once. | Frontend, Backend, Fullstack |
| Stretch Goals | You can also label certain tasks as stretch goals - as a nice to have, but not mandatory for completing this project.                                                                                                                                                                                                           | Must Have, Stretch Goal      |

search with grouping of multiple movies
serach by other users that have certain movies or multiple movies on their own personal lists

finding the movie trailer is easy if the api already has the yt link on it 
  otherwise it could be more involved by also using the yt api
