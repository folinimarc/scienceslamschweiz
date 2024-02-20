'use strict';

console.log('Bonjour from main.js');

/*
When clicking an image, show overlay displaying alt text.
*/
document.querySelectorAll('.img-overlay').forEach(el => {
    el.addEventListener('click', () => {
        if (el.classList.contains("visible")) {
            el.classList.remove("visible");
            el.style.opacity = 0;
        } else {
            el.classList.add("visible");
            el.style.opacity = 0.9;
        }
    });
});

/* Run as soon as all content was loaded */
window.onload = () => {  
  /* Enable all bootstrap 5 popover elements. */
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {html: true})
  })
};
