// Matrix-like background effect (unchanged)
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.1';
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const chars = "01";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    for (let i = 0; i < columns; i++) drops[i] = 1;
    
    function drawMatrix() {
        ctx.fillStyle = 'rgba(0, 15, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0f0';
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    
    setInterval(drawMatrix, 33);

    // Toggle key input field based on encryption checkbox
    const encryptCheckbox = document.getElementById('encryptCheckbox');
    const keyContainer = document.getElementById('keyContainer');
    
    encryptCheckbox.addEventListener('change', function() {
        keyContainer.style.display = this.checked ? 'block' : 'none';
    });
});

// Initialize loader with enhanced status messages
function initDecoderLoader() {
    const binaryStream = document.querySelector('.binary-stream');
    const statusText = document.querySelector('.status-text');
    const statusProgress = document.querySelector('.status-progress');
    
    // Clear existing binary digits
    binaryStream.innerHTML = '';
    
    // Generate random binary stream
    for (let i = 0; i < 150; i++) {
        const digit = document.createElement('span');
        digit.className = 'binary-digit';
        digit.textContent = Math.random() > 0.5 ? '1' : '0';
        digit.style.animationDelay = `${Math.random() * 2}s`;
        binaryStream.appendChild(digit);
    }
    
    // Status messages sequence
    const statusMessages = [
        "ANALYZING IMAGE DATA",
        "DECRYPTING PIXEL MATRIX",
        "VERIFYING STEGANOGRAPHIC PATTERNS",
        "EXTRACTING HIDDEN PAYLOAD"
    ];
    
    let currentStatus = 0;
    const statusInterval = setInterval(() => {
        if (currentStatus < statusMessages.length) {
            statusText.textContent = statusMessages[currentStatus];
            statusProgress.textContent = `[${'■'.repeat(currentStatus + 1)}${' '.repeat(statusMessages.length - currentStatus)}]`;
            currentStatus++;
        }
    }, 1500);
    
    return statusInterval;
}

// Enhanced decode form handler
document.getElementById('decodeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const loader = document.querySelector('.cyber-loader');
    const resultDiv = document.getElementById('decodedResult');
    const resultContent = document.querySelector('.result-content');
    const statusText = document.querySelector('.status-text');
    const statusProgress = document.querySelector('.status-progress');
    
    // Reset UI
    loader.style.display = 'block';
    resultDiv.style.display = 'none';
    resultContent.textContent = '';
    
    // Start loader
    const statusInterval = initDecoderLoader();
    
    try {
        // Make the actual decode request
        const response = await fetch('/decode', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Show finalizing message for 1 second
        statusText.textContent = "FINALIZING DECRYPTION";
        statusProgress.textContent = '[■■■■■]';
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Show completion message for 1 second
        statusText.textContent = "DECRYPTION COMPLETED";
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Display result
        if (data.error) {
            resultContent.textContent = `ERROR: ${data.error}`;
            resultContent.style.color = '#f44';
        } else {
            resultContent.textContent = data.message;
            resultContent.style.color = '#0f0';
        }
        
    } catch (error) {
        resultContent.textContent = `NETWORK ERROR: ${error.message}`;
        resultContent.style.color = '#f44';
    } finally {
        // Clean up
        clearInterval(statusInterval);
        
        // Show result
        loader.style.display = 'none';
        resultDiv.style.display = 'block';
    }
});

// Enhanced encode form handler
document.getElementById('encodeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitButton = this.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    const encryptCheckbox = document.getElementById('encryptCheckbox');
    const manualKey = this.querySelector('input[name="key"]').value;
    
    try {
        submitButton.disabled = true;
        submitButton.textContent = "PROCESSING...";
        
        const response = await fetch('/encode', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Encoding failed');
        }
        
        // Only show key alert if encryption was enabled AND no manual key was provided
        if (encryptCheckbox.checked && !manualKey) {
            const encryptionKey = response.headers.get('X-Encryption-Key');
            if (encryptionKey) {
                alert(`🔐 ENCRYPTION KEY (SAVE THIS!):\n\n${encryptionKey}\n\nThis key is required to decode the message.`);
            }
        }
        
        // Create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'encoded_' + formData.get('image').name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
});