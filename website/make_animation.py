from flask import Blueprint, render_template_string, request, send_file
import requests
from dotenv import load_dotenv
import os
import time
from PIL import Image

make_animation_bp = Blueprint('make_animation', __name__)

load_dotenv()
stability_api = os.getenv('stability_api')
path = './uploads/'

@make_animation_bp.route('/make_animation/<filename>', methods=['GET', 'POST'])
def make_animation(filename=None):
    # The size should be 768x768 to fit the API
    image = Image.open('./uploads/' + filename).resize((768, 768))

    # POST request from the stability.ai official document
    response = requests.post(
        f"https://api.stability.ai/v2beta/image-to-video",
        headers={
            "authorization": f"Bearer {stability_api}"
        },
        files={
            "image": image
        },
        data={
            "seed": 0,
            "cfg_scale": 1.8,
            "motion_bucket_id": 127
        },
    )

    print("Generation ID:", response.json().get('id'))




    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Make Animation</title>
    </head>
    <body>
        This is the make animation page. The filename is {{ filename }}
    </body>
    </html>
    ''', filename=filename)