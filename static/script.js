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

// Keranjang
function reloadPage() {
  location.reload(); // Reload halaman
}
$(document).ready(function () {
  // Handle Update Button Click
  $('form[action="/keranjang/update"]').on('submit', function (e) {
    e.preventDefault(); // Mencegah form submit secara default

    // Ambil data dari form
    var formData = $(this).serialize();

    $.ajax({
      url: '/keranjang/update',
      type: 'POST',
      data: formData,
      success: function (response) {
        // Menampilkan pesan sukses
        // Swal.fire({
        //   icon: 'success',
        //   title: 'Sukses',
        //   text: response.msg,
        //   timer: 2000,
        //   showConfirmButton: false,
        // });

        // Refresh atau update halaman (opsional)
        setTimeout(function () {
          location.reload(); // Reload halaman setelah pesan sukses
        }, 500); // Tunggu 2 detik sebelum refresh
      },
      error: function (xhr, status, error) {
        // Menampilkan pesan error
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: xhr.responseJSON.msg,
        });
      },
    });
  });
});

// $(document).ready(function () {
//   $('#checkout-form').on('submit', function (e) {
//     e.preventDefault(); // Mencegah form melakukan submit biasa

//     $.ajax({
//       type: 'POST',
//       url: $(this).attr('action'), // URL dari action form
//       data: $(this).serialize(), // Kirim data form
//       success: function (response) {
//         // Cek apakah ada pesan sukses (sesuaikan respons dari server)
//         if (response.msg === 'Checkout berhasil!') {
//           alert(response.msg); // Tampilkan pesan sukses
//           setTimeout(function () {
//             location.reload(); // Reload halaman setelah 1 detik
//           }, 1000);
//         }
//       },
//       error: function () {
//         alert('Terjadi kesalahan saat checkout. Silakan coba lagi.');
//       },
//     });
//   });
// });
// $(document).ready(function () {
//   $('#checkout-form').on('submit', function (e) {
//     e.preventDefault(); // Mencegah form submit biasa

//     $.ajax({
//       type: 'POST',
//       url: $(this).attr('action'), // URL dari action form
//       data: $(this).serialize(), // Kirimkan data form
//       success: function (response) {
//         // Cek apakah pesan sukses ada di dalam respons
//         if (response.msg === 'Checkout berhasil, pesanan telah dibuat!') {
//           alert(response.msg); // Tampilkan pesan sukses
//           setTimeout(function () {
//             location.reload(); // Reload halaman setelah 1 detik
//           }, 1000);
//         }
//       },
//       error: function () {
//         alert('Terjadi kesalahan saat checkout. Silakan coba lagi.');
//       },
//     });
//   });
// });
