document.addEventListener('DOMContentLoaded', function() {
    var link1 = document.querySelector('.slider__inner .slider__item:nth-child(1) .btn2');
    var link2 = document.querySelector('.slider__inner .slider__item:nth-child(2) .btn2');

    var accordion1 = document.querySelector('#wedo_2');
    var accordion2 = document.querySelector('#wedo_3');

    link1.addEventListener('click', function(event) {
        event.preventDefault();
        accordion1.style.display = 'block';
        accordion2.style.display = 'none';
    });

    link2.addEventListener('click', function(event) {
        event.preventDefault();
        accordion1.style.display = 'none';
        accordion2.style.display = 'block';
    });
});

