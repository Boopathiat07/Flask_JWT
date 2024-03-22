from factory import create_app
from models.db_models import *
app = create_app()

if __name__ == "__main__":
    app.run(port=app.config["PORT"], debug=True)



    