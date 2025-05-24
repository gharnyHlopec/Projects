const changeQuantityUrl = "/cart/"
console.log(changeQuantityUrl)
function changeQuantity(productID,value){
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const response = fetch(changeQuantityUrl,{
        method:'POST',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken':csrfToken
        },
        body: JSON.stringify({
            'product_id':productID,
            'value':value
        })
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Newtowk response was not correct');
        }
        return response.json();
    })
    .then(data => {
        document.querySelector('.navbar-div').innerHTML = data.navbar_html;
        document.querySelector('.cart').innerHTML = data.cart_product_wrapper_html;
    })
    .catch(error => {
        console.error("Error: ",error);
    });
}
const deleteFromCartURL='/cart/'
function deleteFromCart(elemID){
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(deleteFromCartURL,{
        method:'POST',
        headers:{
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken':csrfToken
        },
        body:JSON.stringify({
            "product_id":elemID
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error("Newtowk response was not correct")
        }
        return response.json();
    })
    .then(data=>{
        document.querySelector('.navbar-div').innerHTML = data.navbar_html;
        document.querySelector('.cart').innerHTML = data.cart_product_wrapper_html;
    })
    .catch(error => {
        console.error('Error: ',error);
    });
}