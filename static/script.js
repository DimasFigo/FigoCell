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
