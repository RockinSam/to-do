from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Configure SQLite DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'groceries.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    purchased = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'purchased': self.purchased
        }

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/groceries', methods=['GET'])
def get_groceries():
    items = GroceryItem.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/groceries', methods=['POST'])
def add_grocery():
    data = request.json
    item = GroceryItem(name=data['name'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/groceries/<int:item_id>', methods=['PATCH'])
def toggle_grocery(item_id):
    item = GroceryItem.query.get(item_id)
    if item:
        item.purchased = not item.purchased
        db.session.commit()
        return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@app.route('/groceries/<int:item_id>', methods=['DELETE'])
def delete_grocery(item_id):
    item = GroceryItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
