'''
Read image and find the artist whose style is most similar to the image.

We use our trained ResNet18 model
'''
from flask import Blueprint, render_template_string, session
import torch
from torchvision import transforms
from torch import nn, optim
from PIL import Image
import pandas as pd
import numpy as np
from torchvision import models
from flask_cors import cross_origin
from flask_cors import CORS

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
import cv2
import os


# Arist dictionary
df = pd.read_csv('./artists/artists.csv')
artists = df['name'].values
artists.sort()
artists_dict = {i: artist for i, artist in enumerate(artists)}

# print(artists_dict)

find_artist_bp = Blueprint('find_artist', __name__)
CORS(find_artist_bp, resources={r"/find_artist/*": {"origins": "*"}})
num_classes = len(artists)
# Load the trained model
model = models.resnet18()
model.fc = nn.Sequential(
    nn.Dropout(0.3),  # Add dropout to the fully connected layer
    nn.Linear(model.fc.in_features, num_classes)
)
state_dict = torch.load('./model/artist_classifier.pth', map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize the image
])




# @find_artist_bp.route('/find_artist/<filename>')
# def find_artist(filename=None):

#     # Load the image
#     image = Image.open('./uploads/' + filename)

#     # Apply the transformation
#     image_tensor = transform(image).unsqueeze(0)

#     # Get the prediction
#     with torch.no_grad():
#         prediction = model(image_tensor)
#     _, predicted = torch.max(prediction, 1)

#     # Get the artist name
#     artist = artists_dict[predicted.item()]



#     return render_template_string('''
#     <!doctype html>
#     <html>
#     <head>
#         <title>Find Artist</title>
#     </head>
#     <body>
#         This is the find artist page. The filename is {{ filename }}<br>
#         The predicterd artist is {{artist}}
#     </body>
#     </html>
#     ''', filename=filename, artist=artist)


# Endpoint to retrieve author of filename
@find_artist_bp.route('/find_artist/<filename>', methods=['GET'])
def find_artist(filename=None):
    if filename is None:
        return {"error": "File not found"}, 404

    try:
        # Load the image
        image = Image.open('./uploads/' + filename)

        # Convert the image to a numpy array to run with GradCAM
        rgb_img = np.array(image.convert('RGB'), dtype=np.float32) / 255.0

        # Apply the transformation
        image_tensor = transform(image).unsqueeze(0)

        # Get the prediction
        with torch.no_grad():
            prediction = model(image_tensor)
        _, predicted = torch.max(prediction, 1)

        # Get the artist name
        artist = artists_dict[predicted.item()]

        # Based on the Grad-CAM, since we use ResNet18, we use the layer4 as the target layer
        target_layers = [model.layer4[-1]]
        cam = GradCAM(model=model, target_layers=target_layers)

        targets = [ClassifierOutputTarget(predicted.item())]
        
        grayscale_cam = cam(input_tensor=image_tensor, targets=targets)[0, :]

        grayscale_cam = cv2.resize(grayscale_cam, (rgb_img.shape[1], rgb_img.shape[0]))

        visualisation = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)

        heatmap = Image.fromarray((visualisation * 255).astype(np.uint8))

        # Check if the directory exists and create it if necessary
        if not os.path.exists('./static/'):
            os.makedirs('./static/')

        # Save the heatmap
        heatmap.save(f'./static/{filename}_heatmap.jpg')

        # Save prediction in session variables
        # session['best_guesses_artist'] = artist

        return {"artist": artist,
                "images": [heatmap]}
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500