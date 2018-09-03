from flask import jsonify, flash, request, abort, render_template
from app import db
from app.models import Product, Offer
from app import app
import json


@app.route('/')
def index():
    return render_template("index.html")


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


@app.route('/offerasso', methods=['POST'])
def offer_to_product():
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    for jsonObj in jsonObjs:
        offer = Offer.query.filter(Offer.offer_code ==
                                   jsonObj['offercode']).first()
        print(offer)
        if offer is None:
            abort(400)
        for products in jsonObj['productcode']:
            product = Product.query.filter(Product.product_code ==
                                           products).first()
            offer.products.append(product)
            db.session.add(offer)
            db.session.commit()
    return jsonify({'message': 'Offer to Product associated'})


@app.route('/offers')
def show_all_offers():
    all_offer_product = []
    offers = Offer.query.all()
    for offer in offers:
        offer_product = row2dict(offer)
        offer_product['product'] = []
        for product in offer.products:
            offer_product['product'].append(row2dict(product))
        all_offer_product.append(offer_product)
    return jsonify(all_offer_product)


@app.route('/products')
def show_all_products():
    all_products = []
    products = Product.query.all()
    for product in products:
        all_products.append(row2dict(product))
    return jsonify(all_products)


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
