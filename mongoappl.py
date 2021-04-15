from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from multiprocessing import Process
import time


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://<username>:<password>@cluster0.vspam.mongodb.net/MediGO?retryWrites=true&w=majority'
mongo = PyMongo(app)
ngos = mongo.db.NGOlist
modos = mongo.db.MedicineList

@app.route('/')
def index():
    return render_template('indexButton.html')

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

    modos.insert_one({'text': new_modo, 'family': new_todo1, 'ExpDate': new_todo2,'complete': False})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='localhost', debug=True)



