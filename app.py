from flask import Flask, render_template, flash, redirect, url_for, request
import sqlite3
import os

app = Flask(__name__)

def global_var(Uname):
    global globalUsername
    globalUsername = Uname
    return globalUsername

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

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
                        return redirect(url_for('createaccountsuccess', globalUsername = username))
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
                    return redirect(url_for('loginsuccess', globalUsername=Uname))
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
