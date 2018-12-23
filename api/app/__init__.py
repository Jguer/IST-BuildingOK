# Import flask and template operators
from flask import request, current_app, Flask

from pymongo import MongoClient

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("app.config")

# Define the database object which is imported
# by modules and controllers
client = MongoClient(
    'mongodb+srv://api:MsfqxRh80C9nDP9j@buildingok-x0spo.azure.mongodb.net/test?retryWrites=true'
)

db = client['test-database']

# if not db.Building.list_indexes():
db.User.create_index([("cur_pos", '2dsphere')])
# db.Building.create_index({'position': '2dsphere'})
db.Building.create_index([("position", '2dsphere')])

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return ("Not at home", 404)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers[
            'Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


from app.mod_user.controllers import mod_user as user_module
from app.mod_admin.controllers import mod_admin as admin_module
from app.mod_bot.controllers import mod_bot as bot_module

# Import a module / component using its blueprint handler variable (mod_auth)
# Register blueprint(s)
app.register_blueprint(user_module)
app.register_blueprint(admin_module)
app.register_blueprint(bot_module)

app.after_request(add_cors_headers)
