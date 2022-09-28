from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse
from item import ItemList, Item
from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = 'abcd1234'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
