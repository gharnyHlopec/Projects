    const dropArea = document.getElementById('image-drop-area');
    const fileInput = document.getElementById('images');
    const imagePreview = document.getElementById('image-preview');

    

   
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

  
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

 
    dropArea.addEventListener('drop', handleDrop, false);

 
    dropArea.addEventListener('click', () => {
    fileInput.click(); 
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropArea.classList.add('highlight');
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }

    function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    imagePreview.innerHTML = ''; 
    handleFiles(files);
    }

    function handleFiles(files) {
    for (const file of files) {
        displayImagePreview(file);
    }
 
    fileInput.files = files;
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

     
        imagePreview.innerHTML = '';

        handleFiles(files);
    }

    function handleFiles(files) {
        for (const file of files) {
            displayImagePreview(file);
            
            fileInput.files = files; 
        }
    }

    
    function displayImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imageContainer = document.createElement('div');
            imageContainer.style.position = 'relative';
            imageContainer.style.display = 'inline-block'; 
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '100px';
            img.style.maxHeight = '100px';
            img.style.marginRight = '10px';
            imageContainer.appendChild(img);
            
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить';
            deleteButton.style.position = 'absolute';
            deleteButton.style.top = '50%';
            deleteButton.style.left = '50%';
            deleteButton.style.transform = 'translate(-50%, -50%)'; 
            deleteButton.style.backgroundColor = 'rgba(255, 0, 0, 0.7)';
            deleteButton.style.color = 'white';
            deleteButton.style.border = 'none';
            deleteButton.style.padding = '8px 16px';
            deleteButton.style.borderRadius = '5px';
            deleteButton.style.cursor = 'pointer';
            deleteButton.style.opacity = 0; 
            deleteButton.style.transition = 'opacity 0.3s ease'; 
            
            imageContainer.addEventListener('mouseover', () => {
                deleteButton.style.opacity = 1; 
            });
            imageContainer.addEventListener('mouseout', () => {
                deleteButton.style.opacity = 0; 
            });
            
            deleteButton.addEventListener('click', (e) => {
                e.stopPropagation(); 
                imagePreview.removeChild(imageContainer); 
               
                const files = Array.from(fileInput.files); 
                const index = files.indexOf(file); 
                files.splice(index, 1); 
                
                const newDt = new DataTransfer();
                files.forEach(f => newDt.items.add(f));
                
                fileInput.files = newDt.files;
            });
            imageContainer.appendChild(deleteButton);
            imagePreview.appendChild(imageContainer);
        };
        reader.readAsDataURL(file);
    }

    fileInput.addEventListener('change', (e) => {
    imagePreview.innerHTML = ''; 
    handleFiles(e.target.files);
    });

    
    productTypeSelect.addEventListener('change', () => {
    
    fileInput.files = new DataTransfer().files; 

    
    imagePreview.innerHTML = ''; 
    });