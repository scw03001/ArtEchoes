from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os
from flask_cors import CORS
from chatbot import chatbot_bp
from find_artist import find_artist_bp
from make_animation import make_animation_bp

# main app
app = Flask(__name__)
CORS(app)
app.secret_key = 'example_secret_key'
# register blueprints
CORS(find_artist_bp, supports_credentials=True)
CORS(chatbot_bp, supports_credentials=True)
app.register_blueprint(chatbot_bp)
app.register_blueprint(find_artist_bp)
app.register_blueprint(make_animation_bp)


# Assign the upload folder. IF not exists, create it
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Only allow these file formats
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file format is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Main page -> upload image
@app.route('/')
def upload_form():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Main</title>
    </head>
    <body>
        <h2>Upload Image</h2>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
    </body>
    </html>
    ''')

# Endpoint to upload a picture
@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f'{filename} uploaded successfully.')
        # return redirect(url_for('choose_option', filename=filename))
        return {"status": "success"}, 200
    else:
        # This should be visualised in the website as well and make users to re-upload the file
        return 'Allowed file types are png, jpg, jpeg'
    

# return image from server
@app.route('/images/<filename>')
def get_image(filename):
    try:
        # Validate if the filename is secure and prevent path traversal attacks
        if '..' in filename or filename.startswith('/'):
            return {}
        
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return {}

if __name__ == '__main__':
    app.run(debug=True)
    

@app.route('/choose_option/<filename>')
def choose_option(filename):
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Choose Option</title>
    </head>
    <body>
        <h2>Choose an option for the uploaded image</h2>
        <a href="{{ url_for('chatbot.chatbot', filename=filename) }}">Chatbot</a>
        <a href="{{ url_for('find_artist.find_artist', filename=filename) }}">Find Similar Artist</a>
        <a href="{{ url_for('make_animation.make_animation', filename=filename) }}">Make Animation</a>
    </body>
    </html>
    ''', filename=filename)


if __name__ == "__main__":
    app.run(port=8000, debug=True)