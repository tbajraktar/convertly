const fileInput = document.getElementById('file-input');
const uploadContainer = document.getElementById('upload-container');
const uploadContent = document.getElementById('upload-content');
const processingContent = document.getElementById('processing-content');
const resultContent = document.getElementById('result-content');
const resultImage = document.getElementById('result-image');
const downloadHdBtn = document.getElementById('download-hd-btn');
const downloadWatermarkBtn = document.getElementById('download-watermark-btn');
const resetBtn = document.getElementById('reset-btn');
const adModal = document.getElementById('ad-modal');
const adTimer = document.getElementById('ad-timer');
const closeAdBtn = document.getElementById('close-ad');

// Navigation & Modal Handlers (Pricing Removed)

// State management
// Pro Status & Pricing Logic Removed

// PayPal Button Integration
// PayPal Integration Removed

// Close modals when clicking outside
// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === adModal) adModal.style.display = 'none';
});

let currentProcessedBlob = null;

// Drag and drop handling
uploadContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadContainer.classList.add('dragover');
});

uploadContainer.addEventListener('dragleave', () => {
    uploadContainer.classList.remove('dragover');
});

uploadContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadContainer.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file.');
        return;
    }

    // Show processing state
    uploadContent.style.display = 'none';
    processingContent.style.display = 'flex';

    // Create FormData
    const formData = new FormData();
    formData.append('file', file);

    // Send to backend
    // Determine API URL
    let apiUrl = `${window.location.origin}/remove-bg`;
    if (window.location.origin === 'null' || window.location.protocol === 'file:') {
        apiUrl = 'http://127.0.0.1:8000/remove-bg';
    }
    console.log('Uploading to:', apiUrl);

    fetch(apiUrl, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.blob();
        })
        .then(blob => {
            currentProcessedBlob = blob;
            // Create URL for the result image
            const url = URL.createObjectURL(blob);
            resultImage.src = url;

            // Show result state
            processingContent.style.display = 'none';
            resultContent.style.display = 'flex';

            // Setup download buttons
            downloadHdBtn.onclick = () => {
                showAdAndDownload();
            };

            downloadWatermarkBtn.onclick = () => {
                // Standard download (No watermark now)
                triggerDownload(currentProcessedBlob, `convertly-standard-${Date.now()}.png`);
            };
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error: ${error.message}. Ensure the backend is running.`);
            resetUI();
        });
}

function showAdAndDownload() {
    adModal.style.display = 'flex';
    let count = 5;
    adTimer.innerText = count;

    const interval = setInterval(() => {
        count--;
        adTimer.innerText = count;
        if (count <= 0) {
            clearInterval(interval);
            adModal.style.display = 'none';
            triggerDownload(currentProcessedBlob, `convertly-hd-${Date.now()}.png`);
        }
    }, 1000);

    closeAdBtn.onclick = () => {
        clearInterval(interval);
        adModal.style.display = 'none';
    };
}

// downloadWithWatermark function Removed

function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 100);
}

resetBtn.addEventListener('click', resetUI);

function resetUI() {
    resultContent.style.display = 'none';
    processingContent.style.display = 'none';
    uploadContent.style.display = 'flex';
    fileInput.value = '';
    currentProcessedBlob = null;

    if (resultImage.src) {
        URL.revokeObjectURL(resultImage.src);
        resultImage.src = '';
    }

}

// Footer Toggle
const footerToggleBtn = document.getElementById('footer-toggle-btn');
const footerDirectory = document.getElementById('footer-directory');
const footerToggleIcon = document.getElementById('footer-toggle-icon');

if (footerToggleBtn && footerDirectory) {
    footerToggleBtn.addEventListener('click', () => {
        const isHidden = footerDirectory.style.display === 'none';
        footerDirectory.style.display = isHidden ? 'block' : 'none';
        footerToggleIcon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
    });
}
