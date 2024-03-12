from create_app import app
from authlib.integrations.flask_client import OAuth
from flask import url_for, Blueprint
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_META_URL=os.getenv('GOOGLE_META_URL')
GOOGLE_SCOPE=os.getenv('GOOGLE_SCOPE')

oauth = OAuth(app)

oauth2_view = Blueprint('oauth2_view',__name__)

oauth.register(
    "oauth2login",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": GOOGLE_SCOPE,
    },
    server_metadata_url=f'{GOOGLE_META_URL}',
)

@oauth2_view.route("/oauthlogin")
def google_login():
    return oauth.oauth2login.authorize_redirect(redirect_uri=url_for("oauth2_view.google_callback", _external=True))

@oauth2_view.route("/signin-google")
def google_callback():
    token = oauth.oauth2login.authorize_access_token(access_type="offline")
    return token

