// const text = 'Selamat Datang di Figo Cell';
// const textContainer = document.getElementById('text');
// const delay = 100; // Delay per huruf dalam milidetik
// const pauseTime = 1000; // Waktu jeda sebelum mengulang animasi (1 detik)

// function splitTextToSpans(text) {
//   return text.split('').map((char) => {
//     const span = document.createElement('span');
//     span.textContent = char;
//     span.classList.add('hidden');
//     return span;
//   });
// }

// function showTextPerLetter(spans) {
//   spans.forEach((span, index) => {
//     setTimeout(() => {
//       span.classList.remove('hidden');
//     }, index * delay);
//   });
// }

// function resetText(spans) {
//   spans.forEach((span) => {
//     span.classList.add('hidden');
//   });
// }

// function animateText() {
//   const spans = splitTextToSpans(text);

//   // Kosongkan kontainer sebelum menambahkan ulang spans
//   textContainer.innerHTML = '';
//   spans.forEach((span) => textContainer.appendChild(span));

//   // Mulai menampilkan teks per huruf
//   showTextPerLetter(spans);

//   // Set delay untuk mereset dan memulai ulang animasi
//   setTimeout(() => {
//     resetText(spans);
//     animateText(); // Panggil animasi lagi untuk mengulang
//   }, text.length * delay + pauseTime);
// }

// // Mulai animasi teks
// animateText();

// window.onscroll = function () {
//   var navbar = document.querySelector('.navbarr');

//   // Jika scroll lebih dari 50px dari atas, tambahkan kelas .navbar-transparent
//   if (window.pageYOffset > 50) {
//     navbar.classList.add('navbar-transparent');
//   } else {
//     navbar.classList.remove('navbar-transparent');
//   }
// };

// // Keranjang
// function reloadPage() {
//   location.reload(); // Reload halaman
// }
// $(document).ready(function () {
//   // Handle Update Button Click
//   $('form[action="/keranjang/update"]').on('submit', function (e) {
//     e.preventDefault(); // Mencegah form submit secara default

//     // Ambil data dari form
//     var formData = $(this).serialize();

//     $.ajax({
//       url: '/keranjang/update',
//       type: 'POST',
//       data: formData,
//       success: function (response) {
//         // Menampilkan pesan sukses
//         // Swal.fire({
//         //   icon: 'success',
//         //   title: 'Sukses',
//         //   text: response.msg,
//         //   timer: 2000,
//         //   showConfirmButton: false,
//         // });

//         // Refresh atau update halaman (opsional)
//         setTimeout(function () {
//           location.reload(); // Reload halaman setelah pesan sukses
//         }, 500); // Tunggu 2 detik sebelum refresh
//       },
//       error: function (xhr, status, error) {
//         // Menampilkan pesan error
//         Swal.fire({
//           icon: 'error',
//           title: 'Error',
//           text: xhr.responseJSON.msg,
//         });
//       },
//     });
//   });
// });
const text = 'Selamat Datang di Figo Cell';
const textContainer = document.getElementById('text');
const delay = 100; // Delay per huruf dalam milidetik
const pauseTime = 1000; // Waktu jeda sebelum mengulang animasi (1 detik)

function splitTextToSpans(text) {
  return text.split('').map((char) => {
    const span = document.createElement('span');
    span.textContent = char;
    span.classList.add('hidden');
    return span;
  });
}

function showTextPerLetter(spans) {
  spans.forEach((span, index) => {
    setTimeout(() => {
      span.classList.remove('hidden');
    }, index * delay);
  });
}

function resetText(spans) {
  spans.forEach((span) => {
    span.classList.add('hidden');
  });
}

function animateText() {
  const spans = splitTextToSpans(text);

  // Kosongkan kontainer sebelum menambahkan ulang spans
  textContainer.innerHTML = '';
  spans.forEach((span) => textContainer.appendChild(span));

  // Mulai menampilkan teks per huruf
  showTextPerLetter(spans);

  // Set delay untuk mereset dan memulai ulang animasi
  setTimeout(() => {
    resetText(spans);
    animateText(); // Panggil animasi lagi untuk mengulang
  }, text.length * delay + pauseTime);
}

// Mulai animasi teks
animateText();

window.onscroll = function () {
  var navbar = document.querySelector('.navbarr');

  // Jika scroll lebih dari 50px dari atas, tambahkan kelas .navbar-transparent
  if (window.pageYOffset > 50) {
    navbar.classList.add('navbar-transparent');
  } else {
    navbar.classList.remove('navbar-transparent');
  }
};

// keranjang
$(document).ready(function () {
  // Tangkap event submit form checkout
  $('#checkout-form').submit(function (event) {
    event.preventDefault(); // Mencegah submit form secara default

    $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: $(this).serialize(),
      success: function (response) {
        // Cek apakah checkout berhasil
        if (response.msg === 'Checkout berhasil, pesanan telah dibuat!') {
          // Tampilkan pesan sukses
          Swal.fire({
            title: 'Sukses',
            text: 'Barang berhasil dicheckout.',
            icon: 'success',
            customClass: {
              title: 'custom-swal-title',
              popup: 'custom-swal-popup',
              htmlContainer: 'custom-swal-text', // Pastikan menggunakan htmlContainer
            },
          });
          // Redirect ke halaman konfirmasi pesanan
          // window.location.href = "/";
          setTimeout(function () {
            location.reload(); // Reload halaman setelah 1 detik
          }, 1000);
        } else {
          // Tampilkan pesan error jika ada
          alert(response.msg);
        }
      },
      error: function (xhr, status, error) {
        alert('Terjadi kesalahan: ' + error);
      },
    });
  });
});

