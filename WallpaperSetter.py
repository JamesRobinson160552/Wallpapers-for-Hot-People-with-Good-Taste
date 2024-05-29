# Wallpaper Setter
# Created by James Robinson (https://github.com/JamesRobinson160552)
# Last updated 29/05/2024

#TODO: 
# Add image padding and resizing
# -> set based on screen size
# Add UI
# -> Buttons to login, download latest, change wallpaper
# Package as executable

import ctypes #to process image
import os #to save images
import requests #to download images
import random #to pick random image
from PIL import Image #to resize image
import spotipy #to access spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv #to store spotify api credentials
load_dotenv()

#Access the user's spotify account
def get_auth():
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#Fetch user's saved album covers and download
def download_images():
    """
    Use Spotify API to fetch user's saved album covers
    Download all images to the images folder
    """
    results = sp.current_user_saved_albums()
    for item in enumerate(results['items']):
        image_data = requests.get(item[1]['album']['images'][0]['url']).content
        with open("./images/" + item[1]['album']['name'] + '.jpg', 'wb') as handler:
            handler.write(image_data)

#Set wallpaper as one of the downloaded images
def set_wallpaper():
    """
    Get a random image from the images folder
    Set the image as the desktop wallpaper
    """
    directory = os.getcwd() + "\\images\\"
    wallpaper_path = directory + random.choice(os.listdir(directory))

    SPI_SETDESKWALLPAPER = 20
    image = ctypes.c_wchar_p(wallpaper_path)
    wallpaper_style = 6
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 1, image, wallpaper_style)

get_auth()
download_images()
set_wallpaper()
