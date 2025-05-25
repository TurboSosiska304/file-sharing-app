document.getElementById('uploadForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (!files.length) {
        showMessage('Please select at least one file to upload.', false);
        return;
    }

    const formData = new FormData();
    let totalSize = 0;
    
    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
        totalSize += files[i].size;
    }

    const progressContainer = document.getElementById('progressContainer');
    progressContainer.style.display = 'block';

    const progressPercent = document.getElementById('progressPercent');
    const progressBar = document.getElementById('progressBar');
    const uploadSpeed = document.getElementById('uploadSpeed');
    const uploadedSize = document.getElementById('uploadedSize');
    const totalSizeElement = document.getElementById('totalSize');

    totalSizeElement.textContent = (totalSize / (1024 * 1024)).toFixed(2) + ' MB';

    const xhr = new XMLHttpRequest();
    let startTime = null;

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            progressPercent.textContent = percentComplete.toFixed(1) + '%';
            progressBar.style.width = percentComplete + '%';
            uploadedSize.textContent = (event.loaded / (1024 * 1024)).toFixed(2) + ' MB';

            if (!startTime) startTime = Date.now();
            const elapsedTime = (Date.now() - startTime) / 1000;
            const speed = event.loaded / (1024 * 1024 * elapsedTime);
            uploadSpeed.textContent = speed.toFixed(2) + ' MB/s';
        }
    };

    xhr.onload = function() {
        progressContainer.style.display = 'none';
        const response = JSON.parse(xhr.responseText);
        showMessage(response.message, response.success);
    };

    xhr.onerror = function() {
        progressContainer.style.display = 'none';
        showMessage('An error occurred during the upload.', false);
    };

    xhr.open('POST', '/upload', true);
    xhr.send(formData);
});

// Функция для отображения сообщений
function showMessage(message, isSuccess) {
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.textContent = message;
    messageContainer.className = isSuccess ? 'success' : '';
}

// Обработчик для кнопок удаления
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn')) {
        const filename = e.target.getAttribute('data-filename');
        fetch(`/delete/${filename}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            showMessage(data.message, data.success);
            if (data.success) {
                const li = e.target.parentElement;
                const ul = li.parentElement;
                li.remove();
                if (!ul.children.length) {
                    const emptyLi = document.createElement('li');
                    emptyLi.textContent = 'No files in this category.';
                    ul.appendChild(emptyLi);
                }
            }
        })
        .catch(error => {
            showMessage('Error deleting file.', false);
        });
    }
});