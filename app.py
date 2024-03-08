from create_app import db, app
from api.views import user_view
from api.usercron import emailTask
from flask_crontab import Crontab

app.register_blueprint(user_view)
app.register_blueprint(emailTask)

crontab = Crontab(app)

@crontab.job(minute="1")
def send_email():
    print("hello !! ") 

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run()

