const fileInput = document.getElementById('file-input');
const uploadContainer = document.getElementById('upload-container');
const uploadContent = document.getElementById('upload-content');
const processingContent = document.getElementById('processing-content');
// const resultContent = document.getElementById('result-content'); // REMOVED
// const resultImage = document.getElementById('result-image'); // REMOVED
// const downloadHdBtn = document.getElementById('download-hd-btn'); // REMOVED
// const downloadWatermarkBtn = document.getElementById('download-watermark-btn'); // REMOVED
const resetBtn = document.getElementById('reset-btn');
const adModal = document.getElementById('ad-modal');
const adTimer = document.getElementById('ad-timer');
const closeAdBtn = document.getElementById('close-ad');

// Navigation & Modal Handlers (Pricing Removed)

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

// Drop handler moved to bottom to support batch

fileInput.addEventListener('change', (e) => {
    // Handler moved to bottom
});


/* Image Editor Class */
class ImageEditor {
    constructor() {
        this.canvas = document.getElementById('editor-canvas');
        this.ctx = this.canvas.getContext('2d');

        this.cutoutImage = null; // The subject (foreground)
        this.maskCanvas = document.createElement('canvas'); // Offscreen mask
        this.maskCtx = this.maskCanvas.getContext('2d');

        this.bgImage = null; // Custom background image
        this.bgColor = 'transparent';

        // Transform State
        this.rotation = 0;
        this.scaleX = 1; // For flip

        // Manual Tool State
        this.brushSize = 20;
        this.isDrawing = false;
        this.mode = 'erase';
        this.lastX = 0;
        this.lastY = 0;

        this.initEventListeners();
        this.initCanvasEvents();
    }

