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
@app.route('/total_pengguna', methods=['GET'])
def total_pengguna():
    # Mengambil jumlah pengguna dari koleksi 'pengguna'
    jumlah_pengguna = db.users.count_documents({})
    
    return jsonify({'total_pengguna': jumlah_pengguna})

@app.route('/total_order', methods=['GET'])
def total_order():
    # Mengambil jumlah pengguna dari koleksi 'pengguna'
    jumlah_order = db.orders.count_documents({})
    
    return jsonify({'total_order': jumlah_order})

@app.route('/total_produk', methods=['GET'])
def total_produk():
    # Mengambil jumlah pengguna dari koleksi 'pengguna'
    jumlah_produk = db.produk.count_documents({})
    
    return jsonify({'total_produk': jumlah_produk})
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
        return render_template('index.html', username=session['username'])
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

# Keranjang Collection
@app.route('/keranjang', methods=['GET'])
def view_cart():
    if 'username' in session:
        username = session['username']
        keranjang = db.keranjang.find_one({'username': username})
        if keranjang:
            produk_keranjang = keranjang.get('produk', [])
            # Pastikan harga dikonversi menjadi integer/float sebelum dijumlahkan
            total_harga = sum(int(produk['total']) for produk in produk_keranjang)
            return render_template('keranjang.html', produk_keranjang=produk_keranjang, total_harga=total_harga, username=session.get('username'))
        return render_template('keranjang.html', produk_keranjang=[], total_harga=0, username=session.get('username'))
    flash('Anda harus login untuk melihat keranjang!')
    return redirect(url_for('login'))


@app.route('/keranjang/add', methods=['POST'])
def add_to_cart():
    if 'username' not in session:  # Pastikan user sudah login
        return jsonify({'msg': 'Anda harus login untuk menambahkan barang ke keranjang.', 'status': 'error'}), 401
    if 'username' in session:  # Cek apakah user sudah login
        nama_produk = request.form.get('nama_produk')
        username = session['username']

        # Cari produk berdasarkan nama
        produk = db.produk.find_one({'nama': nama_produk})
    
        if produk:
            # Pastikan harga adalah integer
            harga = int(produk['harga'])  # Konversi harga ke integer

            # Cek apakah produk sudah ada di keranjang
            keranjang = db.keranjang.find_one({'username': username})

            if keranjang:
                # Jika produk sudah ada, tambahkan jumlahnya
                produk_dalam_keranjang = keranjang.get('produk', [])
                for item in produk_dalam_keranjang:
                    if item['nama'] == nama_produk:
                        item['jumlah'] += 1
                        item['total'] = item['jumlah'] * harga  # Pastikan total dihitung dengan harga yang benar
                        break
                else:
                    # Jika produk belum ada, tambahkan produk baru
                    produk_baru = {
                        'nama': produk['nama'],
                        'harga': harga,
                        'jumlah': 1,
                        'total': harga,  # Total dihitung dengan harga yang benar
                        'file': produk['file']
                    }
                    produk_dalam_keranjang.append(produk_baru)
                
                # Update keranjang di database
                db.keranjang.update_one(
                    {'username': username},
                    {'$set': {'produk': produk_dalam_keranjang}}
                )
            else:
                # Jika keranjang belum ada, buat keranjang baru
                produk_baru = {
                    'nama': produk['nama'],
                    'harga': harga,
                    'jumlah': 1,
                    'total': harga,  # Total dihitung dengan harga yang benar
                    'file': produk['file']
                }
                db.keranjang.insert_one({
                    'username': username,
                    'produk': [produk_baru]
                })

            return jsonify({'msg': 'Produk berhasil ditambahkan ke keranjang!'})
        else:
            return jsonify({'msg': 'Produk tidak ditemukan!'}), 404
    return jsonify({'msg': 'Anda harus login untuk menambahkan ke keranjang!'})


@app.route('/keranjang/delete', methods=['POST'])
def delete_from_cart():
    if 'username' in session:  # Cek apakah user sudah login
        nama_produk = request.form.get('nama_produk')

        if not nama_produk:
            return jsonify({'msg': 'Nama produk tidak ditemukan!'}), 400
        
        # Hapus produk dari keranjang berdasarkan nama
        username = session['username']
        result = db.keranjang.update_one(
            {'username': username},
            {'$pull': {'produk': {'nama': nama_produk}}}  # Menghapus produk berdasarkan nama
        )

        if result.modified_count > 0:
            return jsonify({'msg': 'Produk berhasil dihapus dari keranjang!'})
        else:
            return jsonify({'msg': 'Produk tidak ditemukan dalam keranjang!'}), 404
    return jsonify({'msg': 'Anda harus login untuk menghapus dari keranjang!'}), 401

