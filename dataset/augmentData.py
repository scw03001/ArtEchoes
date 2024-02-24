import os
import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision.utils import save_image
import shutil



'''
This file aguments data with adding noise, rotation, flip, crop, and color jitter.
'''



# Gaussian noise
class AddGaussianNoise(object):
    def __init__(self, mean=0., std=1.):
        self.std = std
        self.mean = mean
        
    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean

# Aguement and save the applied files
def augment_and_save(image_path, save_dir, num_augment=40):
    # define transformation for augmentation
    data_transforms = transforms.Compose([
        transforms.RandomRotation(degrees=30),
        transforms.RandomHorizontalFlip(p=0.25),
        transforms.RandomResizedCrop(size=256, scale=(0.7, 1.0)),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
        transforms.ToTensor()
    ])

    img = Image.open(image_path)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filename = os.path.basename(image_path).split('.')[0]

    for i in range(num_augment):

        img_aug = data_transforms(img)
        save_image(img_aug, os.path.join(save_dir, f'{filename}_{i}.jpg'))

# Apply augment_and_save to the specified foler
def process_images(folder_path, num_augment=10):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                path = os.path.join(root, file_name)
                print(path)
                save_dir = os.path.join(root, file_name.split('.')[0])
                new_img_path = os.path.join(save_dir, file_name)

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                augment_and_save(path, save_dir, num_augment)
                shutil.move(path, new_img_path)
                print("Successfully created")


if __name__ == "__main__":
    path = './images'
    process_images(path, 2)