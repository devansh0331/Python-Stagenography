from flask import Flask, render_template, request, send_file, jsonify, Response
import json
import os
import time  # For time.sleep if using progress updates
from steganography import encode_image, decode_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In app.py, update the encode route to handle both GET and POST
@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({'error': 'No image selected'}), 400
            
        image = request.files['image']
        message = request.form.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + image.filename)
        
        try:
            image.save(input_path)
            encode_image(input_path, message, output_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Handle GET request by showing the form
    return render_template('index.html')


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
        
        secret = decode_image(input_path)
        return {'message': secret}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/progress')
def progress():
    def generate():
        for i in range(101):
            yield f"data: {{\"progress\": {i}}}\n\n"
            time.sleep(0.05)  # Slower progression
    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)