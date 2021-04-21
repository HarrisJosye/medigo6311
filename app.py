from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import re

app = Flask(__name__)
app.secret_key = 'idontknowitsroleyetbutneedit'
app.config['MONGO_URI'] = 'mongodb+srv://mandeepmandla:IAb8tM0lYpp9j5xJ@cluster0.vspam.mongodb.net/MediGO?retryWrites=true&w=majority'
mongo = PyMongo(app)
LoginDB = mongo.db.Login
SignupDB = mongo.db.SignUp
ngos = mongo.db.NGOlist
modos = mongo.db.MedicineList
AppMedReq = mongo.db.Medicine_Request_Approval
AppDonReq = mongo.db.Medicine_Donation_Approval
Notification = mongo.db.Notification

global num
global uid
global ngoid
global medicine_name

@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')


@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    global num, ngoID
    global uid
    if request.method == 'POST':

        get_user = LoginDB.find_one({'Username': request.form['username']})
        get_password = LoginDB.find_one({'Password': request.form['password']})
        get_email = LoginDB.find_one({'Email': request.form['username']})
        get_uid = SignupDB.find_one({'Username': request.form['username']})
        get_user_type = SignupDB.find_one({"Username": request.form['username']}, {'Category': 1, '_id': 0})
        num = re.sub("\D", "", str(get_user_type))  # To extract category
        uid = get_uid['_id']
        print(uid)
        print(num)

        if num == '2':
            get_user_NGOID = SignupDB.find_one({"Username": request.form['username']}, {'ngoID': 1, '_id': 0})
            str_user_NGOID = str(get_user_NGOID)
            ngoID = str_user_NGOID[11:13]
            print(ngoID)

        if get_user or get_email:
            if get_password:
                return redirect(url_for('index', input=num))
        else:
            print("Username or password incorrect.")
            flash('Username or password incorrect.')
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
            flash("User already exists")
            return redirect(url_for('login_page'))
        if password_1 != password_2:
            print("Password and confirm password doesn't match")
            flash("Password and confirm password doesn't match")
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
    return render_template('indexButton.html', num=num)

@app.route('/notification')
def notification():
    global uid
    global num

    print(input)
    id=uid

    try:
        app_status = AppMedReq.find_one({'requestedUserID': ObjectId(id)})
        print(app_status['request'])
        if app_status['request']=="Approved":
            notif=1
        elif app_status['request']=="Declined":
            notif=0
        elif app_status['request'] == "tbd":
            notif = 4
        else:
            notif=2
    except:
        notif=2
    return render_template('notification.html',notif=notif, type=num)


@app.route('/complete/<oid>')
def complete(oid):
    global num
    try:
        do_item = ngos.find_one({'_id': ObjectId(oid)})
        do_item['complete'] = True
        ngos.save(do_item)
    except:
        do_item = modos.find_one({'_id': ObjectId(oid)})
        do_item['complete'] = True
        modos.save(do_item)
    return redirect(url_for('index', input=num))

@app.route('/medreq/<id>')
def medreq(id):
    global num
    global ngoid
    ngoid = id
    search_meds=modos.find({'ngoID': id})
    return render_template('medlist.html', todos=search_meds, type=num)

@app.route('/ngoreq/<id>')
def ngoreq(id):
    global num
    global ngoid
    ngoid = id
    search_ngos=ngos.find({'ngoID': id})
    return render_template('medlist.html', todos=search_ngos, type=num)

@app.route('/req_form/<name>')
def req_form(name):
    global num
    global medicine_name
    medicine_name=name
    return render_template('request_form.html', type=num)

@app.route('/ngo_list')
def ngo_list():
    global num
    saved_ngos = ngos.find()
    return render_template('ngolist.html', todos=saved_ngos, type=num)


@app.route('/med_list')
def med_list():
    saved_modos = modos.find()
    return render_template('ngoMedlist.html', todos=saved_modos, type=num)


@app.route('/donate')
def donate():
    return render_template('medicinedonate.html',type=num)

