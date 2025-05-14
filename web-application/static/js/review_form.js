const ratingStars = document.querySelectorAll('.rating span');
const ratingInput = document.getElementById('rating-value');
const reviewForm = document.querySelector('.comment-form form'); 

ratingStars.forEach(star => {
    star.addEventListener('click', () => {
        const value = star.dataset.value;
        ratingInput.value = value; 
        ratingStars.forEach(s => s.classList.remove('active'));
        for (let i = 0; i < value; i++) {
            ratingStars[i].classList.add('active');
        }
    });

    star.addEventListener('mouseover', () => {
        const value = star.dataset.value;
        ratingStars.forEach(s => s.classList.remove('active'));
        for (let i = 0; i < value; i++) {
            ratingStars[i].classList.add('active');
        }
    });

    star.addEventListener('mouseout', () => {
        const currentValue = ratingInput.value;
        ratingStars.forEach(s => s.classList.remove('active'));
        for (let i = 0; i < currentValue; i++) {
            ratingStars[i].classList.add('active');
        }
    });
});

reviewForm.addEventListener('submit', (event) => {
    if (ratingInput.value === "0") {
        event.preventDefault(); 
        alert("Нужно выставить оценку!"); 
    }
});