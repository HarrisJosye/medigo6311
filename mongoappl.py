from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from multiprocessing import Process
import time


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://harrisjosye:SfVK0uf8fOgIcE3U@cluster0.vspam.mongodb.net/MediGO?retryWrites=true&w=majority'
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


if __name__ == "__main__":
    app.run(host='localhost', debug=True)



