from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Student(Resource): #inherit the resource class
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) # filter returns an filter object
        return {'item': item}, 200 if item else 404

class Item(Resource):
    @jwt_required()
    def get(self, name):
        return {'student': name}
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, 
                        required=True, 
                        help="This field cannot be left blank!"
    )
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #400 is bad request
        
        data = parser.parse_args()
        # data = request.get_json(force=True) # content type has to be application/json, silent=True does not return an error, it just returns an none
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # status code 202 is delaying about the creation
    
    def delete(self, name):
        global items #avoid the conflict between the local variable and the global variable.
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Items deleted'}
    
    #no matter how many times you call it the output should not change
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Student, '/student/<string:name>')
api.add_resource(Item, '/item/<string:item>')
api.add_resource(ItemList, '/items')
app.run(port=5001, debug=True)