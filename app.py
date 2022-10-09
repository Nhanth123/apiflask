import os
import urllib

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError
from urllib.parse import quote

from db import db
from ma import ma
from resources.user import UserRegister, UserLogin, User
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///data.db")

params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-AK4UPFQ;DATABASE=TreasuryIntegrationAPI;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = 'abcd1234'
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":

    ma.init_app(app)
    app.run(port=5000, debug=True)
