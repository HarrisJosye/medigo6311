from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import re
from multiprocessing import Process
import time

app = Flask(__name__)
app.secret_key = 'idontknowitsroleyetbutneedit'
app.config[
    'MONGO_URI'] = 'mongodb+srv://mandeepmandla:IAb8tM0lYpp9j5xJ@cluster0.vspam.mongodb.net/MediGO?retryWrites=true&w=majority'
mongo = PyMongo(app)
LoginDB = mongo.db.Login
SignupDB = mongo.db.SignUp
ngos = mongo.db.NGOlist
modos = mongo.db.MedicineList
AppMedReq = mongo.db.Medicine_Request_Approval
AppDonReq = mongo.db.Medicine_Donation_Approval


@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':

        get_user = LoginDB.find_one({'Username': request.form['username']})
        get_password = LoginDB.find_one({'Password': request.form['password']})
        get_email = LoginDB.find_one({'Email': request.form['username']})

        get_user_type = SignupDB.find_one({"Username": request.form['username']}, {'Category': 1, '_id': 0})
        num = re.sub("\D", "", str(get_user_type))  # To extract category

        print(num)

        if get_user or get_email:
            if get_password:
                print("Login successful")
                return redirect(url_for('index', input=num))
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
        registrationno = request.form.get('NGOReg')
        dob = request.form.get('dob')
        sex = request.form.get('sex')

        user_exist = LoginDB.find_one({'Username': request.form['username']})
        email_exist = LoginDB.find_one({'email': request.form['email']})

        if user_exist or email_exist:
            print("User already exists")
            return redirect(url_for('login_page'))
        if password_1 != password_2:
            print("Password and confirm password doesn't match")
            return redirect(url_for('signup_page'))
        else:
            new_user = (
                {'Username': request.form['username'], 'Email': request.form['email'], 'Password': password_1,
                 'DOB': dob,
                 'Sex': sex,
                 'Category': category, 'Registration Number': registrationno})
            new_user_login = (
                {'Username': request.form['username'], 'Email': request.form['email'], 'Password': password_1})
            SignupDB.insert(new_user)
            LoginDB.insert(new_user_login)

            return redirect(url_for('login_page'))

    return render_template('signup_page.html', userlist=userlist)


@app.route('/index/<input>')
def index(input):
    num = input
    print(input)
    return render_template('indexButton.html', num=num)


@app.route('/complete/<oid>')
def complete(oid):
    try:
        do_item = ngos.find_one({'_id': ObjectId(oid)})
        do_item['complete'] = True
        ngos.save(do_item)
    except:
        do_item = modos.find_one({'_id': ObjectId(oid)})
        do_item['complete'] = True
        modos.save(do_item)
    return redirect(url_for('index'))


@app.route('/ngo_list')
def ngo_list():
    saved_ngos = ngos.find()
    return render_template('ngolist.html', todos=saved_ngos)


@app.route('/med_list')
def med_list():
    saved_modos = modos.find()
    return render_template('ngolist.html', todos=saved_modos)


@app.route('/donate')
def donate():
    return render_template('medicinedonate.html')


@app.route('/add_modo', methods=['POST'])
def add_modo():
    new_modo = request.form.get('new-todo')
    new_todo1 = request.form.get('new-todo1')
    new_todo2 = request.form.get('new-todo2')

    AppDonReq.insert_one({'text': new_modo, 'family': new_todo1, 'ExpDate': new_todo2, 'complete': False})
    return redirect(url_for('index'))


@app.route('/Approve')
def Approve():
    return render_template('Approve_request.html')


@app.route('/App_req')
def App_req():
    Approval_req = AppMedReq.find()
    return render_template('Approval_med_req.html', todos=Approval_req)


@app.route('/App_don')
def App_don():
    Approval_don = AppDonReq.find()
    return render_template('Approval_don_req.html', todos=Approval_don)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
