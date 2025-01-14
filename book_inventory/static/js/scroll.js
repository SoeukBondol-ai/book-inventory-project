const scrollContainer = document.querySelector('.scrollable-container');
const scrollLeftButton = document.querySelector('.scroll-left');
const scrollRightButton = document.querySelector('.scroll-right');

// Scroll Left
scrollLeftButton.addEventListener('click', () => {
    scrollContainer.scrollBy({
        left: -300, // Adjust scroll distance
        behavior: 'smooth'
    });
});

// Scroll Right
scrollRightButton.addEventListener('click', () => {
    scrollContainer.scrollBy({
        left: 300, // Adjust scroll distance
        behavior: 'smooth'
    });
});

// Hide buttons when at the start or end
scrollContainer.addEventListener('scroll', () => {
    if (scrollContainer.scrollLeft === 0) {
        scrollLeftButton.classList.add('hidden');
    } else {
        scrollLeftButton.classList.remove('hidden');
    }

    if (scrollContainer.scrollLeft + scrollContainer.clientWidth >= scrollContainer.scrollWidth) {
        scrollRightButton.classList.add('hidden');
    } else {
        scrollRightButton.classList.remove('hidden');
    }
});

// Initial check for button visibility
scrollContainer.dispatchEvent(new Event('scroll'));