    initEventListeners() {
        // Tab Switching & Tools logic (Keep existing)
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tool-group').forEach(g => g.classList.remove('active'));

                btn.classList.add('active');
                document.getElementById(`tool-${btn.dataset.tab}`).classList.add('active');
            });
        });

        // Background Tools
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (btn.classList.contains('custom')) return;
                this.bgColor = btn.dataset.color;
                this.bgImage = null;
                this.updateColorActiveState(btn);
                this.render();
            });
        });

        const colorPicker = document.getElementById('custom-color-picker');
        colorPicker.addEventListener('input', (e) => {
            this.bgColor = e.target.value;
            this.bgImage = null;
            this.render();
        });

        const bgInput = document.getElementById('bg-file-input');
        bgInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                const url = URL.createObjectURL(e.target.files[0]);
                const img = new Image();
                img.onload = () => {
                    this.bgImage = img;
                    this.render();
                };
                img.src = url;
            }
        });

        // Manual Tools
        document.querySelectorAll('.tool-btn[data-mode]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tool-btn[data-mode]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.mode = btn.dataset.mode;
            });
        });

        document.getElementById('brush-size').addEventListener('input', (e) => {
            this.brushSize = parseInt(e.target.value, 10);
        });

        // Transform Tools
        document.getElementById('rotate-left').onclick = () => { this.rotation -= 90; this.render(); };
        document.getElementById('rotate-right').onclick = () => { this.rotation += 90; this.render(); };
        document.getElementById('flip-h').onclick = () => { this.scaleX *= -1; this.render(); };

        // Download
        document.getElementById('download-btn').onclick = () => this.download();
        document.getElementById('download-hd-btn').onclick = () => this.startAdFlow();
        document.getElementById('download-std-btn').onclick = () => this.downloadWithSmartLink();

        // Environment Detection
        this.checkEnvironment();

        // Ad Modal Logic
        document.getElementById('close-ad').onclick = () => {
            document.getElementById('ad-modal').style.display = 'none';
            if (this.adInterval) clearInterval(this.adInterval);
        };
    }

    startAdFlow() {
        const modal = document.getElementById('ad-modal');
        const timerDisplay = document.getElementById('ad-timer');
        let timeLeft = 5;

        modal.style.display = 'flex';
        timerDisplay.innerText = timeLeft;

        if (this.adInterval) clearInterval(this.adInterval);

        this.adInterval = setInterval(() => {
            timeLeft--;
            timerDisplay.innerText = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(this.adInterval);
                modal.style.display = 'none';
                this.download();
            }
        }, 1000);
    }

    checkEnvironment() {
        const urlParams = new URLSearchParams(window.location.search);
        const isDesktopApp = urlParams.get('app') === 'desktop';

        if (!isDesktopApp) {
            // Website Mode (Any environment NOT explicitly marked as desktop app)
            document.getElementById('download-btn').style.display = 'none';
            document.getElementById('download-hd-btn').style.display = 'inline-flex';
            document.getElementById('download-std-btn').style.display = 'inline-flex';
        } else {
            // Desktop App Mode
            document.getElementById('download-btn').style.display = 'inline-flex';
            document.getElementById('download-hd-btn').style.display = 'none';
            document.getElementById('download-std-btn').style.display = 'none';
        }
    }

    initCanvasEvents() {
        // Mouse Events
        this.canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
        this.canvas.addEventListener('mousemove', (e) => this.draw(e));
        this.canvas.addEventListener('mouseup', () => this.stopDrawing());
        this.canvas.addEventListener('mouseout', () => this.stopDrawing());

        // Touch Events
        this.canvas.addEventListener('touchstart', (e) => { e.preventDefault(); this.startDrawing(e.touches[0]); });
        this.canvas.addEventListener('touchmove', (e) => { e.preventDefault(); this.draw(e.touches[0]); });
        this.canvas.addEventListener('touchend', () => this.stopDrawing());
    }

    getMousePos(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;

        // We need to map screen coordinates to the *untransformed* subject space?
        // Actually, drawing happens in "screen space" over the canvas, but applies to the Mask.
        // The Mask is attached to the Subject.
        // This is tricky if the subject is Rotated. 
        // For simplicity V1: Disable drawing if rotated? Or map coordinates inversed.
        // Let's rely on mapping coordinates relative to center if we want to support rotation, 
        // OR simplified: Apply drawing to an "Overlay Mask" that is NOT rotated?
        // No, if I rotate the subject, the erase marks should follow.
        // So I must draw on the `maskCanvas`.
        // To do that, I need to transform the mouse coordinates back into the `maskCanvas` local space.

        let x = (e.clientX - rect.left) * scaleX;
        let y = (e.clientY - rect.top) * scaleY;

        // Inverse Transform Logic
        const cx = this.canvas.width / 2;
        const cy = this.canvas.height / 2;

        // Translate to center
        let dx = x - cx;
        let dy = y - cy;

        // Inverse Scale (Flip)
        dx = dx * this.scaleX;

        // Inverse Rotate
        const rad = -this.rotation * Math.PI / 180;
        const rx = dx * Math.cos(rad) - dy * Math.sin(rad);
        const ry = dx * Math.sin(rad) + dy * Math.cos(rad);

        // Translate back
        return {
            x: rx + cx,
            y: ry + cy
        };
    }

    startDrawing(e) {
        this.isDrawing = true;
        const pos = this.getMousePos(e);
        this.lastX = pos.x;
        this.lastY = pos.y;
        this.draw(e); // Draw single dot on click
    }

    draw(e) {
        if (!this.isDrawing) return;

        const pos = this.getMousePos(e);

        this.maskCtx.lineWidth = this.brushSize;
        this.maskCtx.lineCap = 'round';
        this.maskCtx.lineJoin = 'round';

        if (this.mode === 'erase') {
            this.maskCtx.globalCompositeOperation = 'destination-out';
            this.maskCtx.strokeStyle = 'rgba(0,0,0,1)';
        } else {
            this.maskCtx.globalCompositeOperation = 'source-over';
            this.maskCtx.strokeStyle = 'rgba(0,0,0,1)';
        }

        this.maskCtx.beginPath();
        this.maskCtx.moveTo(this.lastX, this.lastY);
        this.maskCtx.lineTo(pos.x, pos.y);
        this.maskCtx.stroke();

        this.lastX = pos.x;
        this.lastY = pos.y;

        this.render();
    }

    stopDrawing() {
        this.isDrawing = false;
    }

    updateColorActiveState(activeBtn) {
        document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
        activeBtn.classList.add('active');
    }

    loadImage(blob) {
        const url = URL.createObjectURL(blob);
        const img = new Image();
        img.onload = () => {
            this.cutoutImage = img;
            // Reset State
            this.rotation = 0;
            this.scaleX = 1;
            this.bgColor = 'transparent';
            this.bgImage = null;
            this.mode = 'erase';

            // Set Canvas Size
            this.canvas.width = img.width;
            this.canvas.height = img.height;

            // Init Mask
            this.maskCanvas.width = img.width;
            this.maskCanvas.height = img.height;
            this.maskCtx.fillStyle = 'black'; // Solid mask
            this.maskCtx.fillRect(0, 0, img.width, img.height);

            this.render();

            // Switch UI
            document.getElementById('upload-content').style.display = 'none';
            document.getElementById('processing-content').style.display = 'none';
            document.getElementById('editor-container').style.display = 'flex';
        };
        img.onerror = () => {
            alert("Error loading processed image. The response might not be a valid image.");
            document.getElementById('processing-content').style.display = 'none';
            document.getElementById('upload-content').style.display = 'flex';
        };
        img.src = url;
    }

    render() {
        if (!this.cutoutImage) return;

        const w = this.canvas.width;
        const h = this.canvas.height;

        // Clear Main Canvas
        this.ctx.clearRect(0, 0, w, h);

        // 1. Draw Background (Static, fills constrained aspect ratio if needed, here fills full canvas)
        this.ctx.save();
        if (this.bgImage) {
            this.ctx.drawImage(this.bgImage, 0, 0, w, h);
        } else if (this.bgColor !== 'transparent') {
            this.ctx.fillStyle = this.bgColor;
            this.ctx.fillRect(0, 0, w, h);
        }
        this.ctx.restore();

        // 2. Composite Subject + Mask
        // We create a temporary canvas to merge Subject AND Mask, then draw that temp result transformed
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = w;
        tempCanvas.height = h;
        const tempCtx = tempCanvas.getContext('2d');

        // Draw Subject
        tempCtx.drawImage(this.cutoutImage, 0, 0);

        // Mask it (The mask is: Black=Keep, Transparent=Cut)
        // Wait, mask logic:
        // 'erase' -> removes from mask. 
        // To mask the original image:
        // Draw Image.
        // GlobalComposite 'destination-in' -> Draw Mask.
        // If Mask is Solid Black -> Image Kept.
        // If Mask is Transparent -> Image Deleted.
        tempCtx.globalCompositeOperation = 'destination-in';
        tempCtx.drawImage(this.maskCanvas, 0, 0);

        // 3. Draw Composite to Main Canvas (With Transforms)
        this.ctx.save();
        this.ctx.translate(w / 2, h / 2);
        this.ctx.rotate(this.rotation * Math.PI / 180);
        this.ctx.scale(this.scaleX, 1);
        this.ctx.drawImage(tempCanvas, -w / 2, -h / 2);
        this.ctx.restore();
    }

    download() {
        const link = document.createElement('a');
        link.download = `convertly-edit-${Date.now()}.png`;
        link.href = this.canvas.toDataURL('image/png');
        link.click();
    }

    downloadWithSmartLink() {
        console.log("Triggering Smart Link Download...");

        // Open Smart Link (using anchor click to avoid popup blockers)
        const smartLink = document.createElement('a');
        smartLink.href = 'https://controlslaverystuffing.com/vwz6ieynnt?key=6826f59154b57a96baa665a28b70fd19';
        smartLink.target = '_blank'; // New Tab
        smartLink.rel = 'noopener noreferrer';
        document.body.appendChild(smartLink);
        smartLink.click();

        // Small delay to ensure the first click registers before the second
        setTimeout(() => {
            document.body.removeChild(smartLink);
            this.download();
        }, 100);
    }
}

