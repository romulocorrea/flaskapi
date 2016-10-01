# Flask-API

This repository is part of an assignment from my web development class which I have to create a bookmark manager to every new user.
The project was defined to use Django to do it, buuuut, since I'm pretty much stubborn to KISS, I've decided to create a REST of it :)
Searching about REST using Django, I found out it was still pretty messy. I don't like Django handling everything! I looked around and ended up finding Flask!

It was perfect for my project! Since I'm a JavaScript developer, Flask remembered me so much about NodeJS in a way of providing simple and fast ways to create a REST. So that's how it was set. Flask, I choose you!

Note it was used an EC2 instance in AWS to create a MongoDB server once mLab seems to keep it hard to change user permissions :angry: So, if the database is not working anymore when you get this project, just point to your local MongoDB server in the config file :smile:

### Project's requirements:
    - Python 2.7
    - MongoDB
    - Flask

### REST endpoints:
##### Unsecured routes:
  - `/api/v1/users/new`
    - `POST` - create a new user


  - `/api/v1/auth`
    - `POST` - login which returns a token

##### Secured routes:
  - `/api/v1/users` (admin only)
    - `GET` - returns a list of users


  - `/api/v1/users/<id>` (admin / own user)
    - `GET` - returns details about a specific user
    - `PUT` - update a specific user
    - `DELETE` - delete a specific user


  - `/api/v1/pages` (admin / own user's pages)
    - `GET` - returns a list of pages


  - `/api/v1/pages/<id>` (admin / own user's pages)
    - `GET` - returns details about a specific page
    - `PUT` - update a specific user
    - `DELETE` - delete a specific user


  - `/api/v1/categories` (admin / own user's categories)
    - `GET` - returns a list of categories


  - `/api/v1/categories/<id>` (admin / own user's categories)
    - `GET` - returns details about a specific category
    - `PUT` - update a specific category
    - `DELETE` - delete a specific category
