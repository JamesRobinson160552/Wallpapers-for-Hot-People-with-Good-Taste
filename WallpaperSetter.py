# Wallpaper Setter
# Created by James Robinson (https://github.com/JamesRobinson160552)
# Last updated 06/26/2024

#TODO: 
# Improve UI
# Add ability to increase/decrease size
# Bugs:
#   Wallpaper does not persist after restart

import ctypes #to process image
import os #to save images
import requests #to download images
import random #to pick random image
from PIL import Image #to resize image
import tkinter as tk #to create GUI
import tkinter.ttk as ttk
from tkinter.ttk import Style
import spotipy #to access spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv #to store spotify api credentials
load_dotenv()

#Access the user's spotify account
def get_auth():
    """
    Prompts user to authorize library access via default browser
    """
    scope = "user-library-read"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#Fetch user's saved album covers and download
def download_images():
    """
    Uses Spotify API to fetch user's saved album covers
    Downloads all images to the images folder
    """
    results = get_auth().current_user_saved_albums()
    for item in enumerate(results['items']):
        image_data = requests.get(item[1]['album']['images'][0]['url']).content
        with open((IMAGE_DIRECTORY + item[1]['album']['name'] + '.jpg').replace(" ", "_").replace("?", ""), 'wb') as handler:
            handler.write(image_data)
    
    for image in os.listdir(IMAGE_DIRECTORY):
        resize_image(IMAGE_DIRECTORY + image, screen_width, screen_height/1.5)

#Set wallpaper as one of the downloaded images
def set_wallpaper():
    """
    Gets a random image from the images folder
    Sets the image as the desktop wallpaper
    """
    wallpaper_path = IMAGE_DIRECTORY + random.choice(os.listdir(IMAGE_DIRECTORY))

    SPI_SETDESKWALLPAPER = 20
    image = ctypes.c_wchar_p(wallpaper_path)
    wallpaper_style = 6
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 1, image, wallpaper_style)

#Make image fit display
def resize_image(image_path, new_width, new_height):
    """
    Resizes an image to fit display
    Note: in this case, cropping adds blackspace hence 'bigger' sizes will make
    the image appear smaller
    """
    image = Image.open(image_path)
    width, height = image.size

    left = (width - new_width)/2
    right = (width + new_width)/2
    top = (height - new_height)/2
    bottom = (height + new_height)/2

    image = image.crop((left, top, right, bottom))
    image.save(image_path)

#Create image directory if it doesn't exist
IMAGE_DIRECTORY = os.getcwd() + "\\images\\"
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

#Create TKinter GUI
app = tk.Tk(className="WallpaperSetter")
screen_width, screen_height = app.maxsize() #Get screen size with max application size
app.geometry("800x400") #Window resize
app.resizable(width=False, height=False)
app.configure(background='black')

title = tk.Label(app, text="Wallpapers for Hot People with Good Taste")
title.configure(background='black', foreground='green', font='sans 28 bold')
title.pack(side=tk.TOP, pady=20)

ButtonBorder = tk.Frame(app, background='green')
ButtonBorder.pack(side=tk.TOP, pady=20, padx=100,fill=tk.BOTH)

ButtonMenu = tk.Frame(ButtonBorder, background='gray')
ButtonMenu.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH)

style = Style()
style.configure('W.TButton', 
                font=('calibri', 20, 'bold'),
                background='green',
                foreground='green'
                )

SignInButton = ttk.Button(ButtonMenu, text="Sign In", command=get_auth, style='W.TButton')
GetImagesButton = ttk.Button(ButtonMenu, text="Get Images", command=download_images, style='W.TButton')
SetWallpaperButton = ttk.Button(ButtonMenu, text="Set Wallpaper", command=set_wallpaper, style='W.TButton')

SignInButton.pack(side=tk.TOP, ipadx=200, ipady=10, padx=20, pady=8)
GetImagesButton.pack(side=tk.TOP, ipadx=200, ipady=10, padx=20, pady=8)
SetWallpaperButton.pack(side=tk.TOP, ipadx=200, ipady=10, padx=20, pady=8)

#Run GUI
app.mainloop()
