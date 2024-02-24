import os
import shutil

'''
The downloaded dataset is not organized by artist. This script will organize the dataset by artist.
'''


def changeDirectory():
    for root, dirs, files in os.walk('./wikiart/'):
        for file in files:
            # Split the artist and artwork
            parts = file.split('_')
            artists = parts[0]
            artwork = '_'.join(parts[1:]).replace('.jpg', '')

            # create new directory
            new_dir = os.path.join('./wikiart_by_artist/', artists)

            # if not exist
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            # move the file and rename the file
            old_path = os.path.join(root, file)
            new_dir = os.path.join(new_dir, artwork + '.jpg')
            shutil.move(old_path, new_dir)


def main():
    if __name__ == "__main__":
        changeDirectory()