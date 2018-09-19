from app import db
from datetime import datetime

offer_link = db.Table('offer_link',
                      db.Column('product_id', db.Integer,
                                db.ForeignKey('product.product_id')),
                      db.Column('offer_id', db.Integer,
                                db.ForeignKey('offer.offer_id'))
                      )


class Product(db.Model):
    __tablename__ = 'product'

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
    def seed(cls, fake, i):
        product = Product(
            product_code='PROD'+str(i).rjust(6, '0'),
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
    __tablename__ = 'offer'
    offer_id = db.Column(db.Integer, primary_key=True)
    offer_code = db.Column(db.String(20), unique=True, nullable=False)
    offer_name = db.Column(db.String(150), nullable=False)
    offer_desc = db.Column(db.String(255))
    offer_start = db.Column(db.DateTime, nullable=False)
    offer_end = db.Column(db.DateTime, nullable=False)
    products = db.relationship('Product', secondary='offer_link',
                               backref='product', lazy=True)

    def __repr__(self):
        return '<Offer {}>'.format(self.offer_code)

    @classmethod
    def seed(cls, fake, i):
        offer = Offer(
            offer_code='OFFER'+str(i).rjust(6, '0'),
            offer_name=fake.offername_gen(),
            offer_desc=fake.offerdesc_gen(),
            offer_start=datetime.strptime(fake.date(), '%Y-%m-%d'),
            offer_end=datetime.strptime(fake.date(), '%Y-%m-%d')
        )
        offer.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            message = {"message": "Records added"}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = {"message": template.format(type(ex).__name__, ex.args)}
            print(message)