@app.route('/create_request', methods=['POST'])
def create_request():
    global num
    userId= ObjectId(uid)
    user_find = SignupDB.find_one({'_id': ObjectId(uid)})
    new_todo = request.form.get('new-todo')
    new_todo1 = request.form.get('new-todo1')
    new_todo2 = request.form.get('new-todo2')
    new_todo3 = request.form.get('new-todo3')
    new_todo5 = request.form.get('new-todo5')

    AppMedReq.insert_one({'requestedUserID': userId, 'requestedUserName': user_find['Username'], 'recipient':new_todo, 'mailID':new_todo1,'phone':new_todo5,'medicine_name':medicine_name,'MEDquantity':new_todo2,'ngoID':ngoid, 'request':"tbd"})
    return render_template('notification.html',notif=3, type=num)


@app.route('/add_modo', methods=['POST'])
def add_modo():
    global num
    new_modo = request.form.get('new-todo')
    new_todo1 = request.form.get('new-todo1')
    new_todo2 = request.form.get('new-todo2')
    new_todo3 = request.form.get('new-todo3')

    AppDonReq.insert_one({'text': new_modo, 'family': new_todo1, 'ExpDate': new_todo2,'description': new_todo3, 'complete': False})
    return render_template('notification.html',notif=3, type=num)


@app.route('/Approve')
def Approve():
    return render_template('Approve_request.html')


@app.route('/App_req')
def App_req():
    global num
    global flag
    flag = False
    Approval_req = AppMedReq.find({'request': 'tbd'})
    return render_template('Approval_med_req.html', todos=Approval_req, type=num, flag=flag)


@app.route('/App_don')
def App_don():
    global num
    global flag
    flag = False
    Approval_don = AppDonReq.find()
    return render_template('Approval_don_req.html', todos=Approval_don, type=num, flag=flag)


@app.route('/Sel_Apv_don/<text>')
def Sel_Apv_don(text):
    global num, flag, name
    flag = True
    name = text
    search_meds = AppDonReq.find({'text': text})
    return render_template('Approval_don_req.html', todos=search_meds, type=num, flag=flag)


@app.route('/Sel_Apv_req/<text>')
def Sel_Apv_req(text):
    global num, flag, name
    flag = True
    name = text
    search_meds = AppMedReq.find({'medicine_name': text})
    return render_template('Approval_med_req.html', todos=search_meds, type=num, flag=flag)


@app.route('/Approved')
def Approved():
    global num, flag, name
    flag = True
    print(name)
    Approved = AppDonReq.find({'text': name}, {'_id': 0})

    for app in Approved:
        print(app)
        modos.insert_one(app)
        AppDonReq.remove({"text": name})

    return redirect(url_for('index', input=num))


@app.route('/Approved_med')
def Approved_med():
    global num, flag, name, ngoID
    flag = True
    print(name)
    Approved = AppDonReq.find({'text': name}, {'_id': 0})
    AppDonReq.find_one_and_update({'text': name}, {'$set': {'ngoID': ngoID}})

    for app in Approved:
        print(app)
        modos.insert_one(app)
        AppDonReq.remove({"text": name})

    return redirect(url_for('index', input=num))


@app.route('/Declined')
def Declined():
    global num, flag, name
    flag = True
    print("Declined")
    print(name)
    AppDonReq.remove({"text": name})

    return redirect(url_for('index', input=num))


@app.route('/Request_App')
def Request_App():
    global num, flag, name
    flag = True
    print(name)
    AppMedReq.find_one_and_update({'medicine_name': name}, {'$set': {'request': 'Approved'}})

    return redirect(url_for('index', input=num))


@app.route('/Request_Dec')
def Request_Dec():
    global num, flag, name
    flag = True
    print("Declined")
    print(name)
    AppMedReq.find_one_and_update({'medicine_name': name}, {'$set': {'request': 'Declined'}})

    return redirect(url_for('index', input=num))


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
