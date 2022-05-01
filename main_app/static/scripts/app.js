console.log("sanity check");

let $slider = document.getElementById('slider');
let $toggle = document.getElementById('toggle');

$toggle.addEventListener('click', function() {
    let isOpen = $slider.classList.contains('slide-in');

    $slider.setAttribute('class', isOpen ? 'slide-out' : 'slide-in');
});

let $slider2 = document.getElementById('slider2');

$toggle.addEventListener('click', function() {
    let isOpen = $slider2.classList.contains('slide-in2');

    $slider2.setAttribute('class', isOpen ? 'slide-out' : 'slide-in2');
});

