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
import tkinter as tk #to create GUI
import spotipy #to access spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv #to store spotify api credentials
load_dotenv()

#Access the user's spotify account
def get_auth():
    scope = "user-library-read"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#Fetch user's saved album covers and download
def download_images():
    """
    Use Spotify API to fetch user's saved album covers
    Download all images to the images folder
    """
    results = get_auth().current_user_saved_albums()
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

#Make image fit display
def resize_image(image_path, new_width, new_height):
    """
    Resize image to fit display
    Note: in this case, cropping adds blackspace hence 'bigger' sizes will make
    the image appear smaller
    """
    image = Image.open(image_path)
    width, height = image.size

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    image = image.crop((left, top, right, bottom))
    image.save(image_path)

app = tk.Tk()
screen_width, screen_height = app.maxsize()
print ("Terminal size: " + str(screen_width) + "x" + str(screen_height))

get_auth()
download_images()
for image in os.listdir("./images"):
    resize_image("./images/" + image, screen_width - 350, screen_height - 350)
set_wallpaper()
