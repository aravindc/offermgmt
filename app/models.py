from app import db

offer_link = db.Table('offer_link',
                      db.Column('product_id', db.Integer,
                                db.ForeignKey('product.product_id')),
                      db.Column('offer_id', db.Integer,
                                db.ForeignKey('offer.offer_id'))
                      )


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), unique=True)
    product_desc = db.Column(db.String(255), nullable=False)
    product_image_url_s = db.Column(db.String(255))
    product_image_url_m = db.Column(db.String(255))
    product_image_url_l = db.Column(db.String(255))
    product_url = db.Column(db.String(20))

    def __repr__(self):
        return '<Product {}>'.format(self.product_code)


class Offer(db.Model):
    offer_id = db.Column(db.Integer, primary_key=True)
    offer_code = db.Column(db.String(20), unique=True)
    offer_desc = db.Column(db.String(255), nullable=False)
    offer_start = db.Column(db.DateTime)
    offer_end = db.Column(db.DateTime)
    products = db.relationship('Product', secondary='offer_link',
                               backref='product', lazy=True)

    def __repr__(self):
        return '<Offer {}>'.format(self.offer_code)
