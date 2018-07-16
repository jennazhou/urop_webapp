# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, flash, render_template, request, redirect, session, url_for
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.html5 import IntegerField, EmailField
from passlib.hash import sha256_crypt
import user_database as u_db
import os
import sqlite3
import question_database as qn_db

app = Flask(__name__)

'''
Problems yet to be solved:
   - the duration of session
   - logout 
   - homepage design
'''

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    try:
#   if request.form['password'] == 'password' and request.form['username'] == 'admin':
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            #all_users  # this is the encrypted password stored in the database
            #the data retrieved from the database is presented in a tuple, therefore need an index to index the number
            if sha256_crypt.verify(password, u_db.psw_retrieval(username)[0]): 
                session['logged_in'] = True;
                session['username'] = username;
                return redirect(url_for('home'))
            else:
                error = "The username or/and password is wrong. Please try again."
        return render_template('login.html', error=error)    
    
    except Exception as e:
        error = "The username or/and password is wrong. Please try again."
        return render_template('login.html', error=error)

#Cannot import class from another customised module. Can only use your own module
class RegistrationForm(Form):
    email = EmailField('E-mail Address', [
        validators.Length(min=6, max=50),
        validators.Required(),
        validators.Email(message='Please enter a valid email address')
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Your passwords do not match!')
        ]) #message is printed when the password doesnt not match the confirmation password
    confirm = PasswordField('Confirm Password' )
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100, message='Please enter a valid age')])
    birth_cty = TextField('Country of Birth', [validators.Length(min=1, max=30)])
    res_cty = TextField('Country of Residence', [validators.Length(min=1, max=30)])


@app.route('/register', methods=['GET','POST'])
def do_admin_register():
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data
            if u_db.psw_retrieval(email) != None:
                error = "That E-mail adress is already taken"
                return render_template('register_short.html', form=form, error=error)
            else:
                password = sha256_crypt.encrypt((str(form.password.data)))
                age = form.age.data
                birth_country = form.birth_cty.data
                residence_country = form.res_cty.data
                u_db.create_table()
                u_db.data_entry(email, password, age, birth_country, residence_country)
                session['logged_in'] = True
                session['username'] = email
                return redirect(url_for('home'))
        else:
            return render_template('register_short.html', form=form)


@app.route('/test')
def test():
    return render_template('sample.html')

allquestions = qn_db.qn_retrieval(1)

@app.route('/question/<max_qn>/<qn>', methods=['GET', 'POST'])
def question(qn, max_qn):
    if request.method == 'GET':
        return render_template('mindmap.html', question_id = qn, tuple_of_qn = allquestions[int(qn)-1])
    if request.method == 'POST':
        #return "submitted"
        car = request.form.get("cars")
        conn = sqlite3.connect('users.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
        c = conn.cursor()
        c.execute("INSERT INTO users (user_input) VALUES(?)", (car))
        conn.commit() #always commit when making modifications, eg. inputing data
        c.close()
        conn.close()
        current_qn = int(qn) + 1
        if current_qn == max_qn:
            return ("You are done!")
        return redirect('/question/' + str(max_qn)+'/' + str(current_qn))

if __name__ == "__main__":
    app.secret_key = os.urandom(12) #need this for session to work
    app.run(debug=True, port=4000)
