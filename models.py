from app import db

class Customer(db.Model):
    __tablename__ = "customer"
    custid = db.Column(db.Integer, primary_key=True) 
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    username = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(20),unique=True)

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

class Grpchat(db.Model):
    __tablename__ = "grpchat"
    grpid = db.Column(db.Integer, primary_key=True) 
    hostid = db.Column(db.String(20),db.ForeignKey('customer.custid'))
    memberid = db.Column(db.String(20),db.ForeignKey('customer.custid'),unique=True)

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column('product_id',db.String(20),primary_key=True)
    product_name=db.Column('product_name',db.String(20))
    product_url = db.Column(db.String(20))

class Grpcart(db.Model):
    __tablename__ = "grpcart"
    # __table_args__ = (
    #     # PrimaryKeyConstraint('grpchat.hostid', 'grpchat.hostid'),
    #     extend_existing=True
    # )
    id=db.Column('cart_id',db.Integer,autoincrement = True,primary_key=True)
    # id = db.Column(db.String(20),db.ForeignKey('product.id'))
    hostid = db.Column(db.String(20))
    sectionid = db.Column(db.String(20))
    # product_name = db.Column(db.String(20),db.ForeignKey('product.product_name'))
    product_name = db.Column(db.String(20))
    product_img = db.Column(db.String(20))

    @staticmethod
    def update(sectionid, **kwargs):
        grpcart = Grpcart.query.filter_by(sectionid=sectionid).first()
        print(kwargs)
        for key, value in kwargs.items():
            setattr(grpcart, key, value) 

        print(grpcart.__dict__)
        db.session.commit()

# class Grpcart(db.Model):
#     __tablename__ = "grpcart"
#     # __table_args__ = (
#     #     # PrimaryKeyConstraint('grpchat.hostid', 'grpchat.hostid'),
#     #     extend_existing=True
#     # )
#     id = db.Column(db.String(20),db.ForeignKey('product.id'))
#     cartid = db.Column(db.String(20),db.ForeignKey('customer.custid'))
#     sectionid = db.Column(db.String(20))
#     # product_name = db.Column(db.String(20),db.ForeignKey('product.product_name'))
#     product_name = db.Column(db.String(20))
#     product_img = db.Column(db.String(20))


