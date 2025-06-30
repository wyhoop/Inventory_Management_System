from config.config import DevConfig
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from models.models import Product, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app, doc="/docs")


# model (serializer)
product_model = api.model(
    "Product",
    {
        "id" : fields.Integer(),
        "name": fields.String(),
        "sku" : fields.String(),
        "description" : fields.String(),
        "current_quantity" : fields.Integer(),
    }
)

sign_up_model = api.model(
    "SignUp",
    {
        "username" : fields.String(),
        "password" : fields.String(),
        "access_level" : fields.String()
    }
)

@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World"}
    
@api.route('/signup')
class SignUp(Resource):
    @api.expect(sign_up_model)
    def post(self):
        data = request.get_json()

        username = data.get('username')

        db_user = User.query.filter_by(username=username).first()

        if db_user is not None:
            return jsonify({"message" : "User with that username already exists!"}) # TODO: Maybe route this to login?

        new_user = User(
            username = data.get('username'),
            password = generate_password_hash(data.get('password')),
            access_level = data.get('access_level') # TODO: Consider changing this to 'role'?
        )

        new_user.save()

        return jsonify({"message" : f"User, {username} succesfully created."})


@api.route('/login')
class Login(Resource):
    def post(self):
        pass
    


@api.route('/products')
class ProductsResource(Resource):
    @api.marshal_list_with(product_model) # Allows us to be able to understand the sqlalchemy model by serializing the onject into a dict
    def get(self):
        """Get all products from database"""

        products=Product.query.all()

        return products
    
    @api.marshal_with(product_model)
    @api.expect(product_model)
    def post(self):
        """Create a new product in inventory"""

        data = request.get_json() # Helps us get data that comes from any client that may send this data

        new_product = Product(
            name = data.get('name'),
            sku = data.get('sku'),
            description = data.get('description'),
            current_quantity = data.get('current_quantity')
        )

        new_product.save() #from models.py

        return new_product, 201

@api.route('/product/<int:id>')
class ProductResource(Resource):
    @api.marshal_with(product_model)
    def get(self, id):
        """Get a product by id"""
        product = Product.query.get_or_404(id)

        return product

    @api.marshal_with(product_model)
    def put(self, id):
        """Update a product by its id"""
        
        product_to_update = Product.query.get_or_404(id) 

        data = request.get_json()

        product_to_update.update(
            data.get('name'),
            data.get('sku'),
            data.get('description'),
            data.get('current_quantity')
            )
        
        return product_to_update

    @api.marshal_with(product_model)
    def delete(self, id):
        """Delete a product by id"""
        
        product_to_delete = Product.query.get_or_404(id)

        product_to_delete.delete()

        return product_to_delete



@app.shell_context_processor
def make_shell_context():
    return {
        "db" : db,
        "Product" : Product
    }
    

if __name__=="__main__":
    app.run()