const editor = new ImageEditor();

// Batch Processing Logic
const batchContainer = document.getElementById('batch-container');
const batchList = document.getElementById('batch-list');
let batchQueue = [];
let isProcessingBatch = false;

function handleFile(file) {
    // Single file mode
    uploadContent.style.display = 'none';
    processingContent.style.display = 'flex';
    processFile(file)
        .then(blob => {
            editor.loadImage(blob);
        })
        .catch(err => {
            console.error(err);
            alert("Error processing image: " + err.message);
            // Reset UI
            uploadContent.style.display = 'flex';
            processingContent.style.display = 'none';
            document.getElementById('file-input').value = '';
        });
}

// Override drag drop to support both single and batch
uploadContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadContainer.classList.remove('dragover');

    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));

    if (files.length === 0) return;

    if (files.length === 1) {
        handleFile(files[0]);
    } else {
        startBatch(files);
    }
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 1) {
        handleFile(files[0]);
    } else if (files.length > 1) {
        startBatch(files);
    }
});
// Enable multiple file selection
fileInput.setAttribute('multiple', '');


function startBatch(files) {
    uploadContent.style.display = 'none';
    batchContainer.style.display = 'block';
    batchQueue = files;
    batchList.innerHTML = '';

    files.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'batch-item';
        div.innerHTML = `
            <div class="batch-info">
                <span>${file.name}</span>
            </div>
            <span class="batch-status" id="status-${index}">Pending...</span>
        `;
        batchList.appendChild(div);
    });

    processBatchQueue();
}

async function processBatchQueue() {
    for (let i = 0; i < batchQueue.length; i++) {
        const file = batchQueue[i];
        const statusEl = document.getElementById(`status-${i}`);

        statusEl.innerText = "Processing...";
        statusEl.className = "batch-status"; // Reset text color

        try {
            const blob = await processFile(file);
            const url = URL.createObjectURL(blob);

            // Auto Download
            const a = document.createElement('a');
            a.href = url;
            a.download = `convertly-batch-${i}.png`;
            a.click();

            statusEl.innerText = "Downloaded";
            statusEl.classList.add("status-success");
        } catch (err) {
            statusEl.innerText = "Error";
            statusEl.classList.add("status-error");
        }
    }
}

async function processFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    let apiUrl = `${window.location.origin}/remove-bg`;
    if (window.location.origin === 'null' || window.location.protocol === 'file:') {
        apiUrl = 'http://127.0.0.1:8000/remove-bg';
    }

    const res = await fetch(apiUrl, { method: 'POST', body: formData });
    if (!res.ok) throw new Error('API Error');
    return await res.blob();
}

document.getElementById('batch-rest-btn').onclick = () => {
    batchContainer.style.display = 'none';
    uploadContent.style.display = 'flex';
    fileInput.value = '';
};

document.getElementById('reset-btn').onclick = () => {
    document.getElementById('editor-container').style.display = 'none';
    uploadContent.style.display = 'flex';
    fileInput.value = '';
};

// Removed old download/ad logic functions as they are superceded by Editor download


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
