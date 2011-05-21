from flask import Flask, render_template, redirect, url_for, request
import pymongo
from pymongo.objectid import ObjectId

app = Flask(__name__)
connection = pymongo.Connection()
db = connection['address_book']

## index page - list addresses
@app.route('/', methods=['GET'])
def addresses():
    addresses = db.addresses.find()
    return render_template('index.html', addresses=addresses)

## new addres form
@app.route('/address/new', methods=['GET'])
def new_address():
    return render_template('new.html')

## create a new address
@app.route('/address', methods=['POST'])
def create_address():
    address = {
             'firstname':request.form['firstname'],
             'lastname':request.form['lastname'],
             'email':request.form['email'],
             'website':request.form['website']
             }
    
    id = db.addresses.insert(address)
    return redirect(url_for('show_address',id=str(id)))

## show current address
@app.route('/address/<id>', methods=['GET'])
def show_address(id):
    address = db.addresses.find_one({"_id": ObjectId(id)})
    return render_template('show.html', address=address)

## edit current address
@app.route('/address/<id>/edit', methods=['GET'])
def edit_address(id):
    address = db.addresses.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', address=address)

## update address details
@app.route('/address/<id>', methods=['POST'])
def update_address(id):
    db.addresses.update({"_id": ObjectId(id)}, {"$set": {
                                                         'firstname':request.form['firstname'],
                                                         'lastname':request.form['lastname'],
                                                         'email':request.form['email'],
                                                         'website':request.form['website']
                                                         }})
    
    return redirect(url_for('show_address',id=id))

## delete address
@app.route('/address/<id>/delete', methods=['GET'])
def delete_address(id):
    db.addresses.remove({"_id": ObjectId(id)})
    return redirect(url_for('addresses'))

if __name__ == '__main__':
    app.run(debug=True)