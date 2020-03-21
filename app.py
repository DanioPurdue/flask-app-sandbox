from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
items = []
class Student(Resource): #inherit the resource class
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

class Item(Resource):
    def get(self, name):
        return {'student': name}
    
    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item, 201 # status code 202 is delaying about the creation
api.add_resource(Student, '/student/<string:name>')
api.add_resource(Item, '/item/<string:item>')
app.run(port=5001, debug=True)