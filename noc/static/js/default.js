// Показать кнопку, когда пользователь прокручивает документ на 20 пикселей вниз
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
        document.getElementById("scrollup").style.display = "block";
    } else {
        document.getElementById("scrollup").style.display = "none";
    }
}

// Прокручивать страницу вверх, когда пользователь нажимает на кнопку
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}