# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
atm_db = db.collection('atm')

data_atm = {}


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    data = {}

    try:
        id = request.form['id']
        data_atm['NoRekening'] = request.form['NoRekening']
        data_atm['Pin'] = request.form['Pin']
        data_atm['Saldo'] = int(request.form['Saldo'])
        data_atm['Nama'] = request.form['Nama']
        data_atm['TTL'] = request.form['TTL']
        data_atm['Alamat'] = request.form['Alamat']
        atm_db.document(id).set(data_atm)

        data['message'] = "Data Berhasil ditambahkan"
        data['success'] = True
        return jsonify(data), 200
    except Exception as e:
        data['success'] = False
        data['message'] = e
        return jsonify(data)


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        user : Return document that matches query ID.
        all_user : Return all documents.
    """
    data = {}
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('user')
        data['message'] = "Data Berhasil ditampilkan"
        data['success'] = True
        if todo_id:
            user = atm_db.document(todo_id).get()
            data['data'] = user.to_dict()
            return jsonify(data), 200
        else:
            all_user = [doc.to_dict() for doc in atm_db.stream()]
            data['data'] = all_user
            return jsonify(data), 200

    except Exception as e:
        data['success'] = False
        data['message'] = e
        return jsonify(data)


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    data = {}
    try:
        id = request.form['id']
        data_atm['NoRekening'] = request.form['NoRekening']
        data_atm['Pin'] = request.form['Pin']
        data_atm['Saldo'] = request.form['Saldo']
        data_atm['Nama'] = request.form['Nama']
        data_atm['TTL'] = request.form['TTL']
        data_atm['Alamat'] = request.form['Alamat']
        atm_db.document(id).update(data_atm)
        return jsonify({"success": True}), 200
    except Exception as e:
        data['success'] = False
        data['message'] = e
        return jsonify(data)


@app.route('/delete', methods=['DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    data = {}
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        atm_db.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        data['success'] = False
        data['message'] = e
        return jsonify(data)


@app.route("/withdraw", methods=["PUT"])
def withdrawMoney():
    data = {}
    try:
        id = request.form['id']
        user = atm_db.document(id).get().to_dict()
        money = int(request.form['saldo'])

        if int(user['Saldo']) > money:
            user['Saldo'] = int(user['Saldo']) - money
            atm_db.document(id).update(user)

            data['success'] = True
            data['message'] = f"sisa saldo anda  : {user['Saldo']}"
        else:
            data['success'] = False
            data['message'] = f"sisa saldo anda tidak mencukup"

        return jsonify(data)
    except Exception as e:
        data['success'] = False
        data['message'] = e
        return jsonify(data)


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, port=port)
