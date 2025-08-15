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
});

// Initialize loader with enhanced status messages
function initDecoderLoader() {
  const binaryStream = document.querySelector('.binary-stream');
  const statusText = document.querySelector('.status-text');
  const statusProgress = document.querySelector('.status-progress');
  
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

// Progress tracking from server
const eventSource = new EventSource('/progress');
eventSource.onmessage = function(e) {
    const progress = JSON.parse(e.data).progress;
    document.getElementById('progressPercent').textContent = progress;
    document.getElementById('progressBar').style.width = `${progress}%`;
};

// Add this to script.js to handle the encode form
document.querySelector('form[action="/encode"]').addEventListener('submit', function(e) {
    // You can add loading indicators here if needed
    console.log('Encoding form submitted');
    // The form will submit normally since it's not using AJAX
});
