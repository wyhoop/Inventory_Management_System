from exts import db


"""
class Products:
    id: int Primary key
    name: str (text)
    sku: str(text)
    description: str (text)
    current_quantity: int
"""

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.Text(), nullable = False)
    sku = db.Column(db.Text(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    current_quantity = db.Column(db.Integer(), nullable = False)

    def __repr__(self):
        return f"<Product {self.name} >"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, name, sku, description, current_quantity):
        self.name = name
        self.sku = sku
        self.description = description
        self.current_quantity = current_quantity

        db.session.commit()

# User Model
"""
class User:
    id : integer -> PK
    username : string
    password : string
    access_level : Text
"""

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    password = db.Column(db.Text(), nullable = False)
    access_level = db.Column(db.Text(), nullable = False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, username, password, access_level):
        self.username = username
        self.password = password
        self.access_level = access_level

        db.session.commit()