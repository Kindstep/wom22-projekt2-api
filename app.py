import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')

db.init_app(app)

# datamodell = tabell i postgresql
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return {
        'method': request.method,
        'msg': 'Received all orders',
        'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR') 
        }

    if request.method == 'POST':
        body = request.get_json()
        return {
            'msg': 'You posted an order successfully',
            'request_body': body
        }

@app.route("/order", methods=['GET', 'POST'])
def orders():
    if request.method =='GET':
        orders = [],
        for order in Order.query.all():
            orders.append({
                'id': order.id,
                'order': order.order,
                'updated_at': order.updated_at
            })

    if request.method == 'POST':
        body =  request.get_json()
        new_order = Order(order=body)
        db.session.add(new_order)
        db.session.commit(new_order)

        return {'msg': 'Order created', 'id':new_order.id}
        

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')

#http://flask-test-kindstep.rahtiapp.fi/