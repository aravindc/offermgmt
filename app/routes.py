from flask import jsonify, request, abort, render_template
from app import db
from app.models import Product, Offer
from app import app
import json
from datetime import datetime


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/product', methods=['POST'])
def create_product():
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    for jsonObj in jsonObjs:
        db.session.add(Product(
            product_code=jsonObj['product_code'],
            product_desc=jsonObj['product_desc'],
            product_image_url_s=jsonObj['product_image_url_s'],
            product_image_url_m=jsonObj['product_image_url_m'],
            product_image_url_l=jsonObj['product_image_url_l'],
            product_url=jsonObj['product_url'],
            product_lvl1=jsonObj['product_lvl1'],
            product_lvl2=jsonObj['product_lvl2'],
            product_lvl3=jsonObj['product_lvl3'],
            product_lvl4=jsonObj['product_lvl4'],
            product_lvl5=jsonObj['product_lvl5'])
        )
    db.session.commit()
    return jsonify({'message': 'Product Added'})


@app.route('/offer', methods=['POST'])
def create_offer():
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    for jsonObj in jsonObjs:
        db.session.add(Offer(
            offer_code=jsonObj['offer_code'],
            offer_desc=jsonObj['offer_desc'],
            offer_start=datetime.strptime(jsonObj['offer_start'], '%Y-%m-%d'),
            offer_end=datetime.strptime(jsonObj['offer_end'], '%Y-%m-%d')
        ))
    db.session.commit()
    return jsonify({'message': 'Offer Added'})


@app.route('/hietree', methods=['GET'])
def get_hie_data():
    level_no = 0
    output = []
    if level_no == 0:
        for test in db.session.query(Product.product_lvl1).distinct():
            output.append(test.product_lvl1)
    return jsonify(output)


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
