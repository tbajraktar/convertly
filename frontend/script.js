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

const viewPricing = document.getElementById('view-pricing');
const pricingModal = document.getElementById('pricing-modal');
const closePricingBtn = document.getElementById('close-pricing');
const continueFreeBtn = document.getElementById('continue-free');

// State management
let isPro = localStorage.getItem('convertly_pro') === 'true';

// Update UI based on Pro Status
function updateProUI() {
    if (isPro) {
        document.querySelector('.logo').innerHTML += ' <span class="badge-free" style="margin-left:5px; font-size:0.6em; padding: 2px 8px;">PRO</span>';
        if (subscribeProBtn) {
            subscribeProBtn.innerText = 'Subscribed';
            subscribeProBtn.classList.remove('primary');
            subscribeProBtn.classList.add('secondary');
            subscribeProBtn.disabled = true;
        }
    }
}
updateProUI();

// Navigation & Modal Handlers
viewPricing.addEventListener('click', (e) => {
    e.preventDefault();
    pricingModal.style.display = 'flex';
});

closePricingBtn.addEventListener('click', () => {
    pricingModal.style.display = 'none';
});

continueFreeBtn.addEventListener('click', () => {
    pricingModal.style.display = 'none';
});

// PayPal Button Integration
if (window.paypal) {
    paypal.Buttons({
        style: {
            layout: 'vertical',
            color: 'blue',
            shape: 'rect',
            label: 'paypal'
        },
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: '2.00',
                        currency_code: 'USD'
                    },
                    description: 'Convertly Pro - 1 Month Subscription'
                }]
            });
        },
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (orderData) {
                // Successful payment
                isPro = true;
                localStorage.setItem('convertly_pro', 'true');
                alert('Payment Successful! You are now a Pro member.');
                pricingModal.style.display = 'none';
                updateProUI();
            });
        },
        onError: function (err) {
            console.error('PayPal Error:', err);
            alert('An error occurred with the PayPal payment. Please try again.');
        }
    }).render('#paypal-button-container');
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === adModal) adModal.style.display = 'none';
    if (e.target === pricingModal) pricingModal.style.display = 'none';
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
    // Since we now serve frontend and backend from the same port (8000), 
    // we can use a simpler URL logic.
    const apiUrl = window.location.origin === 'null' ? 'http://localhost:8000/remove-bg' : `${window.location.origin}/remove-bg`;

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
                if (isPro) {
                    triggerDownload(currentProcessedBlob, `convertly-pro-${Date.now()}.png`);
                } else {
                    showAdAndDownload();
                }
            };

            downloadWatermarkBtn.onclick = () => {
                if (isPro) {
                    // Pro users get clean download even if they click watermark button
                    triggerDownload(currentProcessedBlob, `convertly-pro-${Date.now()}.png`);
                } else {
                    downloadWithWatermark();
                }
            };
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the image.');
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

function downloadWithWatermark() {
    if (!currentProcessedBlob) return;

    const img = new Image();
    img.src = URL.createObjectURL(currentProcessedBlob);

    img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = img.width;
        canvas.height = img.height;

        // Draw the main image
        ctx.drawImage(img, 0, 0);

        // Add watermark
        ctx.font = `${Math.max(20, img.width / 20)}px Inter`;
        ctx.fillStyle = 'rgba(255, 105, 180, 0.5)'; // Pink semi-transparent
        ctx.textAlign = 'right';
        ctx.textBaseline = 'bottom';

        const padding = img.width / 30;
        ctx.fillText('CONVERTLY', img.width - padding, img.height - padding);

        // Download from canvas
        canvas.toBlob((blob) => {
            triggerDownload(blob, `convertly-free-${Date.now()}.png`);
        }, 'image/png');

        URL.revokeObjectURL(img.src);
    };
}

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
