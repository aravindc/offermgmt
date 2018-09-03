from flask import Flask, jsonify, request, flash, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import secrets
import json
from app.models import Product, Offer

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/product/<string:productcode>', methods=['POST'])
def create_product(productcode):
    product = Product(product_code=productcode)
    db.session.add(product)
    db.session.commit()
    flash('Record Added')
    return jsonify({'message': 'Product code ' + productcode + ' Added'})


@app.route('/offer/<string:offercode>', methods=['POST'])
def create_offer(offercode):
    offer = Offer(offer_code=offercode)
    db.session.add(offer)
    db.session.commit()
    flash('Record Added')
    return jsonify({'message': 'Offer code ' + offercode + ' Added'})


@app.route('/products')
def show_all_products():
    return render_template('show_all_products.html', products=Product.query.all())


@app.route('/offerasso', methods=['POST'])
def offer_to_product():
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    for jsonObj in jsonObjs:
        offer = Offer.query.filter(Offer.offer_code == jsonObj['offercode']).first()
        if offer is None:
            abort(400)
        for products in jsonObj['productcode']:
            product = Product.query.filter(Product.product_code == products).first()
            product.offers.append(offer)
            db.session.add(product)
            db.session.commit()
    return jsonify({'message': 'Offer to Product associated'})


@app.route('/offers')
def show_all_offers():
    all_offer_product = []
    offers = Offer.query.all()
    for offer in offers:
        offer_product = {}
        offer_product['offer_code'] = offer.offer_code
        offer_product['product_code'] = []
        for product in offer.products:
            offer_product['product_code'].append(product.product_code)
        all_offer_product.append(offer_product)
    print(all_offer_product)
    # return render_template('show_all_offers.html', offers=Offer.query.all())
    return jsonify(all_offer_product)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(Product(product_code='PROD001'))
    db.session.add(Product(product_code='PROD002'))
    db.session.add(Product(product_code='PROD003'))
    db.session.add(Product(product_code='PROD004'))
    db.session.add(Product(product_code='PROD005'))
    db.session.add(Offer(offer_code='OFFER001'))
    db.session.add(Offer(offer_code='OFFER002'))
    db.session.add(Offer(offer_code='OFFER003'))
    db.session.commit()
    app.run(debug=True)