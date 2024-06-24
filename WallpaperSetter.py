# Wallpaper Setter
# Created by James Robinson (https://github.com/JamesRobinson160552)
# Last updated 04/19/2024

#TODO: 
# Improve UI

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
        with open((IMAGE_DIRECTORY + item[1]['album']['name'] + '.jpg').replace(" ", "_").replace("?", ""), 'wb') as handler:
            handler.write(image_data)
    
    for image in os.listdir(IMAGE_DIRECTORY):
        resize_image(IMAGE_DIRECTORY + image, screen_width, screen_height)

#Set wallpaper as one of the downloaded images
def set_wallpaper():
    """
    Get a random image from the images folder
    Set the image as the desktop wallpaper
    """
    wallpaper_path = IMAGE_DIRECTORY + random.choice(os.listdir(IMAGE_DIRECTORY))

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

    left = (width - new_width)/2 - 200
    right = (width + new_width)/2 + 200
    top = (height - new_height)/2 + 200
    bottom = (height + new_height)/2 - 200

    image = image.crop((left, top, right, bottom))
    image.save(image_path)

#Create image directory if it doesn't exist
IMAGE_DIRECTORY = os.getcwd() + "\\images\\"
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

#Create TKinter GUI
app = tk.Tk(className="WallpaperSetter")
screen_width, screen_height = app.maxsize() #Get screen size with max application size
app.geometry(str(int(screen_width/2)) + "x" + str(int(screen_height/2))) #Window resize
#print ("Terminal size: " + str(screen_width) + "x" + str(screen_height))

title = tk.Label(app, text="Wallpapers for Hot People with Good Taste")
title.grid(column=1, row=0)

SignInButton = tk.Button(app, text="Sign In", command=get_auth)
GetImagesButton = tk.Button(app, text="Get Images", command=download_images)
SetWallpaperButton = tk.Button(app, text="Set Wallpaper", command=set_wallpaper)

SignInButton.grid(column=1, row=1)
GetImagesButton.grid(column=2, row=1)
SetWallpaperButton.grid(column=3, row=1)

#Run GUI
app.mainloop()
