from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://figocahyo:figo123@cluster0.jjl9s.mongodb.net/')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('admin.html')

@app.route("/produk", methods=["GET"])
def produk_get():
    produk_list = list(db.produk.find({}, {'_id': False}))
    return jsonify({'produk': produk_list})

@app.route("/produk", methods=["POST"])
def produk_post():
    nama_receive = request.form.get('nama_give')
    jenis_receive = request.form.get('jenis_give')
    stok_receive = request.form.get('stok_give')
    harga_receive = request.form.get('harga_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    exntension = file.filename.split('.')[-1]
    file_name = f'static/post-{mytime}.{exntension}'
    file.save(file_name)

    if not nama_receive or not jenis_receive or not stok_receive or not file:
        return jsonify({'msg': 'Isi semua data prodduk'})
    
    produk_list = list(db.produk.find({'nama': nama_receive}, {'_id': False}))
    
    if produk_list:
        return jsonify({'msg': 'Nama sudah terdaftar, silahkan mengehcek nama produk nya!'})
    
    doc = {
        'nama': nama_receive,
        'jenis': jenis_receive,
        'stok': stok_receive,
        'file': file_name,
        'harga': harga_receive
    }
    db.produk.insert_one(doc)
    return jsonify({'msg': 'Data saved successfully'})

@app.route("/daftar-produk", methods=["GET"])
def daftar_produk():
    return render_template('lihat-product.html')

@app.route("/tambah-produk", methods=["GET"])
def tambah_produk():
    return render_template('tambah-product.html')

@app.route("/produk/delete", methods=['POST'])
def produk_delete():
    nama_receive = request.form['nama_give']
    db.produk.delete_one( {
        'nama': nama_receive
    } )
    return jsonify({'msg': 'Delete success!'})

@app.route("/produk/update", methods=['POST'])
def produk_update():
    nama_receive = request.form.get('nama_give')
    jenis_receive = request.form.get('jenis_give')
    stok_receive = request.form.get('stok_give')
    file = request.files["file_give"]

    db.produk.update_one(
        {'nama': nama_receive},
        {'$set': {
            'nama': nama_receive,
            'jenis': jenis_receive,
            'stok': stok_receive,
            'file': file
        }}
    )
    return jsonify({'msg': 'Data updated successfully'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