$(document).ready(function () {
  // Tangkap event submit form checkout
  $('#delete-form').submit(function (event) {
    event.preventDefault(); // Mencegah submit form secara default

    $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: $(this).serialize(),
      success: function (response) {
        // Cek apakah checkout berhasil
        if (response.msg === 'Produk berhasil dihapus dari keranjang!') {
          // Tampilkan pesan sukses
          Swal.fire({
            title: 'Sukses',
            text: 'Barang berhasil dihapus dari keranjang.',
            icon: 'success',
            customClass: {
              title: 'custom-swal-title',
              popup: 'custom-swal-popup',
              htmlContainer: 'custom-swal-text', // Pastikan menggunakan htmlContainer
            },
          });
          // Redirect ke halaman konfirmasi pesanan
          // window.location.href = "/";
          setTimeout(function () {
            location.reload(); // Reload halaman setelah 1 detik
          }, 1000);
        } else {
          // Tampilkan pesan error jika ada
          alert(response.msg);
        }
      },
      error: function (xhr, status, error) {
        alert('Terjadi kesalahan: ' + error);
      },
    });
  });
});

$(document).ready(function () {
  // Tangkap event submit form checkout
  $('#order').submit(function (event) {
    event.preventDefault(); // Mencegah submit form secara default

    $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: $(this).serialize(),
      success: function (response) {
        // Cek apakah checkout berhasil
        if (response.msg === 'Checkout berhasil, pesanan telah dibuat!') {
          // Tampilkan pesan sukses
          Swal.fire({
            title: 'Sukses',
            text: 'Checkout berhasil, Terimakasih! .',
            icon: 'success',
            customClass: {
              title: 'custom-swal-title',
              popup: 'custom-swal-popup',
              htmlContainer: 'custom-swal-text', // Pastikan menggunakan htmlContainer
            },
          });
          // Redirect ke halaman konfirmasi pesanan
          // window.location.href = "/";
          setTimeout(function () {
            location.reload(); // Reload halaman setelah 1 detik
          }, 1000);
        } else {
          // Tampilkan pesan error jika ada
          alert(response.msg);
        }
      },
      error: function (xhr, status, error) {
        alert('Terjadi kesalahan: ' + error);
      },
    });
  });
});

function updateKeranjang(event, produkNama) {
  event.preventDefault(); // Mencegah form reload

  const form = document.getElementById('form-' + produkNama);
  const formData = new FormData(form);

  fetch('/keranjang/update', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        location.reload(); // Reload halaman setelah SweetAlert
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: data.msg,
        });
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Terjadi kesalahan. Coba lagi nanti.',
      });
    });
}

function deleteProduk(event, produkNama) {
  event.preventDefault(); // Mencegah form reload

  const form = document.getElementById('delete-' + produkNama);
  const formData = new FormData(form);

  fetch('/keranjang/delete', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        Swal.fire({
          icon: 'success',
          title: 'Berhasil!',
          text: data.msg,
          timer: 2000,
          showConfirmButton: false,
        }).then(() => {
          location.reload(); // Reload halaman setelah SweetAlert
        });
      } else {
        // Swal.fire({
        //     icon: 'error',
        //     title: 'Error',
        //     text: data.msg
        // });
        location.reload();
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Terjadi kesalahan. Coba lagi nanti.',
      });
    });
}

function orderProduk(event, produkNama) {
  event.preventDefault(); // Mencegah form reload

  const form = document.getElementById('order-' + produkNama);
  const formData = new FormData(form);

  fetch('/order', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        Swal.fire({
          icon: 'success',
          title: 'Berhasil!',
          text: data.msg,
          timer: 2000,
          showConfirmButton: false,
        }).then(() => {
          location.reload(); // Reload halaman setelah SweetAlert
        });
      } else {
        // Swal.fire({
        //     icon: 'error',
        //     title: 'Error',
        //     text: data.msg
        // });
        location.reload();
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Terjadi kesalahan. Coba lagi nanti.',
      });
    });
}

document.querySelectorAll('form[id^="order-form-"]').forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Mencegah form submit langsung

    const produkNama = form.querySelector('input[name="nama_produk"]').value;

    // Menampilkan konfirmasi SweetAlert sebelum melanjutkan checkout
    Swal.fire({
      title: 'Konfirmasi',
      text: 'Apakah Anda yakin ingin memesan produk ' + produkNama + ' ini?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Ya, Pesan!',
      cancelButtonText: 'Batal',
    }).then((result) => {
      if (result.isConfirmed) {
        // Jika pengguna mengonfirmasi, lakukan submit form
        form.submit();
      }
    });
  });
});
