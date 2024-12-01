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
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        if users_collection.find_one({'username': username,}):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if users_collection.find_one({'email': email}):
            flash('Email already registered')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({'nama':nama, 'username': username, 'password': hashed_password, 'role': role, 'email':email})
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
    return render_template('lihat-product.html', username=session.get('username'))

@app.route("/tambah-produk", methods=["GET"])
def tambah_produk():
    return render_template('tambah-product.html', username=session.get('username'))

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

@app.route('/keranjang', methods=['GET'])
def view_cart():
    if 'username' in session:
        username = session['username']
        keranjang = db.keranjang.find_one({'username': username})
        if keranjang:
            produk_keranjang = keranjang.get('produk', [])
            # Pastikan harga dikonversi menjadi integer/float sebelum dijumlahkan
            total_harga = sum(int(produk['harga']) for produk in produk_keranjang)
            return render_template('keranjang.html', produk_keranjang=produk_keranjang, total_harga=total_harga, username=session.get('username'))
        return render_template('keranjang.html', produk_keranjang=[], total_harga=0)
    flash('Anda harus login untuk melihat keranjang!')
    return redirect(url_for('login'))


@app.route('/keranjang/add', methods=['POST'])
def add_to_cart():
    if 'username' in session:  # Cek apakah user sudah login
        nama_produk = request.form.get('nama_produk')
        username = session['username']
        
        # Cari produk berdasarkan nama
        produk = db.produk.find_one({'nama': nama_produk})
        
        if produk:
            # Tambahkan produk ke keranjang user
            db.keranjang.update_one(
                {'username': username},
                {'$push': {'produk': produk}},
                upsert=True
            )
            return jsonify({'msg': 'Produk berhasil ditambahkan ke keranjang!'})
        else:
            return jsonify({'msg': 'Produk tidak ditemukan!'}), 404
    return jsonify({'msg': 'Anda harus login untuk menambahkan ke keranjang!'}), 401

@app.route('/product', methods=["GET"])
def product():
   return render_template ('product.html', username=session.get('username'))

@app.route('/detail', methods=["GET"])
def detail():
   return render_template ('detail-product.html', username=session.get('username'))

@app.route('/contact', methods=["GET"])
def contact():
   return render_template ('contact.html',username=session.get('username'))

@app.route('/pulsa/regular', methods=["GET"])
def regular():
   return render_template ('pulsa-regular.html', username=session.get('username'))

@app.route('/pulsa/listrik', methods=["GET"])
def listrik():
   return render_template ('pulsa-listrik.html', username=session.get('username'))

# Users Collcetion
@app.route('/user', methods=["GET"])
def user():
   return render_template('user.html', username=session.get('username'))

@app.route('/users', methods=["GET"])
def users():
   user_list = list(db.users.find({}, {'_id': False}))
   return jsonify({'users': user_list})

@app.route("/users/delete", methods=['POST'])
def users_delete():
    username_receive = request.form['username_give']
    db.users.delete_one( {
        'username': username_receive
    } )
    return jsonify({'msg': 'Delete user success!'})

@app.route("/users/update", methods=["POST"])
def users_update():
    id_receive = request.form.get('id')  # pastikan ID diambil dengan benar
    nama_receive = request.form.get('nama')
    username_receive = request.form.get('username')
    email_receive = request.form.get('email')
    role_receive = request.form.get('role')

    if not id_receive or not nama_receive or not username_receive or not email_receive or not role_receive:
        return jsonify({'msg': 'Semua field harus diisi!'}), 400

    db.users.update_one(
        {'username': username_receive},
        {'$set': {
            'nama': nama_receive,
            'email': email_receive,
            'role': role_receive,
        }}
    )
    return jsonify({'msg': 'Data user updated successfully'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

