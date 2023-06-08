function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function(){
        var output = document.getElementById('original-image');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
};
function validateForm() {
    var fileInput = document.getElementById('file-input');
    if (fileInput.files.length === 0) {
        var errorContainer = document.getElementById('error-message');
        errorContainer.textContent = "Please select an image.";
        return false;
    }
    return true;
}