from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
