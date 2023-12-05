
import random

from flask import Flask,render_template, request,jsonify,url_for,redirect,session
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
import sqlite3, hashlib, os

from markupsafe import escape
from flask_cors import CORS,cross_origin

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = './static'

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            admin=''
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName,superuser FROM users WHERE email = ?", (session['email'], ))
            userId, firstName,admin = cur.fetchone()
    conn.close()
    return (loggedIn, firstName,admin)


@app.route('/')
def index():
    loggedIn, firstName,admin = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from productos')
        products=cur.fetchall()
    conn.close()
    return render_template('index.html', loggedIn=loggedIn, firstName=firstName,products=products,admin=admin)


import base64
@app.route("/create/<b64>", methods=["GET"])
def webpay_plus_create(b64):
    loggedIn, firstName,admin = getLoginDetails()

    print("Webpay Plus Transaction.create")
    print(b64)
    decoded_base64=int(base64.b64decode(b64))
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = decoded_base64
    return_url = request.url_root + '/commit'
    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }
    
    response = (Transaction()).create(buy_order, session_id, amount, return_url)

    print(response)

    return render_template('create.html', request=create_request, response=response,decodedb64=decoded_base64, loggedIn=loggedIn, firstName=firstName)



@app.route("/commit", methods=["GET"])
def webpay_plus_commit():
    loggedIn, firstName,admin = getLoginDetails()

    token = request.args.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    print("response: {}".format(response))

    return render_template('commit.html', token=token, response=response, loggedIn=loggedIn, firstName=firstName)

@app.route("/commit", methods=["POST"])
def webpay_plus_commit_error():
    loggedIn, firstName,admin = getLoginDetails()

    token = request.form.get("TBK_TOKEN")
    print("commit error for token_ws: {}".format(token))

    #response = Transaction.commit(token=token)
    #print("response: {}".format(response))
    response = {
        "error": "Transacción con errores"
    }

    return render_template('commit.html', token=token, response=response, loggedIn=loggedIn, firstName=firstName)    

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/signUpForm")
def registrationForm():
    return render_template("register.html")


@app.route('/dashboard')
def dashboardForm():
    productCount = 0
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from productos')
        productCount=len(cur.fetchall())
    conn.close()
    loggedIn, firstName,admin = getLoginDetails()
    return render_template("dashboard/index.html",loggedIn=loggedIn,firstName=firstName,productCount=productCount,admin=admin)


@app.route('/dashboard/product/add_product',methods=['POST','GET'])
def addProduct():
    if request.method == 'POST':
        nombre=request.form['nombre']
        precio=request.form['precio']
        descripcion = request.form['descripcion']
        imagen= request.files['imagen']
        nombreImagen= request.files['imagen'].filename
        stock=request.form['stock']
        categoria = request.form['categoria']
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                print(request.form)

                cur.execute('INSERT INTO productos (nombre, precio,descripcion,stock, imagen,categoria) VALUES (?, ?, ?, ?,?,?)', (nombre, precio,descripcion,stock,nombreImagen, categoria))
                con.commit()

                file_name = nombreImagen or ''
                destination = '/'.join([UPLOAD_FOLDER, file_name])
                imagen.save(destination)
                print('ok')


            except:
                print('nok')
                con.rollback()
        con.close()

        return redirect(url_for('dashboardForm'))
    loggedIn, firstName,admin = getLoginDetails()

    return render_template("dashboard/product/product.html",firstName=firstName,admin=admin)

@app.route('/dashboard/product',methods=['POST','GET'])
def products():
    if request.method =='POST':
        prodId=request.form['id']
        print(prodId)
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('delete from productos where idProducto = ?', ( prodId))
                con.commit()
            except:
                print('nok')
                con.rollback()
        con.close()

        return redirect(url_for('products'))

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from productos')
        products=cur.fetchall()
    conn.close()
    print (products)
    loggedIn, firstName,admin = getLoginDetails()

    return render_template("dashboard/product/list.html",products=products,firstName=firstName,admin=admin)

@app.route('/dashboard/users',methods=['GET','POST'])
def users():
    if request.method =='POST':
        userId=request.form['id']
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('delete from users where userId = ?', ( userId))
                con.commit()
            except:
                print('nok')
                con.rollback()
        con.close()

        return redirect(url_for('users'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('select * from users')
        users=cur.fetchall()
        print(users)
    conn.close()
    loggedIn, firstName,admin = getLoginDetails()

    return render_template("dashboard/user/list.html",users=users,firstName=firstName,admin=admin)


@app.route('/dashboard/users/add_user',methods=['POST','GET'])
def addUser():
    if request.method == 'POST':
        print(request.form)
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        if(request.form['admin2'] is None):
            admin = 0
        else:
            admin=1
        print(admin)
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone,superuser) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone,admin))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return redirect(url_for('users'))
    loggedIn, firstName,admin = getLoginDetails()

    return render_template("dashboard/user/detail.html",firstName=firstName,admin=admin)
