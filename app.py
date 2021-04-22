from flask import Flask, render_template, request,session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from models import *
import hashlib
from flask_socketio import SocketIO, send, emit, join_room


app = Flask("__name__")

app.secret_key = 'secret@123'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\manavi\\Desktop\\python\\myn\\myn.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        # receiving option chosen from client
        section = str(request.form.get('opt1'))

        # converting it into a list section user name and product chosen for that user
        prod_name = section.split(',')
        print(prod_name[1])
        
        prod_name.append([Product.query.all()[i].product_url for i in range(len(Product.query.all())) if Product.query.all()[i].product_name==prod_name[1]])

        
        prod_name.append([Grpchat.query.all()[i].hostid for i in range(len(Grpchat.query.all()))][0])
        # print(type(prod_name[0]))

        # [grpchat.query.all()[].hostid][0]
        if len(Grpcart.query.all()) == 3:
            Grpcart.update(str(prod_name[0]),product_name=str(prod_name[1],),product_img=str(prod_name[2]))
            # Grpcart.query.filter_by(sectionid=str(prod_name[0])).update(product_name=str(prod_name[1]))

            # Grpcart.query.filter_by(sectionid=str(prod_name[0])).update(product_img=str(prod_name[2]))
            # db.session.commit()
        else:
            grpcart = Grpcart(sectionid=str(prod_name[0]),product_name=str(prod_name[1]),product_img=str(prod_name[2]),hostid=str(prod_name[3]))
            db.session.add(grpcart)
            db.session.commit()


    prodname = [Product.query.all()[i].product_name for i in range(len(Product.query.all()))]

    prod_id = [Product.query.all()[i].id for i in range(len(Product.query.all()))]

    room = [Grpchat.query.all()[i].hostid for i in range(len(Grpchat.query.all()))]

    members = [Grpchat.query.all()[i].memberid for i in range(len(Grpchat.query.all()))]
    # print(room)

    return render_template('home.html', prodname = prodname, prod_id=prod_id,room = room[0], members = members)

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        hashed_pswd = hashlib.md5(password.encode()).hexdigest()

        user = Customer(fname=fname, lname=lname, username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['username']
        ulist = [Customer.query.all()[i].username for i in range(len(Customer.query.all()))]
        if u in ulist:
            z = Customer.query.filter_by(username=u).all()[0].password
            if(hashlib.md5(request.form['password'].encode()).hexdigest()!=z):
                error = 'Invalid'
            else:
                session['username']=u
                return redirect(url_for('home'))
        error = 'Invalid'
    return render_template('login.html', error=error)

@app.route("/cart")
def cart():
    sections = [Grpcart.query.all()[i].sectionid for i in range(len(Grpcart.query.all()))]
    prod = [Grpcart.query.all()[i].product_name for i in range(len(Grpcart.query.all()))]
    img = [Grpcart.query.all()[i].product_img for i in range(len(Grpcart.query.all()))]
    print(img[0])
    # print(testing)
    return render_template('cart.html',length=3,sections=sections,prod=prod,img=img)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('welcome'))

@socketio.on('message')
def handle_message(data):
    # send({'msg': data['msg'], 'username': data['username'], 'room': data['room'] })
    send(data, broadcast=True)
    print(data)
    grp = Grpchat(hostid=data["room"], memberid=data["username"])
    db.session.add(grp)
    db.session.commit()


@socketio.on('new_room')
def new_room(data):
    room = data['room']
    host = data['username']
    print(data)

    grp = Grpchat(hostid=host, memberid=host)
    db.session.add(grp)
    db.session.commit()

@socketio.on('join')
def join(data):
    """User joins a room"""
    username = data["username"] 
    
    join_room(data["room"])
    

    grp = Grpchat(hostid=data["room"], memberid=username)


if __name__ == "__main__":
    socketio.run(app, debug=True)



