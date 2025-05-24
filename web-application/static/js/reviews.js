const reviewButtonWrapper = document.querySelector('.review-button-wrapper');    
const starFilter = document.querySelector('.star-filter');
const crossSign = document.querySelector('.cross-sign');

window.addEventListener('resize',checkWidth)
reviewButtonWrapper.addEventListener('click', closeFiltersByClickingOnTheGraySpot);

function checkWidth(){
    if (reviewButtonWrapper.style.display == 'block' && window.innerWidth>=770) {
        reviewButtonWrapper.style.display = '';
        starFilter.style.display = '';
        crossSign.style.display = '';
    }
}
function showFilters(){
    reviewButtonWrapper.style.display = 'block';
    starFilter.style.display = 'block';
    crossSign.style.display = 'flex';
}
function closeFiltersByClickingOnTheGraySpot(event) {
    if (event.target === reviewButtonWrapper) {
        closeFilters()
    }
}
function closeFilters(){
    reviewButtonWrapper.style.display = '';
    starFilter.style.display = '';
    crossSign.style.display = '';
}
function filterReviews(){
    let stars=''
    const checkboxes = document.querySelectorAll('.star-filter-input');
    checkboxes.forEach((checkbox) => {
        if (checkbox.checked){
            stars+=checkbox.value;
        }
    });
    reviewsURL = new URL(window.location.href);
    reviewsURL.searchParams.set('stars', stars);
    sort = document.querySelector('.sort').value
    reviewsURL.searchParams.set('sort', sort);
    fetch(reviewsURL,{
    method:'GET',
    headers:{
        'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Newtowk response was not correct');
        }
        return response.json();
    })
        .then(data => {
            document.querySelector(".review-list").innerHTML = data.html;
            window.history.pushState({},'',reviewsURL);
        })
        .catch(error => {
            console.error("Error: ",error);
        });
}