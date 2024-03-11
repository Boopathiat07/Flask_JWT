from create_app import db, app
from api.views import user_view
from api.google_oauth import oauth2_view
from api.mongodb_crud import mongodb_view

app.register_blueprint(user_view)
app.register_blueprint(oauth2_view)
app.register_blueprint(mongodb_view)

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

