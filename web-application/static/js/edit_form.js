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
function displayImagePreview(file) { 
  const reader = new FileReader(); 
  reader.onload = function (e) { 
    const imageContainer = document.createElement('div'); 
    imageContainer.classList.add('image-container'); 
    const img = document.createElement('img'); 
    img.src = e.target.result; 
    imageContainer.appendChild(img); 
    const deleteButton = document.createElement('button'); 
    deleteButton.textContent = 'Удалить'; 
    deleteButton.classList.add('delete-button'); 
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