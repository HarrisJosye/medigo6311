from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from multiprocessing import Process
import time

app = Flask(__name__)
app.secret_key = 'idontknowitsroleyetbutneedit'
app.config[
    'MONGO_URI'] = 'mongodb+srv://mandeepmandla:IAb8tM0lYpp9j5xJ@cluster0.vspam.mongodb.net/MediGO?retryWrites=true&w=majority'
mongo = PyMongo(app)
LoginDB = mongo.db.Login
SignupDB = mongo.db.SignUp


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':

        get_user = LoginDB.find_one({'Username': request.form['username']})
        get_password = LoginDB.find_one({'Password': request.form['password']})
        get_email = LoginDB.find_one({'Email': request.form['username']})

        if get_user or get_email:
            if get_password:
                print("Login successful")
                return redirect(url_for('welcome_page'))
        else:
            print("Username or password incorrect.")
            return redirect(url_for('login_page'))

    return render_template('login_page.html')


@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    userlist = [{'type': 'New user'}, {'type': 'New NGO'}]
    if "username" in session:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        password_1 = request.form.get("password")
        password_2 = request.form.get("confirmpassword")

        category = request.form.get('category')

        user_exist = LoginDB.find_one({'Username': request.form['username']})
        email_exist = LoginDB.find_one({'email': request.form['email']})

        if user_exist or email_exist:
            print("User already exists")
            return redirect(url_for('login_page'))
        if password_1 != password_2:
            print("Password and confirm password doesn't match")
            return redirect(url_for('signup_page'))
        else:
            new_user = ({'Username': request.form['username'], 'Email': request.form['email'], 'Password': password_1,
                         'Category': category})
            new_user_login = (
                {'Username': request.form['username'], 'Email': request.form['email'], 'Password': password_1})
            SignupDB.insert(new_user)
            LoginDB.insert(new_user_login)

            return redirect(url_for('welcome_page'))

    return render_template('signup_page.html', userlist=userlist)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
