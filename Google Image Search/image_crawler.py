import csv
import requests
import os
from PIL import Image
from io import BytesIO

# Define a function to search for artworks on Google and display them
def search_google_artworks(artist_name, artwork_title, img_size='large', img_type='photo', num_results=10):
    # API key and Custom Search Engine ID for Google API
    api_key = 'API'  # Replace with your actual API key
    cse_id = 'EID'  # Replace with your actual Custom Search Engine ID

    # Combine artist name and artwork title for the search query
    query = f"{artist_name} {artwork_title}"
    # Google Custom Search JSON API endpoint
    url = f"https://www.googleapis.com/customsearch/v1"

    # Parameters for the API request
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key,
        'searchType': 'image',
        'imgSize': img_size,
        'imgType': img_type,
        'num': num_results
    }

    # Send the request to Google's Custom Search API
    response = requests.get(url, params=params)
    # Convert the response to JSON format
    results = response.json()

    # Extract image URLs from the search results
    image_urls = [item['link'] for item in results.get('items', [])]

    # Return the list of image URLs
    return image_urls

# Define a function to download and save images
def download_images(image_urls, artist_name, artwork_title):
    # Create a directory for the artist if it doesn't exist
    artist_dir = "crawled_images/" + artist_name.replace(" ", "_")
    artwork_title = artwork_title.replace(' ', '_')
    artwork_dir = artist_dir + "/" + artwork_title
    
    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)

    if not os.path.exists(artwork_dir):
        os.makedirs(artwork_dir)
        
    # Download each image
    for i, url in enumerate(image_urls):
        try:
            # Get the image from the URL
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            # Save the image
            img_path = f"{artist_dir}/{artwork_title}/{artwork_title}_{i+1}.png"
            img.save(img_path)
            
            print(f"Downloaded and saved image to {img_path}")
        except Exception as e:
            print(f"Could not download {url}: {e}")

# Function to process CSV and download images
def process_csv_and_download_images(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            image_directory, _, artist_name = row  # Adjust according to your CSV structure
            artwork_title = image_directory.split('/')[1][:-4]
            print(f"Searching for images of {artist_name}'s {artwork_title}")
            image_urls = search_google_artworks(artist_name, artwork_title)
            download_images(image_urls, artist_name, artwork_title)

# Replace 'csv/part_?.csv' with the path to your actual CSV file
process_csv_and_download_images('csv/part_?.csv')
