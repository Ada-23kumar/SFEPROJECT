from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector   # type: ignore
import sys
import os


app = Flask(__name__)
app.secret_key=os.urandom(24) 

try:
    conn = mysql.connector.connect(host = "localhost", user = "root", password = "", database= "SFE_PROJECT")

    curser = conn.cursor()
except:
    print("Error")
    sys.exit()
else:
    print("Connected")


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
    curser.execute("""
        SELECT * FROM User_login WHERE email LIKE '{}' AND password LIKE '{}';
        """.format(email, password))
    
    user = curser.fetchall()
    if len(user) > 0:
        session['id'] = user[0][0]
        return redirect('/user')
    else:
        return redirect('/sign_in')

@app.route('/sign_up')
def sign_up():
    return render_template('signup.html')


@app.route('/register_validation', methods=['POST'])
def register_validation():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    curser.execute("""
                   INSERT INTO User_login (name, email, password) VALUES ('{}', '{}', '{}
                   ');
                   """.format(name, email, password))
    conn.commit()

    curser.execute("""
        SELECT * FROM User_login WHERE email LIKE '{}' AND password LIKE '{}'""".format(email, password))
    myuser = curser.fetchall()
    return redirect('/sign_in')






@app.route('/user')
def user():
    if'id' in session:
        return render_template('userlogin.html')
    else:
        return redirect('/sign_in')
    
    
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
    session.pop('id')
    return redirect('/')








if __name__ == "__main__":
    app.run(debug = True)