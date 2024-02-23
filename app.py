from flask import Flask, render_template, flash, redirect, url_for, request, session, make_response, jsonify
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] =[os.urandom(24)]


def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername


@app.route('/')
def index():
    cookie = request.cookies.get('userID')
    if cookie != "":
        resp = make_response(render_template('logoutcookie.html'))
        resp.set_cookie('userID', "")
        return resp
    else:
        return render_template('index.html')

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    try:
        cookie = request.cookies.get('userID')  # get the cookie
        database = r"userdatabase.db"  # database file
        conn = None
        conn = sqlite3.connect(database)  # connecting to the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (cookie,))  # querying the database
        user = cur.fetchall()
        cur.close()
    except IndexError:
        flash('Error')
    name = request.cookies.get('userID')  # get the cookie
    data = name
    return render_template('userpage.html', data=data)


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        administrator = "No"
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"userdatabase.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                #cur = mysql.connection.cursor()
                #cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ?', (username,))
                user = cur.fetchall()
                cur.close()
                if user:
                    flash('Username already exists!')
                else:
                    if password != confirmPassword:
                        flash('Passwords do not match!')
                    else:
                        cur = conn.cursor()
                        cur.execute('INSERT INTO users VALUES(?, ?, ?)', (username, password, administrator))
                        conn.commit()
                        cur.close()
                        resp = make_response(
                        render_template('readcookie.html'))  # setting the cookie connected to the username
                        resp.set_cookie('userID', username)
                        return resp
            except IndexError:
                flash('Username or Password is incorrect!')
    return render_template('createaccount.html')


@app.route('/login' , methods=['GET', 'POST'])
def login():
    # globalAttempt = global_var2(attempt=3)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            try:
                database = r"userdatabase.db"
                conn = None
                conn = sqlite3.connect(database)
                cur = conn.cursor()
                # cur = mysql.connection.cursor()
                # cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user = cur.fetchall()
                cur.close()
                User = user[0]
                Uname = User[0]
                Pword = User[1]
                if Uname == username and Pword == password:
                    global_var(Uname)
                    resp = make_response(render_template('readcookie.html'))
                    resp.set_cookie('userID', Uname)  # setting the cookie connected to the username
                    return resp
                else:
                    # globalAttempt = global_var2(globalAttempt)
                    flash('Username or Password is incorrect!')
                    # print(globalAttempt)
            except IndexError:
                # globalAttempt = global_var2(globalAttempt)

                flash('Username or Password is incorrect!')
                # print(globalAttempt)
    return render_template('login.html')


@app.route('/loginscucess/<globalUsername>')
def loginsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('loginsuccess.html', globalUsername = globalUsername)


@app.route('/createaccountsuccess/<globalUsername>')
def createaccountsuccess(globalUsername):
    globalUsername = globalUsername
    return render_template('createaccountsuccess.html', globalUsername = globalUsername)


@app.route('/logout')
def logout():
    return render_template('logout.html')


if __name__ == '__main__':
    app.run()
