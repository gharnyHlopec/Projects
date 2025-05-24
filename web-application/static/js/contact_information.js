document.querySelector('#order_form').addEventListener('submit', function(event){
    let payment_status = document.getElementById('payment_status').value.trim();
    if (!payment_status){
        event.preventDefault(); 
        alert('Выберите способ оплаты');
    }
})

function openCart(){
    window.location.href='/cart'
}