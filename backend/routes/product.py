from flask import request, jsonify, Blueprint
from backend.models import Product
from backend import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError


products_bp = Blueprint('product', __name__)

def init_app(app):
    app.register_blueprint(products_bp)

@products_bp.route('/')
def hello_world():
    return 'Hello, World!'

@products_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        name = data['name']
        location_x = int(data.get('location_x', 0))  # Ensuring type correctness
        location_y = int(data.get('location_y', 0))
        price = float(data.get('price', 0.0))
        expiration_date = data.get('expiration_date')

        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')

        new_product = Product(name=name, location_x=location_x, location_y=location_y, price=price, expiration_date=expiration_date)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": f"Product '{name}' added successfully"}), 201

    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Product with this name already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<int:id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.serialize())
    else:
        return jsonify({"error": "Product not found"}), 404

@products_bp.route('/name/<string:name>', methods=['GET'])
def get_product_by_name(name):
    product = Product.query.filter_by(name=name).first()
    if product:
        return jsonify(product.serialize())
    else:
        return jsonify({"error": "Product not found"}), 404

@products_bp.route('/price/<string:name>', methods=['GET'])
def get_price_by_name(name):
    product = Product.query.filter_by(name=name).first()
    if product:
        return jsonify({'price': product.price})
    else:
        return jsonify({"error": "Product not found"}), 404

@products_bp.route('/update/<string:name>', methods=['PUT'])
def update_product(name):
    product = Product.query.filter_by(name=name).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.json
    for key in data:
        if hasattr(product, key):
            setattr(product, key, data[key])
    db.session.commit()
    return jsonify({"message": f"Product '{name}' updated successfully"})

@products_bp.route('/delete/<string:name>', methods=['DELETE'])
def delete_product(name):
    product = Product.query.filter_by(name=name).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product '{name}' deleted successfully"})

@products_bp.route('/location/<string:name>', methods=['GET'])
def get_location_by_name(name):
    product = Product.query.filter_by(name=name).first()
    if product:
        return jsonify({'location': (product.location_x, product.location_y)})
    else:
        return jsonify({"error": "Product not found"}), 404
