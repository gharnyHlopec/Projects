document.addEventListener('DOMContentLoaded', (event) => {
  const minPriceInput = document.getElementById('min_price');
  const maxPriceInput = document.getElementById('max_price');
  const minYearInput = document.getElementById('min_year');
  const maxYearInput = document.getElementById('max_year');
  const availabilitySelect = document.getElementById('availability');
  const sortSelect = document.getElementById('sort');

  
  const savedAvailability = localStorage.getItem('availability');
  if (savedAvailability) {
    availabilitySelect.value = savedAvailability;
  }

  function updateCatalog(event) {
    if (event.type === 'keydown' && event.key !== 'Enter') {
      return;
    }

    event.preventDefault();

    const minPrice = minPriceInput.value;
    const maxPrice = maxPriceInput.value;
    const minYear = minYearInput.value;
    const maxYear = maxYearInput.value;
    const availability = availabilitySelect.value;
    const sort = sortSelect.value;

    const currentUrl = new URL(window.location.href);

    currentUrl.searchParams.set('min_price', minPrice);
    currentUrl.searchParams.set('max_price', maxPrice);
    currentUrl.searchParams.set('min_year', minYear);
    currentUrl.searchParams.set('max_year', maxYear);
    currentUrl.searchParams.set('availability', availability);
    currentUrl.searchParams.set('sort', sort);

  
    localStorage.setItem('availability', availability);

    window.location.href = currentUrl.href;
  }

  minPriceInput.addEventListener('keydown', updateCatalog);
  maxPriceInput.addEventListener('keydown', updateCatalog);
  minYearInput.addEventListener('keydown', updateCatalog);
  maxYearInput.addEventListener('keydown', updateCatalog);
  availabilitySelect.addEventListener('change', updateCatalog);
  sortSelect.addEventListener('change', updateCatalog);
});
  