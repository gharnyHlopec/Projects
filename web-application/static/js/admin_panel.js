updateButtonStates()
setInterval(() => {
    const refreshOrdersURL = "/admin-panel/";
    fetch(refreshOrdersURL,{
        headers:{
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#in_progress').innerHTML = data.html1;
        document.querySelector('#ended').innerHTML = data.html2;
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
        document.querySelector('#in_progress').innerHTML = data.html1
        document.querySelector('#ended').innerHTML = data.html2
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

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const tabId = tab.getAttribute('data-tab');
            tabContents.forEach(content => {
                if (content.id === tabId) {
                    content.classList.add('active');
                } else {
                    content.classList.remove('active');
                }
            });
        });
    });
});