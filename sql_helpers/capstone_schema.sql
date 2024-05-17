
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL
        CHECK (position('@' IN email) > 1)

)