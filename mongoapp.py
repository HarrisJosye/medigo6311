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

@app.route('/admin')
def adminindex():
    saved_ngos = ngos.find()
    saved_meds=modos.find()
    return render_template('index.html', ngos=saved_ngos, modos=saved_meds)

@app.route('/add_ngo', methods=['POST'])
def add_ngo():
    new_todo = request.form.get('new-todo')
    ngos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/add_modo', methods=['POST'])
def add_modo():
    new_modo = request.form.get('new-todo')
    modos.insert_one({'text' : new_modo, 'complete' : False})
    return redirect(url_for('index'))

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

@app.route('/delete_completed')
def delete_completed():
    ngos.delete_many({'complete' : True})
    modos.delete_many({'complete': True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    ngos.delete_many({})
    modos.delete_many({})
    return redirect(url_for('index'))

@app.route('/ngo_list')
def ngo_list():
    saved_ngos = ngos.find()
    return render_template('ngolist.html', todos=saved_ngos)

@app.route('/med_list')
def med_list():
    saved_modos = modos.find()
    return render_template('medicinelist.html', todos=saved_modos)

def thread1():
    app.run(host='localhost', debug=True)

def thread2():
    i=0
    while i<30:
        print(f'This is thread 2 function:{i}')
        time.sleep(1)
        i=i+1

def main():
    t1 = Process(target=thread1)
    t2 = Process(target=thread2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()