from factory import create_app
from api.views.views import user_view
from api.views.google_oauth import oauth2_view
from api.views.mongodb_crud import mongodb_view
from api.views.file_upload import file_view
from api.views.geo_code_data import geo_view

app = create_app.app
db = create_app.db

app.register_blueprint(user_view)
app.register_blueprint(oauth2_view)
app.register_blueprint(mongodb_view)
app.register_blueprint(file_view)
app.register_blueprint(geo_view)

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":

    app.run(debug=True)

