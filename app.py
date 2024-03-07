from createApp import db, app
from api.views import user_view

app.register_blueprint(user_view)

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run()

