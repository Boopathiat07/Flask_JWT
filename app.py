from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .api.views import view
import os

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")

app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"
app.register_blueprint(view)

db = SQLAlchemy(app)

# if __name__ == "__main__":
#     app.run()