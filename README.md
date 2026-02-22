
# PASSED

The backend repository for passed - torist pass portal wherein the user can add, update, remove items in cart and for each cart  a pass with unique passcode will be generated


## Tech Stack

- Django
- Django Rest Framework
- dbsqlite(database)
- Django ORM
- Django Silk(for query optimization)
- Render


## Installation

- Clone using the following repo link


```bash
git clone https://github.com/san031/passed.git buypasspage
```

- Go to the project folder and run npm install

```bash
cd buypasspage

npm install
```


- Now run the app

```bash 
npm run dev
```

## Features

- Token based authentication is used for login and logout functionality
- Django ORM is used to make queries in the backend
- All API endpoints returns standardized response format
- Separate apps such as cart, pass, base are created so as to handle cohesiveness
- Cart app contains api endpoints to create, update, remove items or to delete the whole cart
- Pass app contains endpoints to generate pass or view pass
- Base app handles api endpoints to generate user token, user profile details, view tourists spots
