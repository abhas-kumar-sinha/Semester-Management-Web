// Get input, text, and preview elements
const imageInput = document.getElementById('imageInput');
const fileText = document.getElementById('fileText');
const imagePreview = document.querySelector('.img-container');

// Update text and preview when file is chosen
imageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    const fileName = file ? file.name : 'No file chosen';
    fileText.textContent = fileName;

    // If a file is selected, display it as the background
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imagePreview.style.backgroundImage = `url('${e.target.result}')`;
        };

        reader.readAsDataURL(file);
    } else {
        imagePreview.style.backgroundImage = 'none';
    }
});