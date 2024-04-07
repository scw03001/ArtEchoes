import os
import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision.utils import save_image

# Gaussian noise
class AddRandomGaussianNoise(object):
    def __init__(self, mean=0., std_range=(0.01, 0.1)):
        self.mean = mean
        self.std_min, self.std_max = std_range
        
    def __call__(self, tensor):
        std = torch.empty(1).uniform_(self.std_min, self.std_max).item()
        return tensor + torch.randn(tensor.size()) * std + self.mean


# Augment and save the applied files
def augment_and_save(data_transforms, image_path, file_name, save_dir, num_augment):
    # Load and check if the image is black and white
    original_img = Image.open(image_path)

    # Resize and convert original image, then normalize it
    img_resized = transforms.Resize((224, 224))(original_img.convert('RGB'))
    img_tensor = transforms.ToTensor()(img_resized)

    # Save the normalized tensor image
    save_image(img_tensor, os.path.join(save_dir, file_name))

    # Apply augmentation to the original resized image
    for i in range(num_augment):
        img_aug = data_transforms(img_resized)  # Use resized image for augmentation
        save_image(img_aug, os.path.join(save_dir, f'{file_name.split(".")[0]}_{i}.jpg'))

    # Delete the original image
    os.remove(image_path)
    print(f"Deleted original image: {image_path}")

# Apply augment_and_save to the specified folder
def process_images(folder_path, num_augment=10):
    # Define transformation for augmentation
    data_transforms = transforms.Compose([
        transforms.RandomRotation(degrees=20),
        transforms.RandomHorizontalFlip(p=0.25),
        transforms.RandomResizedCrop(size=224, scale=(0.85, 1.0)),
        transforms.ColorJitter(brightness=0.05, contrast=0.05, saturation=0.05, hue=0.02),
        transforms.ToTensor(),
        AddRandomGaussianNoise(0., (0.001, 0.01)),
    ])
            
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            artist_name = " ".join([token for token in file_name.split('.')[0].split('_') if token.isalpha()])  
                            
            path = os.path.join(root, file_name)
            print(f"Processing {path}")
            
            save_dir = os.path.join(root, artist_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            augment_and_save(data_transforms, path, file_name, save_dir, num_augment)
            print("Successfully created and augmented images")

if __name__ == "__main__":
    path = './resized'
    process_images(path, 10)
