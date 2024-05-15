const productTypeSelect = document.getElementById('product_type');
const formContainer = document.getElementById('form_container');

productTypeSelect.addEventListener('change', (event) => {
  const selectedType = event.target.value;
  
 
  const url = `/get_form/?product_type=${selectedType}`; 
  
  fetch(url)
    .then(response => response.text())
    .then(html => {
      formContainer.innerHTML = html;
    });
});