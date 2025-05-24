
updateButtonStates()
setInterval(() => {
    const refreshOrdersURL = "/admin-panel/"
    fetch(refreshOrdersURL,{
        headers:{
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(".admin-panel-wrapper").innerHTML=data.html;
        updateButtonStates();
    });
},5000);

function changeOrderStatus(pk,action){
    acceptOrderURL= "/admin-panel/"
    const CSRFToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(acceptOrderURL,{
        method:'POST',
        headers:{
            'X-Requested-With':'XMLHttpRequest',
            "X-CSRFToken":CSRFToken
        },
        body:JSON.stringify({
            'action':action,
            'pk':pk
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error('Newtowk response was not correct');
        }else
        return response.json();
    })
    .then(data => {
        document.querySelector('.admin-panel-wrapper').innerHTML = data.html
        updateButtonStates()
    })
    .catch(error => {
        console.error("Error: ",error);
    });
}

function updateButtonStates(){    
    document.querySelectorAll('.active-orders').forEach(function(orderItem) {
    if (orderItem.querySelector('.warning')) {
        const button = orderItem.querySelector('.accept-button');
        button.style.display = 'none';
    }
});
}