# @app.route('/keranjang/update', methods=['POST'])
# def update_keranjang():
#     if 'username' in session:
#         username = session['username']
#         nama_produk = request.form.get('nama_produk')
#         jumlah = int(request.form.get('jumlah'))

#         if nama_produk and jumlah > 0:
#             # Update jumlah produk di keranjang
#             result = db.keranjang.update_one(
#                 {'username': username, 'produk.nama': nama_produk},
#                 {'$set': {'produk.$.jumlah': jumlah, 'produk.$.total': jumlah * db.produk.find_one({'nama': nama_produk})['harga']}}
#             )
#             if result.modified_count > 0:
#                 return jsonify({'msg': 'Jumlah produk berhasil diperbarui!'})
#             else:
#                 return jsonify({'msg': 'Gagal memperbarui produk di keranjang!'}), 400
#     return jsonify({'msg': 'Anda harus login untuk memperbarui produk!'}), 401
# @app.route('/keranjang/update', methods=['POST'])
# def update_keranjang():
#     if 'username' in session:
#         username = session['username']
#         nama_produk = request.form.get('nama_produk')
#         jumlah = int(request.form.get('jumlah'))

#         # Cek apakah produk ada di keranjang user
#         keranjang_item = db.keranjang.find_one({'username': username, 'produk.nama': nama_produk})
        
#         if keranjang_item:
#             # Ambil jumlah produk saat ini dari keranjang
#             jumlah_sekarang = keranjang_item['produk']['jumlah']
            
#             # Tambahkan jumlah baru ke jumlah yang ada
#             jumlah_total = jumlah_sekarang + jumlah

#             # Update jumlah produk di keranjang
#             result = db.keranjang.update_one(
#                 {'username': username, 'produk.nama': nama_produk},
#                 {'$set': {'produk.$.jumlah': jumlah_total, 'produk.$.total': jumlah_total * db.produk.find_one({'nama': nama_produk})['harga']}}
#             )

#             if result.modified_count > 0:
#                 return jsonify({'msg': 'Jumlah produk berhasil diperbarui!'})
#             else:
#                 return jsonify({'msg': 'Gagal memperbarui produk di keranjang!'}), 400
#         else:
#             return jsonify({'msg': 'Produk tidak ditemukan dalam keranjang!'}), 404
#     return jsonify({'msg': 'Anda harus login untuk memperbarui produk!'}), 401
@app.route('/keranjang/update', methods=['POST'])
def update_keranjang():
    if 'username' in session:
        username = session['username']
        nama_produk = request.form.get('nama_produk')
        jumlah = int(request.form.get('jumlah'))

        # Cek apakah produk ada di keranjang user
        keranjang_item = db.keranjang.find_one({'username': username, 'produk.nama': nama_produk})

        if keranjang_item:
            # Cari produk yang cocok dalam list produk
            for produk in keranjang_item['produk']:
                if produk['nama'] == nama_produk:
                    jumlah_sekarang = int(produk['jumlah'])

                    # Tambahkan jumlah baru ke jumlah yang ada
                    jumlah_total = int(jumlah_sekarang + 1)

                    harga_produk = int(db.produk.find_one({'nama': nama_produk})['harga'])
                    result = db.keranjang.update_one(
                    {'username': username, 'produk.nama': nama_produk},
                    {'$set': {
                        'produk.$.jumlah': jumlah_total,
                        'produk.$.total': jumlah_total * harga_produk
                        }}
                    )

                    if result.modified_count > 0:
                        return jsonify({'msg': 'Jumlah produk berhasil diperbarui!'})
                    else:
                        return jsonify({'msg': 'Gagal memperbarui produk di keranjang!'}), 400

            # Jika produk tidak ditemukan
            return jsonify({'msg': 'Produk tidak ditemukan dalam keranjang!'}), 404
    return jsonify({'msg': 'Anda harus login untuk memperbarui produk!'}), 401


