from flask import Flask
from flask import request, render_template
from flask_pymongo import PyMongo
import datetime
import string
import random

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'testing'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaksInvoice'

mongo = PyMongo(app)

now = datetime.datetime.now().strftime('%Y-%m-%d')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/new', methods=['POST'])
def add_invoice():
  invoice = mongo.db.invoice
  invoice_id = id_generator()
  name = request.form['name']
  address = request.form['address']
  products = request.form.getlist('check')
  quantity = request.form.getlist('qty')
  price = request.form.getlist('price')
  quantity = list(map(int, quantity))
  price = list(map(int, price))
  price1 = [price*quantity for price,quantity in zip(price,quantity)]
  date = now
  invoice_id = invoice.insert({'invoice_id' : invoice_id , 'Name': name, 'Address': address, 'Date' : date, 'Products' : products, 'Quantity' : quantity, 'Price' : price })
  new_invoice = invoice.find_one({'_id': invoice_id })
  return render_template('invoice.html',id = new_invoice['invoice_id'], name = new_invoice['Name'] , products = new_invoice['Products'] , date = new_invoice['Date'], price = new_invoice['Price'],quantity = new_invoice['Quantity'], address = new_invoice['Address'] , length = len(new_invoice['Products']), total = sum(price1))

@app.route('/search', methods=['POST'])
def search_invoice():
    invoice = mongo.db.invoice
    invoice_id = request.form['invoiceid']
    new_invoice = invoice.find_one({'invoice_id': invoice_id}) or invoice.find_one({'Name': invoice_id})
    quantity = new_invoice['Quantity']
    quantity = list(map(int, quantity))
    price = new_invoice['Price']
    price = list(map(int, price))
    price = [price*quantity for price, quantity in zip(price,quantity)]
    return render_template('invoice.html', id=new_invoice['invoice_id'], name=new_invoice['Name'],
                           products=new_invoice['Products'], date=new_invoice['Date'], price=new_invoice['Price'],
                           quantity=new_invoice['Quantity'], address=new_invoice['Address'],
                           length=len(new_invoice['Products']), total=sum(price))

@app.route('/updatePage/<inid>', methods=['POST','GET'])
def to_update(inid):
    invoice = mongo.db.invoice
    invoice_id = inid
    new_invoice = invoice.find_one({'invoice_id': invoice_id})
    return render_template('update.html', id=invoice_id, name=new_invoice['Name'],
                           products=new_invoice['Products'], date=new_invoice['Date'], price=new_invoice['Price'],
                           quantity=new_invoice['Quantity'], address=new_invoice['Address'],
                           length=len(new_invoice['Products']))

@app.route('/updatePage/updateinvoice/<inid>', methods=['POST','GET'])
def update_invoice(inid):
  invoice = mongo.db.invoice
  invoice_id = inid
  name = request.form['name']
  address = request.form['address']
  products = request.form.getlist('check')
  quantity = request.form.getlist('qty')
  price = request.form.getlist('price')
  quantity = list(map(int, quantity))
  price = list(map(int, price))
  price1 = [price*quantity for price, quantity in zip(price, quantity)]
  date = now
  invoice.update({'invoice_id' : invoice_id} , {'invoice_id' : invoice_id ,'Name': name, 'Address': address, 'Date' : date, 'Products' : products, 'Quantity' : quantity, 'Price' : price })
  new_invoice = invoice.find_one({'invoice_id': invoice_id })
  return render_template('invoice.html',id = invoice_id, name = new_invoice['Name'] , products = new_invoice['Products'] , date = new_invoice['Date'], price = new_invoice['Price'],quantity = new_invoice['Quantity'], address = new_invoice['Address'] , length = len(new_invoice['Products']), total = sum(price1))


@app.route('/delete',methods=['POST','GET'])
def delete_invoice():
    invoice = mongo.db.invoice
    invoice_id = request.form['invoiceid']
    new_invoice = invoice.remove({"invoice_id":invoice_id})
    return render_template('success.html', sam=new_invoice)

if __name__ == '__main__':
    app.run(host='0.0.0.0')