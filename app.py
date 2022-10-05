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
class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        return {
        'method': request.method,
        'msg': 'Webhook works on Rahti!',
        'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR') 
        }

    if request.method == 'POST':
        body = request.get_json()
        return {
            'msg': 'You posted successfully',
            'request_body': body
        }

@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method =='GET':
        users = [],
        for user in User2.query.all():
            users.append({
                'id': user.id,
                'email': user.email,
                'updated_at': user.updated_at
            })

    if request.method == 'POST':
        body =  request.get_json()
        new_user = User2(email=body['email'])
        db.session.add(new_user)
        db.session.commit()
        return {'msg': 'User created', 'id':new_user.id}

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')

#http://flask-test-kindstep.rahtiapp.fi/