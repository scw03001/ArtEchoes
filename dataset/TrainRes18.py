import torch
import torchvision.models as models
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torch import nn, optim
from tqdm import tqdm
import os

# Constants
NUM_CLASSES = 50  # Number of artists
BATCH_SIZE = 32   # Adjust based on GPU memory
INITIAL_LEARNING_RATE = 0.001 # Initial learning rate for Transfer Learning
EPOCHS = 10       # May increase later
TRAIN_RATIO = 0.75 # 75% of data for training, 25% for validation
L2_REGULARIZATION = 1e-5 # Weight decay for regularization

# Ensure the saved_models directory exists
saved_models_dir = ''
os.makedirs(saved_models_dir, exist_ok=True)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Prepare dataset
class ArtDataset(datasets.ImageFolder):
    def __init__(self, root_dir, transform=None):
        super().__init__(root=root_dir, transform=transform)

# Define transforms with augmentation
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize the image
])

# Load data
dataset = ArtDataset(root_dir='./resized', transform=transform)

# Split dataset into training and validation sets
num_train = int(len(dataset) * TRAIN_RATIO)
num_val = len(dataset) - num_train
train_dataset, val_dataset = random_split(dataset, [num_train, num_val])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load pre-trained ResNet model and modify it for NUM_CLASSES classes
model = models.resnet18(pretrained=True)
model.fc = nn.Sequential(
    nn.Dropout(0.3), # Add dropout to the fully connected layer
    nn.Linear(model.fc.in_features, NUM_CLASSES)
)
model = model.to(device)

# Define loss function and optimizer with L2 regularization
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=INITIAL_LEARNING_RATE, weight_decay=L2_REGULARIZATION)

# Define learning rate scheduler
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)  # Decay LR by 0.1 every 3 epochs

# Training loop
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    # Wrap train_loader with tqdm for a progress bar
    for images, labels in tqdm(train_loader, desc=f'Epoch {epoch+1} [Training]'):
        images, labels = images.to(device), labels.to(device)
        
        # Zero the parameter gradients
        optimizer.zero_grad()
        
        # Forward + backward + optimize
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()

    scheduler.step()  # Update learning rate
    print(f'Epoch {epoch+1}, Loss: {running_loss / len(train_loader)}')

    # Validation loop
    model.eval()
    total = 0
    correct = 0
    # Wrap val_loader with tqdm for a progress bar
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc=f'Epoch {epoch+1} [Validation]'):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Epoch {epoch+1}, Validation Accuracy: {100 * correct / total}%')
    
    # Save the trained model after each epoch
    model_save_path = os.path.join(saved_models_dir, f'resnet_art_classifier_epoch_{epoch+1}.pth')
    torch.save(model.state_dict(), model_save_path)
