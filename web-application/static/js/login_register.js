function login(event,operation){
    event.preventDefault();
    const csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const formData = new FormData(document.getElementById(`${operation}-form`));
    loginURL = `/${operation}/`
    fetch(loginURL,{
        method:'POST',
        headers:{
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken':csrf
        },
        body:formData,
    })
    .then(response => {
        if(!response.ok){
            throw new Error(`Ошибка: ${response.status} - ${response.statusText}`);
        } else return response.json();
    })
    .then(data => {
        if (data.redirect){
                window.location.href = data.redirect
            } 
        else {
            document.querySelector(`.${operation}-container`).innerHTML = data.html;
            if (operation == 'login'){
            document.querySelector('input[name="email"]').value = formData.get('email');
            }
        }
    })
    .catch(error => {
        console.error("Error: ",error);
    });
}