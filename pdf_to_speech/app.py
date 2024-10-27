from flask import Flask, render_template, request, redirect, url_for
import pyttsx3
import PyPDF2
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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
        PDFreader = PyPDF2.PdfReader(filepath)
        nopages = len(PDFreader.pages)
        text_content = ""
        
        for i in range(nopages):
            page = PDFreader.pages[i]
            text_content += page.extract_text()
        
        voicePlayer = pyttsx3.init()
        voicePlayer.setProperty('rate', 180)
        voicePlayer.setProperty('volume', 1.0) 
        voicePlayer.say(text_content)
        voicePlayer.runAndWait()
        
        return "PDF read successfully!"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
