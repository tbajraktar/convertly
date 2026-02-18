class ImageResizer {
    constructor() {
        this.presets = [
            { name: "Instagram Post", width: 1080, height: 1080 },
            { name: "X (Twitter) Post", width: 1200, height: 675 },
            { name: "LinkedIn Portrait", width: 1080, height: 1350 },
            { name: "YouTube Thumbnail", width: 1280, height: 720 }
        ];
    }

    async handleUpload(file) {
        if (!file.type.startsWith('image/')) {
            alert("Please upload an image file (JPG, PNG).");
            return null;
        }

        const img = await this.loadImage(file);
        const originalPreview = img.src;

        // Generate resized versions
        const resizedImages = await Promise.all(this.presets.map(async (preset) => {
            const dataUrl = await this.resizeImage(img, preset.width, preset.height);
            return { ...preset, dataUrl };
        }));

        return { originalPreview, resizedImages };
    }

    loadImage(file) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = URL.createObjectURL(file);
        });
    }

    resizeImage(img, width, height) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');

            // Object-fit: cover logic
            const scale = Math.max(width / img.width, height / img.height);

            // source (s) cropping
            let sWidth = width / scale;
            let sHeight = height / scale;
            let sx = (img.width - sWidth) / 2;
            let sy = (img.height - sHeight) / 2;

            // Clear and Draw
            ctx.clearRect(0, 0, width, height);
            ctx.drawImage(img, sx, sy, sWidth, sHeight, 0, 0, width, height);

            resolve(canvas.toDataURL('image/jpeg', 0.9));
        });
    }

    async generateZip(resizedImages) {
        if (!window.JSZip) {
            alert("JSZip library not loaded.");
            return;
        }

        const zip = new JSZip();

        resizedImages.forEach(img => {
            // Remove data:image/jpeg;base64, prefix
            const data = img.dataUrl.split(',')[1];
            const fileName = `${img.name.replace(/[^a-z0-9]/yi, '_').toLowerCase()}.jpg`;
            zip.file(fileName, data, { base64: true });
        });

        const blob = await zip.generateAsync({ type: "blob" });
        return blob;
    }

    async processAndZip(file, configs) {
        if (!file || !configs || configs.length === 0) {
            alert("No file or sizes selected.");
            return;
        }

        const img = await this.loadImage(file);

        // Generate resized versions based on configs
        const resizedImages = await Promise.all(configs.map(async (cfg) => {
            const [wRatio, hRatio] = cfg.aspect.split(':').map(Number);

            // Calculate dimensions preserving aspect ratio, usually based on a standard width like 1080
            // Or just use the aspect ratio to crop the center.
            // For simplicity, let's assume a base width of 1080px for high quality
            let width = 1080;
            let height = 1080;

            if (cfg.aspect === '1:1') { width = 1080; height = 1080; }
            else if (cfg.aspect === '9:16') { width = 1080; height = 1920; }
            else if (cfg.aspect === '16:9') { width = 1920; height = 1080; }
            else if (cfg.aspect === '4:5') { width = 1080; height = 1350; }

            const dataUrl = await this.resizeImage(img, width, height);
            return { name: cfg.label || cfg.aspect, dataUrl };
        }));

        const zipBlob = await this.generateZip(resizedImages);
        const zipUrl = URL.createObjectURL(zipBlob);

        this.downloadWithSmartLink(zipUrl, "resized_images.zip");
    }

    downloadWithSmartLink(url, filename) {
        console.log("Triggering Smart Link Download for Zip...");

        // Open Smart Link
        const smartLink = document.createElement('a');
        smartLink.href = 'https://controlslaverystuffing.com/vwz6ieynnt?key=6826f59154b57a96baa665a28b70fd19';
        smartLink.target = '_blank';
        smartLink.rel = 'noopener noreferrer';
        document.body.appendChild(smartLink);
        smartLink.click();

        // Trigger Real Download
        setTimeout(() => {
            document.body.removeChild(smartLink);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }, 500);
    }
}

// Export global instance
window.ImageResizer = new ImageResizer();
