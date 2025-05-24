setInterval(() => {
    const refreshOrdersURL = "/user-orders/"
    fetch(refreshOrdersURL,{
        headers:{
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(".user-orders-wrapper").innerHTML = data.html;
        updateButtonStates();
    });
},5000);