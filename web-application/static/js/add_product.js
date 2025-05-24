function PostRequest(e){
    e.preventDefault();
    var product_type = document.getElementById("product_type").value;
    const csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const addProductURL = `/add_product/${product_type}`;
    const formData = new FormData(document.getElementById('object-form'));
    let properties = {};
    if (product_type == 'mouse'){
        properties = {
            type: document.getElementById('type').value,
            wireless: document.getElementById('wireless').value,
            sensor_type: document.getElementById('sensor_type').value,
            sensor_model: document.getElementById('sensor_model').value,
            sensor_resolution: document.getElementById('sensor_resolution').value,
            sensor_polling_rate: document.getElementById('sensor_polling_rate').value,
            case_material: document.getElementById('case_material').value,
            lighting: document.getElementById('lighting').value,
        }
    }
    if (product_type == 'keyboard'){
        properties = {
            type: document.getElementById('type').value,
            switch_type: document.getElementById('switch_type').value,
            switch_name: document.getElementById('switch_name').value,
            color: document.getElementById('color').value,
            cyrillic: document.getElementById('cyrillic').value,
            wireless: document.getElementById('wireless').value,
            cable_braid: document.getElementById('cable_braid').value,
        }
    }
    if (product_type == 'headphones'){
        properties = {
            type: document.getElementById('type').value,
            wireless: document.getElementById('wireless').value,
            protection: document.getElementById('protection').value,
            case_material: document.getElementById('case_material').value,
            headphones_color: document.getElementById('headphones_color').value,
            cable_color: document.getElementById('cable_color').value,
            ear_cushion_material: document.getElementById('ear_cushion_material').value,
        }
    }
    formData.append('json_data',JSON.stringify(properties));

    fetch(addProductURL,{
    method:'POST',
    headers:{
        'X-Requested-With':'XMLHttpRequest',
        'X-CSRFToken':csrf
    },
    body: formData,
    })
    .then(response => {
        if (!response.ok){
            throw new Error(`Ошибка: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.redirect){
            window.location.href = data.redirect
        } else{
        document.querySelector('.form-container').innerHTML = data.html;
        for (let key in properties) {
            document.getElementById(key).value = properties[key];
        }
        transferFiles();
        }
    })
    .catch(error => {
        console.error("Ошибка: ",error);
    });
}

function changeForm(product_type){
    const addProductURL = `/add_product/${product_type}`;
    fetch(addProductURL, {
        method:'GET',
        headers:{
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok){
            console.error('Ошибка:', response.status, response.statusText);
            return response.text().then(text => {
                throw new Error(`Ошибка: ${response.status} - ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        document.querySelector('.form-container').innerHTML = data.html;
        transferFiles()
        window.history.pushState({},'',addProductURL);
    })        
    .catch(error => {
        console.error("Ошибка: ",error);
    });
};

let uploadedFiles = [];

let dropArea = document.querySelector('.image-drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})


function preventDefaults(e){
    e.preventDefault()
    e.stopPropagation()
}

;['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
})


;['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
})

function highlight(e) {
    dropArea.classList.add('highlight')
}


function unhighlight(e) {
    dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false)


function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    handleFiles(files)
}

function handleFiles(files) {
    files = [...files] 
    files.forEach(previewFile)
    uploadedFiles.push(...files);
    transferFiles()
}

function previewFile(file) {
    let reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = function() {
        let img = document.createElement('img')
        img.src = reader.result
        img.name = file.name;
        img.onclick = function(){
            deleteImage(img);
        };
        img.draggable = false
        document.getElementById('gallery').appendChild(img);
    }
}

function deleteImage(image_to_delete){
    const images = document.querySelectorAll("#gallery img")
    images.forEach((image) => {
        if(image.name === image_to_delete.name) {image.remove();}
    })
    uploadedFiles = uploadedFiles.filter(file => file.name !== image_to_delete.name);
    transferFiles()
}

function transferFiles(){
    const dataTransfer = new DataTransfer();

    uploadedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });
    const input = document.getElementById('image-input');
    input.files = dataTransfer.files;
}