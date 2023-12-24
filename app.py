#!/usr/bin/env python

from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(img_filename):
    # load an image and set the height to 400 and with depending on the aspect ratio
    img = Image.open(img_filename)
    baseheight = 400
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    # save the resized image to a file
    # use basename to get extract the filename from the path
    filename = os.path.basename(img_filename)
    img.save( f"cache/{filename}")
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # create thumbnail for the image
        resize_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        return jsonify({'message': 'Allowed file types are png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run(debug=True)

