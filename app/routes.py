from flask import jsonify, flash, request, abort
from app import db
from app.models import Product, Offer
from app import app
import json


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
    all_products = []
    products = Product.query.all()
    for product in products:
        all_products.append(product)
    return jsonify(all_products)


@app.route('/offerasso', methods=['POST'])
def offer_to_product():
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    for jsonObj in jsonObjs:
        offer = Offer.query.filter(Offer.offer_code ==
                                   jsonObj['offercode']).first()
        if offer is None:
            abort(400)
        for products in jsonObj['productcode']:
            product = Product.query.filter(Product.product_code ==
                                           products).first()
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
    return jsonify(all_offer_product)
