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

/*
Align height of columns with height of images in corresponding rows.
This is used to allow for y overflow of text elements when they exceed height of images in corresponding rows.
*/
function alignHeights() {
    const elements = document.querySelectorAll('.align-col-height-with-row-img');
    elements.forEach(el => {
      const targetElement = el.parentNode.querySelector('img');
      if (targetElement) {
        el.style.maxHeight = `${targetElement.offsetHeight}px`;
      }
    });
  }

window.onload = () => {
  alignHeights();
  window.addEventListener('resize', alignHeights);
  
  /* Enable all bootstrap 5 popover elements. */
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {html: true})
  })
};
