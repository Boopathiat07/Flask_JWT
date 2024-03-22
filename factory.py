from flask import Flask
from config import Config
from api.views.view import view
from api.views.rbac import rbac_view
from middleware.authentication import jwt_authentication

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(view)
    app.register_blueprint(rbac_view)
    app.before_request(jwt_authentication)

    return app
    


