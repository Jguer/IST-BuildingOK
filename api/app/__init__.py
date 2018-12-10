# Import flask and template operators
from flask import Flask
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from app.mod_user.controllers import mod_user as user_module

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return ('Not at home', 404)


# Import a module / component using its blueprint handler variable (mod_auth)
# Register blueprint(s)
app.register_blueprint(user_module)
