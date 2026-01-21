document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    const resultContent = document.getElementById('resultContent');

    // Click on upload zone to trigger file input
    uploadZone.addEventListener('click', function() {
        fileInput.click();
    });

    // Click on upload button to trigger file input
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Drag and drop handlers
    uploadZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    function handleFileUpload(file) {
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            alert('Please upload a JPG, PNG, or WebP image.');
            return;
        }

        // Show loading state
        resultContent.innerHTML = '<div class="placeholder-message"><p>Processing image...</p></div>';

        // Create FormData
        const formData = new FormData();
        formData.append('file', file);

        // Upload file
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResult(data);
            } else {
                resultContent.innerHTML = `<div class="placeholder-message"><p style="color: #ef4444;">Error: ${data.error || 'Upload failed'}</p></div>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultContent.innerHTML = `<div class="placeholder-message"><p style="color: #ef4444;">Error uploading file. Please try again.</p></div>`;
        });
    }

    function displayResult(data) {
        resultContent.innerHTML = `
            <img src="${data.image_url}" alt="Uploaded image" class="result-image">
            <div class="prediction-label">${data.prediction}</div>
            <div class="confidence-score">Confidence: ${data.confidence}</div>
            <div class="prediction-description">${data.description}</div>
        `;
    }
});
