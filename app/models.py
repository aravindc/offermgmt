from app import db
from datetime import datetime

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
    product_url = db.Column(db.String(50))
    product_lvl1 = db.Column(db.String(50))
    product_lvl2 = db.Column(db.String(50))
    product_lvl3 = db.Column(db.String(50))
    product_lvl4 = db.Column(db.String(50))
    product_lvl5 = db.Column(db.String(50))

    def __repr__(self):
        return '<Product {}>'.format(self.product_code)

    @classmethod
    def seed(cls, fake):
        product = Product(
            product_code=fake.prodcode_gen(),
            product_desc=fake.proddesc_gen(),
            product_image_url_s=fake.image_url(width=90, height=90),
            product_image_url_m=fake.image_url(width=150, height=150),
            product_image_url_l=fake.image_url(width=250, height=250),
            product_url=fake.url(),
            product_lvl1=fake.lvl1_gen(),
            product_lvl2=fake.lvl2_gen(),
            product_lvl3=fake.lvl3_gen(),
            product_lvl4=fake.lvl4_gen(),
            product_lvl5=fake.lvl5_gen()
        )
        product.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


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

    @classmethod
    def seed(cls, fake):
        offer = Offer(
            offer_code=fake.offercode_gen(),
            offer_desc=fake.offerdesc_gen(),
            offer_start=datetime.strptime(fake.date(), '%Y-%m-%d'),
            offer_end=datetime.strptime(fake.date(), '%Y-%m-%d')
        )
        offer.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
