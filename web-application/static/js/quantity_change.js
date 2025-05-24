const addToCartUrl = "/add-to-cart/";
function addToCart(productID, quantity){
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const response = fetch(addToCartUrl,{
        method:'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken':csrfToken
        },
        body: JSON.stringify({
            'product_id':productID,
            'quantity':quantity
        })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Ошибка:', response.status, response.statusText);
            return response.text().then(text => {
                throw new Error(`Ошибка: ${response.status} - ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        document.querySelector('.navbar-div').innerHTML = data.navbar_html;
        document.querySelector(`.product-${productID}`).innerHTML = data.quantity_html;
        if (document.querySelector(`.quantity-change-product-${productID}`)){
            document.querySelector(`.add-to-cart-product-${productID}`).style.display='none';
        }
        else{
            document.querySelector(`.add-to-cart-product-${productID}`).style.display='';
        }
    })
    .catch(error => {
        console.error("Ошибка: ",error);
    });
}
