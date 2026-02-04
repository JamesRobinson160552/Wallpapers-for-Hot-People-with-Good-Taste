# Wallpaper Setter
# Created by James Robinson (https://github.com/JamesRobinson160552)
# Last updated 06/26/2024

#TODO: 
# Improve UI
# Add ability to increase/decrease size
# Bugs:
#   Wallpaper does not persist after restart

import ctypes #to process image
from ctypes import wintypes
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
    sp = get_auth()
    limit = 50  # Spotify max page size
    offset = 0

    while True:
        results = sp.current_user_saved_albums(limit=limit, offset=offset)
        items = results.get('items', [])
        if not items:
            break

        for item in items:
            try:
                url = item['album']['images'][0]['url']
            except (KeyError, IndexError):
                continue

            name = item['album'].get('name', 'unknown')
            safe_name = name.replace('.', '_').replace('>', '').replace('<', '').replace(':', '').replace('"', '').replace('/', '_').replace('\\', '_').replace('|', "_").replace('?', '').replace('*', 'x')
            image_path = IMAGE_DIRECTORY + safe_name + '.jpg'

            # Avoid re-downloading if we already have the file
            if os.path.exists(image_path):
                continue

            image_data = requests.get(url).content
            with open(image_path, 'wb') as handler:
                handler.write(image_data)

        offset += len(items)
    
    for image in os.listdir(IMAGE_DIRECTORY):
        # Only process common image files
        if not image.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        resize_image(os.path.join(IMAGE_DIRECTORY, image), screen_width, screen_height)

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
    Resize an image to fit within (new_width, new_height) while preserving
    aspect ratio.
    """
    image = Image.open(image_path).convert('RGB')
    new_width = int(new_width)
    new_height = int(new_height)

    src_w, src_h = image.size
    if src_w == 0 or src_h == 0:
        return

    src_ratio = src_w / src_h
    target_ratio = new_width / new_height

    # Determine scaled size to 'contain' the image inside the target box
    if src_ratio > target_ratio:
        # Image is wider than target -> fit to width
        scaled_w = new_width
        scaled_h = round(new_width / src_ratio)
    else:
        # Image is taller (or equal) -> fit to height
        scaled_h = new_height
        scaled_w = round(new_height * src_ratio)

    image = image.resize((scaled_w, scaled_h), Image.LANCZOS)

    # Create background and paste centered to avoid cropping/zoom
    background = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    offset_x = (new_width - scaled_w) // 2
    offset_y = (new_height - scaled_h) // 2
    background.paste(image, (offset_x, offset_y))
    background.save(image_path, quality=95)

#Create image directory if it doesn't exist
IMAGE_DIRECTORY = os.getcwd() + "\\images\\"
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

#Create TKinter GUI
app = tk.Tk(className="WallpaperSetter")

# Get the usable work area (excludes taskbar)
def get_work_area():
    try:
        SPI_GETWORKAREA = 0x0030
        rect = wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        return width, height
    except Exception:
        return app.maxsize()

screen_width, screen_height = get_work_area() #Get screen size excluding taskbar
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
