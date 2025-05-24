function changePage(newPage) {
if(newPage != '...'){
    const url = new URL(window.location.href);
    url.searchParams.set('page', newPage);
    fetchData(url)
    checkButtonsAfterCatalogRefresh()
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}
}
function checkButtonsAfterCatalogRefresh(){
    document.querySelectorAll('.quantity-change').forEach(elem => {
    classes = elem.classList;
    last_class = elem.classList[classes.length-1];
    numbers = last_class.split('-');
    last_number = numbers[numbers.length-1];
    if (document.querySelector(`.quantity-change-product-${last_number}`)){
        document.querySelector(`.add-to-cart-product-${last_number}`).style.display='none';
        }
    else{
        document.querySelector(`.add-to-cart-product-${last_number}`).style.display='';
        }

    })
}
checkButtonsAfterCatalogRefresh()
const homeContainer = document.querySelector('.home-container');
const filterContainer = document.querySelector('.filter-form');
const filterIcon = document.querySelector('.filter-icon');
const closeIcon = document.querySelector('.close-icon');
const pagination = document.querySelector('.pagination')

function openFilters(){
    filterContainer.classList.add('opened');
}

filterContainer.addEventListener('click',(event) => {
    if (event.target === filterContainer){
        closeFilters()
    }
})

function closeFilters(){
    filterContainer.classList.remove('opened');
}

window.addEventListener('resize',changeLayout)
changeLayout()
function changeLayout(){

    if (window.innerWidth <= 665){
        filterIcon.style.display = '';
        document.querySelector('.product-grid').style.gridTemplateColumns = 'repeat(2, 1fr)';
        filterContainer.classList.add('closed');
        homeContainer.classList.add('modified');
    } else if (665 < window.innerWidth && window.innerWidth<= 750){
        filterIcon.style.display = 'none';
        filterContainer.classList.remove('closed');
        homeContainer.classList.remove('modified');
        filterContainer.classList.remove('opened');
        document.querySelector('.product-grid').style.gridTemplateColumns = 'repeat(2, 1fr)';
    } else if (750 < window.innerWidth){
        filterIcon.style.display = 'none';
        filterContainer.classList.remove('closed');
        homeContainer.classList.remove('modified');
        filterContainer.classList.remove('opened');
        document.querySelector('.product-grid').style.gridTemplateColumns = 'repeat(3, 1fr)';
    }
}


function fetchData(url){
    fetch(url,{
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
        document.querySelector('.product-grid-and-pagination').innerHTML = data.html;
        changeLayout()
        checkButtonsAfterCatalogRefresh()
        window.history.pushState({},'',url);
    })
    .catch(error => {
        console.error("Error: ",error);
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    const inputs = [
        document.getElementById('min_price'),
        document.getElementById('max_price'),
        document.getElementById('min_year'),
        document.getElementById('max_year'),
        document.getElementById('availability'),
        document.getElementById('sort')
    ];

    function updateCatalog(event) {

        const currentUrl = new URL(window.location.href);
        inputs.forEach(input => {
            currentUrl.searchParams.set(input.id, input.value);
        });
        currentUrl.searchParams.set('page', 1);

        fetchData(currentUrl.href)
    }

    inputs.forEach(input => {
        input.addEventListener('change', updateCatalog);  
    });
});

function resetFilters(){
    const currentUrl = new URL(window.location.href);
        
    const inputs = [
        document.getElementById('min_price'),
        document.getElementById('max_price'),
        document.getElementById('min_year'),
        document.getElementById('max_year'),
        document.getElementById('availability'),
        document.getElementById('sort')
    ];

    inputs.forEach(input => {
        if (input.id === 'availability'){
            input.value = -1;
        } else{
            input.value = '';
        }
    });
    inputs.forEach(input => {
        currentUrl.searchParams.set(input.id,input.value); 
    });
    currentUrl.searchParams.set('page', 1);
    fetchData(currentUrl.href);
}