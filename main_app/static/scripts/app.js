console.log("sanity check");

// Modal
const modal = new bootstrap.Modal(document.getElementById("modal"))


htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })

htmx.on("hidden.bs.modal", () => {
document.getElementById("dialog").innerHTML = ""
})
  


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


