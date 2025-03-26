from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector   # type: ignore
import sys
import os


app = Flask(__name__)
app.secret_key=os.urandom(24) 

try:
    conn = mysql.connector.connect(host = "localhost", user = "root", password = "", database= "excelPro")

    curser = conn.cursor(dictionary=True)
    print("Connected to Database")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    # sys.exit()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ScrapRate')
def scraprate():
    return render_template('ScrapRate.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="excelPro")
    curser = conn.cursor(dictionary=True)

    curser.execute("SELECT * FROM User_login WHERE email = %s AND password = %s", (email, password))
    user = curser.fetchone()  # Use fetchone() instead of fetchall()

    conn.close()  # Close connection after query execution

    if user:
        session['id'] = user['User_id']
        session['name'] = user['name']
        return redirect(url_for('user', name=user['name']))
    else:
        flash("Invalid email or password!", "danger")
        return redirect('/sign_in')


@app.route('/sign_up')
def sign_up():
    return render_template('signup.html')


@app.route('/register_validation', methods=['POST'])
def register_validation():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="excelPro")
    curser = conn.cursor(dictionary=True)

    curser.execute("INSERT INTO User_login (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()

    # Retrieve newly registered user
    curser.execute("SELECT * FROM User_login WHERE email = %s AND password = %s", (email, password))
    myuser = curser.fetchone()

    conn.close()

    if myuser:
        session['id'] = myuser['User_id']
        session['name'] = myuser['name']
        return redirect(url_for('user', name=myuser['name']))

    flash("Registration successful! Please log in.", "success")
    return redirect('/sign_in')






@app.route('/user/<name>')
def user(name):
    # name = curser.execute("""SELECT * User_login WHERE name """)
    if 'id' not in session:
        return redirect('/sign_in')

    return render_template('userlogin.html', name=name)
    
    
    # return render_template('userlogin.html')




@app.route('/submit_pickup', methods=['POST'])
def submit_pickup():
    # if 'id' not in session:
    #     return redirect(url_for('sign_in'))

    # Get the form data
    address = request.form['address']
    phone = request.form['phone']
    pincode = request.form['pincode']
    quantity = request.form['quantity']
    garbage_type = request.form['garbageType']
    user_id = session['id']  # Get the user ID from the session

    # Insert into database
    # cursor = conn.cursor()
    curser.execute ("""INSERT INTO garbage_pickup (address, phone, pincode, quantity, garbage_type, user_id)
               VALUES ('{}', '{}', '{}', '{}', '{}', '{}');""".format(address, phone, pincode, quantity, garbage_type, user_id))
    # cursor.execute(query, (address, phone, pincode, quantity, garbage_type, user_id))
    conn.commit()

    return "Pickup request submitted successfully!"

@app.route('/logout')
def logout():
    session.pop('id', None)  # Avoid KeyError by providing a default value
    return redirect('/')

@app.route('/delevery')
def delevery():
    return render_template('delevery.html')


@app.route('/auther')
def auther():
    return render_template('auther.html')






if __name__ == "__main__":
    app.run(debug = True)