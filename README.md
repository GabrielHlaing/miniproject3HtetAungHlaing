### INF601 - Advanced Programming in Python
### Htet Aung Hlaing
### Mini Project 3

# Project Title

Mini Project 3: Recipe Sharing Web Application

## Description

- This project is a full-stack recipe management web application built using **Flask**.  
- It allows users to register, log in, create, edit, and delete their recipes.  
- Each recipe is stored in an SQLite database and linked to its author’s profile.  

The app also uses **Bootstrap** for to style as a modern and elegant interface, featuring modals for profile editing and delete confirmations, and a card-based recipe layout.

## Getting Started

### Dependencies
* Install the required packages using:
```commandline
pip install -r requirements.txt
```

### Initialize Database
* Create a database table by:
```commandline
flask --app Recipe init-db 
```
### Executing the Program

Run the Flask app with:
```commandline
flask --app Recipe run
```
* Then open your browser and visit: `http://127.0.0.1:5000/`


## Features

* User authentication (register, login, logout)
* Create, edit, and delete recipes
* Profile editing modal with live form updates
* Card-based recipe listing with dark theme
* Bootstrap modals for delete confirmations
* SQLite database integration
* Flash message system for success/error notifications

## Authors

* Htet Aung Hlaing

## Version History

* 1.0  
    * Complete Flask CRUD application  
    * Dark Bootstrap UI added  
    * Profile edit and delete modals implemented  

## Acknowledgments

* [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
* [Bootstrap 5](https://getbootstrap.com/)
* [SQLite](https://www.sqlite.org/)
