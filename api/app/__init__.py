# Import flask and template operators
from flask import Flask

from pymongo import MongoClient

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("app.config")

# Define the database object which is imported
# by modules and controllers
client = MongoClient(
    'mongodb://api:MsfqxRh80C9nDP9j@buildingok-shard-00-00-x0spo.azure.mongodb.net:27017/'
)

db = client['test-database']


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return ("Not at home", 404)


from app.mod_user.controllers import mod_user as user_module
from app.mod_admin.controllers import mod_admin as admin_module
from app.mod_bot.controllers import mod_bot as bot_module

# Import a module / component using its blueprint handler variable (mod_auth)
# Register blueprint(s)
app.register_blueprint(user_module)
app.register_blueprint(admin_module)
app.register_blueprint(bot_module)
