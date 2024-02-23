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


function alignHeightsAboveBreakpoint() {
  const elements = document.querySelectorAll('.overflow-above-breakpoint');
  elements.forEach(el => {
    const targetElement = el.parentNode.querySelector('img');
    // Check if the target image element exists
    if (targetElement) {
      // For viewports above the 'lg' breakpoint (>= 992px)
      if (window.innerWidth >= 992) {
        el.style.maxHeight = `${targetElement.offsetHeight}px`;
        el.classList.add('overflow-auto');
      } else {
        // For viewports below the 'lg' breakpoint (< 992px)
        el.style.maxHeight = ''; // Reset the maxHeight
        el.classList.remove('overflow-auto');
      }
    }
  });
}

/* Run as soon as all content was loaded */
window.onload = () => {  
  /* Enable all bootstrap 5 popover elements. */
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {html: true})
  })
  /* Align heights of columns with images in corresponding rows. */
  alignHeightsAboveBreakpoint();
  window.addEventListener('resize', alignHeightsAboveBreakpoint);
};
