import os
from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"
