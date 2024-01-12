from flask import request, jsonify, Blueprint
from backend.models import Product
from backend import db

products_bp = Blueprint('products', __name__)

def init_app(app):
    app.register_blueprint(products_bp, url_prefix='/api/products')

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
