    
        const searchButton = document.getElementById("search-button");
        const searchBox = document.getElementById("search-box");
        const closeButton = document.getElementById("close-search");
    
        searchButton.addEventListener("click", () => {
        searchBox.style.display = "block";
        });
    
        closeButton.addEventListener("click", () => {
        searchBox.style.display = "none";
        });
    
