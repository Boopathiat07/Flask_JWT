from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# import os
from createapp import app, db
from api.views import crud_view

app.register_blueprint(crud_view)

# load_dotenv()

# USER_NAME = os.getenv("USER_NAME")
# PASSWORD = os.getenv("PASSWORD")
# HOST = os.getenv("HOST")
# DB_NAME = os.getenv("DB_NAME")

# db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)