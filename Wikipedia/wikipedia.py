from Wikipedia2PDF import Wikipedia2PDF
import pandas as pd
import re

df = pd.read_csv('../GoogleImageSearch/BestArtists50/artists.csv')
artists = df['name'].values
artists.sort()
artists_dict = {i: artist for i, artist in enumerate(artists)}

for i, artist in artists_dict.items():
    print(f"Start downloading artist: {artist}")

    # Replace blank+ special characters with underscore
    artist = re.sub('[^A-Za-z0-9_]+', '', artist.replace(' ', '_'))
    Wikipedia2PDF(f"https://en.wikipedia.org/wiki/{artist}", filename=f"./pdfs/{artist}.pdf")


# manual code to store files that are not correctly downloaded
pages = {
    "Albrecht_Dürer": "https://en.wikipedia.org/wiki/Albrecht_Dürer",
    "Henri_de_Toulouse-Lautrec": "https://fr.wikipedia.org/wiki/Henri_de_Toulouse-Lautrec",
    "Pieter_Bruegel": "https://en.wikipedia.org/wiki/Pieter_Bruegel_the_Elder",
    "Pierre-Auguste_Renoir": "https://en.wikipedia.org/wiki/Pierre-Auguste_Renoir",
    "Vasiliy_Kandinskiy": "https://en.wikipedia.org/wiki/Wassily_Kandinsky",
    "William_Turner": "https://en.wikipedia.org/wiki/J._M._W._Turner"
}

for artist, url in pages.items():
    print("Start downloading artist: ", artist)
    Wikipedia2PDF(url, filename=f"./pdfs/{artist}.pdf")
