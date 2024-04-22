from flask import Blueprint, render_template_string, request, url_for, send_file
import requests
from dotenv import load_dotenv
import os
import time
from tempfile import NamedTemporaryFile
from PIL import Image

make_animation_bp = Blueprint('make_animation', __name__)

load_dotenv()
stability_api = os.getenv('stability_api')
path = './uploads/'

@make_animation_bp.route('/make_animation/<filename>', methods=['GET', 'POST'])
def make_animation(filename=None):
    # The size should be 768x768 to fit the API
    image = Image.open('./uploads/' + filename).resize((768, 768))

    temp_image = NamedTemporaryFile(delete=False, suffix='.jpg')
    image.save(temp_image)

    # POST request from the stability.ai official document
    with open(temp_image.name, 'rb') as img_file:
        response = requests.post(
            f"https://api.stability.ai/v2beta/image-to-video",
            headers={
                "authorization": f"Bearer {stability_api}"
            },
            files={
                "image": img_file
            },
            data={
                "seed": 0,
                "cfg_scale": 1.8, # how stronly sticks to the original image
                "motion_bucket_id":  200 # motion
            },
        )
    
    generation_id = response.json().get('id')
    print("Generation ID:", generation_id)
    return {"generation_ID" : generation_id}
    # Note: The generated video was never stored in the desried address, to the rest the request of the video
    # was moved to the web app.

    # Wait for the video to be generated => needs to be changed 
    time.sleep(60)

    # Fetch the video
    response = requests.request(
        "GET",
        f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
        headers={
            'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer {stability_api}"
        },
    )

    if response.status_code == 202:
        print("Generation in-progress, try again in 10 seconds.")
    elif response.status_code == 200:
        print("Generation complete!")
        directory = './generated_videos/'
        video_filename = f"{filename}.mp4"
        with open(f"{directory}{filename}.mp4", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    

    video_url = url_for('make_animation.serve_video', filename=filename)

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


# <video width="320" height="240" controls>
#             <source src="{{ video_url }}" type="video/mp4">
#         </video>

# @make_animation_bp.route('/serve_video/<filename>')
# def serve_video(filename=None):
#     return send_file(f'./generated_videos/{filename}', mimetype='video/mp4')