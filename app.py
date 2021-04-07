from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, send
import sqlite3, hashlib

app = Flask("__name__")
app.config['SECRET_KEY'] = 'mysecret'


socketio = SocketIO(app)
ROOMS = set()

section = []
# listening for a message event
@socketio.on('message')
def handle_message(data):
    # when message is received then broadcast to all clients that are connected
    send(data, broadcast=True)
    # send((data.username,data.msg))
    section.append(data['username'])
    for i in section:
        conn = sqlite3.connect("database1.db")
        c = conn.cursor()
        c.execute('INSERT INTO kart (name) VALUES (?)', (i,))
        conn.commit()
        conn.close()


@socketio.on('new_room')
def new_room(data):
    ROOMS.add(data['new_room_name'])


@app.route('/')
def welcome():
    return render_template("welcome.html")


@app.route('/home1', methods=['GET','POST'])
def home1():
    customer_in_session = []

    if request.method == 'POST':
        # receiving option chosen from client
        section = str(request.form.get('opt1'))

        # converting it into a list section user name and product chosen for that user
        prod_name = section.split(',')

        con = sqlite3.connect('database1.db')
        cur = con.cursor()

        # getting the corresponding image url fro the products table
        cur.execute('SELECT img FROM products WHERE name="'+prod_name[1]+'"')
        image = cur.fetchone()

        # updating name corresponding product and corresponding image url into kart..this information will be used while creating sections
        cur.execute('UPDATE kart SET prod_name="'+prod_name[1]+'",prod_img="'+str(image)[2:-3]+'" WHERE name="'+prod_name[0]+'"')

        con.commit()
        con.close()

    con = sqlite3.connect('database1.db')
    cur = con.cursor()

    # sending products to client to display and names for creating options in the dropdown
    cur.execute('SELECT * FROM products')
    itemData = cur.fetchall()
    cur.execute('SELECT name FROM kart')
    data = cur.fetchall()

    for i in data:
        customer_in_session.append(str(i)[2:-3])
    customer_in_session = set(customer_in_session)

    username = request.args.get('username', None)
    return render_template("home1.html", username=username, rooms=list(ROOMS), itemData=itemData, customer_in_session=customer_in_session  )


@app.route('/login', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('database1.db')
        cur = con.cursor()
        cur.execute('SELECT username, password FROM users')
        data = cur.fetchall()

        # checks if the credentials match with the database
        for row in data:
            if row[0] == username and row[1] == hashlib.md5(password.encode()).hexdigest():
                session["username"] = username
                return redirect(url_for('home1', username=username) )
            else:
                error = 'Invalid Credentials. Please try again.'
            
    return render_template("login.html", error=error)


# page for registeration
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        if request.form['username'] != "" and request.form['password'] != "":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form['email']
            phone = request.form['phone']
            conn = sqlite3.connect("database1.db")
            c = conn.cursor()
            c.execute('INSERT INTO users (password, email, username, phone) VALUES (?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, username, phone))
            conn.commit()
            conn.close()
            return redirect(url_for('login') )

    return render_template("register.html")



@app.route('/cart')
def cart():
    # maintains list for users to be displayed in group cart
    customer_in_session = []

    con = sqlite3.connect('database1.db')
    cur = con.cursor()
    cur.execute('SELECT name FROM kart')
    data = cur.fetchall()
    cur.execute('SELECT * FROM kart')

    # maintaining a list of name,product name and image url
    testing = cur.fetchall()
    length = len(testing)

    # testing = [['Rohan Mehta', 'Grey Sweater', '/static/pics_1.jpg'],['Alex Simpson', 'Black Top', '/static/pics2.jpg'],['Marishka Menon', 'Kurti', '/static/pic3.jpg']]
    
    for i in data:
        customer_in_session.append(str(i)[2:-3])
    

    return render_template("cart.html", customer_in_session = customer_in_session, testing=testing, length=length )

if __name__ == "__main__":
    socketio.run(app, debug=True)