# Order Collection
@app.route('/order', methods=['POST'])
def create_order():
    if 'username' in session:
        username = session['username']
        keranjang = db.keranjang.find_one({'username': username})

        if keranjang:
            produk_keranjang = keranjang.get('produk', [])
            if not produk_keranjang:
                return jsonify({'msg': 'Keranjang Anda kosong!'}), 400

            # Simpan pesanan ke collection orders
            order_id = str(datetime.utcnow().timestamp())  # Gunakan timestamp untuk ID pesanan
            order = {
                'username': username,
                'produk': produk_keranjang,
                'total_harga': sum(produk['total'] for produk in produk_keranjang),
                'status': 'Pending',  # Status awal pesanan
                'tanggal_pesan': datetime.utcnow(),
                'order_id': order_id
            }

            db.orders.insert_one(order)

            # Mengurangi stok produk setelah pemesanan
            for produk in produk_keranjang:
                db.produk.update_one(
                    {'nama': produk['nama']},
                    {'$inc': {'stok': -produk['jumlah']}}
                )

            # Menghapus produk dari keranjang setelah pemesanan
            db.keranjang.delete_one({'username': username})

            return jsonify({'msg': 'Pesanan berhasil dibuat!', 'order_id': order_id})
        else:
            return jsonify({'msg': 'Keranjang tidak ditemukan!'}), 404
    return jsonify({'msg': 'Anda harus login untuk melakukan pemesanan!'}), 401

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'username' in session:
        username = session['username']
        keranjang = db.keranjang.find_one({'username': username})

        if keranjang:
            produk_keranjang = keranjang.get('produk', [])
            if not produk_keranjang:
                return jsonify({'msg': 'Keranjang Anda kosong!'}), 400

            db.produk.update_many(
                { "stok": { "$type": "string" } },
                [
                    { "$set": { "stok": { "$toInt": "$stok" } } }
                ]
            )

            # Simpan pesanan ke collection orders
            order_id = str(datetime.utcnow().timestamp())  # Gunakan timestamp untuk ID pesanan
            # total_harga = sum(produk['total'] for produk in produk_keranjang)
            total_harga = sum(float(produk['total']) for produk in produk_keranjang)
            
            order = {
                'username': username,
                'produk': produk_keranjang,
                'total_harga': total_harga,
                'status': 'Pending',  # Status awal pesanan
                'tanggal_pesan': datetime.utcnow(),
                'order_id': order_id
            }

            # Masukkan pesanan ke database
            db.orders.insert_one(order)

            # Mengurangi stok produk setelah pemesanan
            for produk in produk_keranjang:
                db.produk.update_one(
                    {'nama': produk['nama']},
                    {'$inc': {'stok': -produk['jumlah']}}
                )

            # Menghapus produk dari keranjang setelah pemesanan
            db.keranjang.delete_one({'username': username})

            return jsonify({'msg': 'Checkout berhasil, pesanan telah dibuat!', 'order_id': order_id})
        else:
            return jsonify({'msg': 'Keranjang tidak ditemukan!'}), 404
    return jsonify({'msg': 'Anda harus login untuk melakukan checkout!'}), 401


@app.route('/order', methods=["GET"])
def order():
   return render_template('order.html', username=session.get('username'))

@app.route('/orders', methods=["GET"])
def orders():
   order_list = list(db.orders.find({}, {'_id': False}))
   return jsonify({'orders': order_list})

@app.route("/orders/delete", methods=['POST'])
def orders_delete():
    order_receive = request.form['orderId_give']
    db.orders.delete_one( {
        'order_id': order_receive
    } )
    return jsonify({'msg': 'Delete order success!'})

@app.route("/orders/update", methods=["POST"])
def orders_update():
    order_id_receive = request.form.get('orderId')  
    status_receive = request.form.get('status')

    if not order_id_receive or not status_receive:
        return jsonify({'msg': 'Order ID dan status harus diisi!'}), 400

    db.orders.update_one(
        {'order_id': order_id_receive},
        {'$set': {'status': status_receive}}
    )
    return jsonify({'msg': 'Data order updated successfully'})


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

@app.route('/profile/<username>', methods=["GET"])
def profile(username):
    # Mengambil data profil pengguna
    user_data = db.users.find_one({'username': username})
    
    if not user_data:
        flash("User not found!")
        return redirect(url_for('login'))
    
    # Mengambil data order berdasarkan username
    orders = list(db.orders.find({'username': username}))
    
    # Render template profile dengan data pengguna dan pesanan
    return render_template('profile.html', user_data=user_data, orders=orders)





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

