from flask import Flask, render_template, request, send_file, jsonify, Response
import json
import os
import time  
from steganography import encode_image, decode_image, generate_aes_key
from werkzeug.utils import secure_filename
from base64 import b64encode, b64decode

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.urandom(24)  # For session management
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/encode', methods=['GET', 'POST'])
@app.route('/encode', methods=['POST'])
def encode():
    if 'image' not in request.files:
        return jsonify({'error': 'No image selected'}), 400
        
    image = request.files['image']
    message = request.form.get('message', '')
    use_encryption = request.form.get('encrypt') == 'on'
    manual_key = request.form.get('key', '').strip()
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + image.filename)
    
    try:
        image.save(input_path)
        
        key = None
        key_b64 = None
        if use_encryption:
            # Use manually entered key if provided, otherwise generate new one
            if manual_key:
                try:
                    key = b64decode(manual_key.encode('utf-8'))
                    if len(key) != 32:  # AES-256 requires 32-byte key
                        raise ValueError("Key must be 32 bytes when decoded")
                    key_b64 = manual_key  # Use the provided key
                except Exception as e:
                    return jsonify({'error': f'Invalid encryption key: {str(e)}'}), 400
            else:
                key = generate_aes_key()
                key_b64 = b64encode(key).decode('utf-8')
        
        encode_image(input_path, message, output_path, key)
        
        response = send_file(output_path, as_attachment=True)
        if use_encryption:
            # Only include key in header if it was auto-generated
            if not manual_key:
                response.headers['X-Encryption-Key'] = key_b64
                response.headers['Access-Control-Expose-Headers'] = 'X-Encryption-Key'
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image selected'}), 400
            
        image = request.files['image']
        message = request.form.get('message', '')
        use_encryption = request.form.get('encrypt') == 'on'
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + image.filename)
        
        try:
            image.save(input_path)
            
            key = None
            if use_encryption:
                key = generate_aes_key()
                key_b64 = b64encode(key).decode('utf-8')
            
            encode_image(input_path, message, output_path, key)
            
            response = send_file(output_path, as_attachment=True)
            if use_encryption:
                # Include the key in a download header
                response.headers['X-Encryption-Key'] = key_b64
                response.headers['Access-Control-Expose-Headers'] = 'X-Encryption-Key'
            
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('index.html')

@app.route('/decode', methods=['POST'])
def decode():
    if 'image' not in request.files:
        return {'error': 'No image selected'}, 400
    
    image = request.files['image']
    if image.filename == '':
        return {'error': 'No image selected'}, 400
    
    try:
        filename = secure_filename(image.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(input_path)
        
        # Check if an encryption key was provided
        key_b64 = request.form.get('key', '')
        key = None
        if key_b64:
            try:
                key = b64decode(key_b64.encode('utf-8'))
            except:
                return {'error': 'Invalid encryption key format'}, 400
        
        secret = decode_image(input_path, key)
        return {'message': secret}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/decode_progress')
def decode_progress():
    def generate():
        # Simulated progress (replace with actual progress from your decode function)
        statuses = [
            ("Analyzing image structure...", 10),
            ("Extracting pixel data...", 25),
            ("Decoding binary patterns...", 45),
            ("Reconstructing message...", 75),
            ("Finalizing...", 90),
            ("Complete", 100)
        ]
        
        for status, progress in statuses:
            yield f"data:{json.dumps({'progress': progress, 'status': status})}\n\n"
            time.sleep(1)  # Simulate work
            
        # When done
        result = decode_image("path_to_image.png")  # Your actual decode call
        yield f"event:complete\ndata:{json.dumps({'message': result})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')



@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)