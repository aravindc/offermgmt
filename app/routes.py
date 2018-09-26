from flask import jsonify, request, abort, render_template
from faker import Faker
from app import db
from app.providers import MyProvider
from app.models import Product, Offer
from app import app
import json
from datetime import datetime


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/populatedb', methods=['POST'])
def populate_db():
    if not request.json:
        abort(400)
    jsonObj = json.loads(request.data)
    fake = Faker()
    fake.add_provider(MyProvider)
    if jsonObj['append'] == "False":
        try:
            db.session.query(Product).delete()
            db.session.query(Offer).delete()
            db.session.commit()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = {"message": template.format(type(ex).__name__, ex.args)}
    for i in range(jsonObj['ProdCount']):
        Product.seed(fake, i+1)
    for j in range(jsonObj['OfferCount']):
        Offer.seed(fake, j+1)
    orows = db.session.query(Offer).count()
    prows = db.session.query(Product).count()
    message = {
        "message":
        "Product table has {0} records and Offer table has {1} records"
        .format(prows, orows)}
    return jsonify(message)


@app.route('/product', methods=['POST'])
def create_product():
    message = {"message": ""}
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
    try:
        db.session.commit()
        message = {"message": "Records added"}
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = {"message": template.format(type(ex).__name__, ex.args)}
    return jsonify(message)


@app.route('/offer', methods=['POST'])
def create_offer():
    message = {"message": ""}
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
    try:
        db.session.commit()
        message = {"message": "Records added"}
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = {"message": template.format(type(ex).__name__, ex.args)}
    return jsonify(message)


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


@app.route('/hiefulltree', methods=['GET'])
def get_hie_data():
    prod_tree = []
    lvl1s = db.session.query(Product.product_lvl1).order_by(
                             Product.product_lvl1).distinct().all()
    for lvl1 in lvl1s:
        lvl1unit = {lvl1[0]: []}
        lvl2s = db.session.query(Product.product_lvl2).filter(
                                 Product.product_lvl1 == lvl1[0]
                                 ).order_by(
                                 Product.product_lvl2
                                 ).distinct().all()
        for lvl2 in lvl2s:
            lvl2unit = {lvl2[0]: []}
            lvl3s = db.session.query(Product.product_lvl3).filter(
                                     Product.product_lvl2 == lvl2[0],
                                     Product.product_lvl1 == lvl1[0]
                                     ).order_by(
                                     Product.product_lvl3
                                     ).distinct().all()
            for lvl3 in lvl3s:
                lvl3unit = {lvl3[0]: []}
                lvl4s = db.session.query(Product.product_lvl4).filter(
                                         Product.product_lvl3 == lvl3[0],
                                         Product.product_lvl2 == lvl2[0],
                                         Product.product_lvl1 == lvl1[0]
                                         ).order_by(
                                         Product.product_lvl4
                                         ).distinct().all()
                for lvl4 in lvl4s:
                    lvl4unit = {lvl4[0]: []}
                    lvl5s = db.session.query(Product.product_lvl5).filter(
                                             Product.product_lvl4 == lvl4[0],
                                             Product.product_lvl3 == lvl3[0],
                                             Product.product_lvl2 == lvl2[0],
                                             Product.product_lvl1 == lvl1[0]
                                             ).order_by(
                                             Product.product_lvl5
                                             ).distinct().all()
                    for lvl5 in lvl5s:
                        lvl5unit = {lvl5[0]: []}
                        prodcodes = db.session.query(
                                     Product.product_code).filter(
                                     Product.product_lvl5 == lvl5[0],
                                     Product.product_lvl4 == lvl4[0],
                                     Product.product_lvl3 == lvl3[0],
                                     Product.product_lvl2 == lvl2[0],
                                     Product.product_lvl1 == lvl1[0]
                                     ).order_by(
                                     Product.product_code
                                     ).distinct().all()
                        if prodcodes is not None:
                            for prodcode in prodcodes:
                                lvl5unit[lvl5[0]].append(prodcode[0])
                        lvl4unit[lvl4[0]].append(lvl5unit)
                    lvl3unit[lvl3[0]].append(lvl4unit)
                lvl2unit[lvl2[0]].append(lvl3unit)
            lvl1unit[lvl1[0]].append(lvl2unit)
        prod_tree.append(lvl1unit)
    return jsonify(prod_tree)


@app.route('/getprodlevel/<int:level>', methods=['POST'])
def getProdLevel(level):
    prodLevel = []
    if not request.json:
        abort(400)
    jsonObjs = json.loads(request.data)
    if level == 1:
        lvls = db.session.query(Product.product_lvl1).order_by(
            Product.product_lvl1).distinct().all()
    elif level == 2:
        lvls = db.session.query(Product.product_lvl2).filter(
            Product.product_lvl1 == jsonObjs["level1"]).order_by(Product.product_lvl2
            ).distinct().all()
    elif level == 3:
        lvls = db.session.query(Product.product_lvl3).filter(
            Product.product_lvl2 == jsonObjs["level2"], 
            Product.product_lvl1 == jsonObjs["level1"]
            ).order_by(Product.product_lvl3).distinct().all()
    elif level == 4:
        lvls = db.session.query(Product.product_lvl4).filter(
            Product.product_lvl3 == jsonObjs["level3"],
            Product.product_lvl2 == jsonObjs["level2"],
            Product.product_lvl1 == jsonObjs["level1"]
        ).order_by(
            Product.product_lvl4
        ).distinct().all()
    elif level == 5:
        lvls = db.session.query(Product.product_lvl5).filter(
            Product.product_lvl4 == jsonObjs["level4"],
            Product.product_lvl3 == jsonObjs["level3"],
            Product.product_lvl2 == jsonObjs["level2"],
            Product.product_lvl1 == jsonObjs["level1"]
        ).order_by(
            Product.product_lvl5
        ).distinct().all()
    elif level == 6:
        lvls = db.session.query(Product.product_code).filter(
            Product.product_lvl5 == jsonObjs["level5"],
            Product.product_lvl4 == jsonObjs["level4"],
            Product.product_lvl3 == jsonObjs["level3"],
            Product.product_lvl2 == jsonObjs["level2"],
            Product.product_lvl1 == jsonObjs["level1"]
        ).order_by(
            Product.product_code
        ).distinct().all()
    for lvl in lvls:
        prodLevel.append(lvl[0])
    return jsonify(prodLevel)


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
