'''
Read image and find the artist whose style is most similar to the image.

We use our trained ResNet18 model
'''
from flask import Blueprint, render_template_string
import torch
from torchvision import transforms
from torch import nn, optim
from PIL import Image
import pandas as pd
from torchvision import models


# Arist dictionary
df = pd.read_csv('./artists/artists.csv')
artists = df['name'].values
artists.sort()
artists_dict = {i: artist for i, artist in enumerate(artists)}

print(artists_dict)

find_artist_bp = Blueprint('find_artist', __name__)
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
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize the image
])




@find_artist_bp.route('/find_artist/<filename>')
def find_artist(filename=None):

    # Load the image
    image = Image.open('./uploads/' + filename)

    # Apply the transformation
    image_tensor = transform(image).unsqueeze(0)

    # Get the prediction
    with torch.no_grad():
        prediction = model(image_tensor)
    _, predicted = torch.max(prediction, 1)

    # Get the artist name
    artist = artists_dict[predicted.item()]



    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Find Artist</title>
    </head>
    <body>
        This is the find artist page. The filename is {{ filename }}<br>
        The predicterd artist is {{artist}}
    </body>
    </html>
    ''', filename=filename, artist=artist)