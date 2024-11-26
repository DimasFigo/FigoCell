from flask import Flask, render_template, request, flash,redirect, url_for, session, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = '12092004'
bcrypt = Bcrypt(app)

client = MongoClient('mongodb+srv://figoood99:figocell17@figocell.wxlz7.mongodb.net/')
db = client['user_management']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if users_collection.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({'username': username, 'password': hashed_password, 'role': role})
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('dashboard_admin.html', username=session['username'])
    flash('Unauthorized access!')
    return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session and session['role'] == 'user':
        return render_template('dashboard_user.html', username=session['username'])
    flash('Unauthorized access!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

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
        return jsonify({'msg': 'Nama sudah terdaftar, silahkan mengecek nama produknya!'})
    
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

@app.route("/produk/update", methods=["POST"])
def produk_update():
    
    nama_receive = request.form.get('nama')
    
    # Cek jika nama kosong
    if not nama_receive:
        return jsonify({'msg': 'ID tidak valid atau tidak ditemukan!'}), 400


    nama_receive = request.form.get('nama')
    jenis_receive = request.form.get('jenis')
    stok_receive = request.form.get('stok')
    harga_receive = request.form.get('harga')

    db.produk.update_one(
        {'nama': nama_receive},
        {'$set': {
            'nama': nama_receive,
            'jenis': jenis_receive,
            'stok': stok_receive,
            'harga': harga_receive,
        }}
    )
    return jsonify({'msg': 'Data updated successfully'})

@app.route('/keranjang', methods=["GET"])
def keranjang():
   return render_template ('keranjang.html')

@app.route('/product', methods=["GET"])
def product():
   return render_template ('product.html')

@app.route('/detail', methods=["GET"])
def detail():
   return render_template ('detail-product.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

