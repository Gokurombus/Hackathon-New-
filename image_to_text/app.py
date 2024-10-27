from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output_texts'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\user\\Downloads\\tesseract"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        
        random_id = str(random.randint(1000, 9999))
        text_filename = f"text_file_{random_id}.txt"
        text_filepath = os.path.join(app.config['OUTPUT_FOLDER'], text_filename)
        
        with open(text_filepath, "w") as f:
            f.write(text)
        
        return redirect(url_for('download_file',filename=text_filename))
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
