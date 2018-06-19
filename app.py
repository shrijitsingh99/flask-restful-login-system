from flask import Flask, render_template
from flask_restful import Api
from flask_session import Session

from Resources.login import UserLogin
from Resources.register import UserRegister
from Resources.profile import UserProfile
from Resources.logout import UserLogout
from db import db
from ma import ma

app = Flask(__name__)
app.secret_key = "password"

# SQLAlchemy Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Session Configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # TODO: On production set to True
# PERMANENT_SESSION_LIFETIME  # TODO: Set value on production
app.config["SESSION_TYPE"] = "sqlalchemy"
# SESSION_PERMANENT # TODO: On production set to False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_SQLALCHEMY"] = db
app.config["SESSION_SQLALCHEMY_TABLE"] = "Session"

api = Api(app)
db.init_app(app)
session = Session()

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(UserProfile, "/<string:username>")
api.add_resource(UserLogout, "/logout")

if __name__ == '__main__':
    session.init_app(app)
    ma.init_app(app)
    app.run()
