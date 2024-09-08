import os
import xml.etree.ElementTree as ET
import subprocess
from PIL import Image
import numpy as np

# Function to convert 16-bit grayscale TIFF to 8-bit
def normalize_16bit_image(image):
    # Convert image to a numpy array
    arr = np.array(image, dtype=np.float32)

    # Normalize the array to 8-bit (0-255)
    arr = (arr / 65535.0) * 255.0
    return arr.astype(np.uint8)

def process_dir(directory):

    rgb_files = []
    frame_num = 1

    all_files = sorted(os.listdir(directory))

    for file in all_files:
        rgb_files.append(file)
        if file.endswith("E.tif"):
            png_file = f"frames_convert/earth_{frame_num}.png"

            # if os.path.exists(png_file):
            #     print("Already exists:", png_file)
            #     continue

            red_file = "images/" + rgb_files[2]
            green_file = "images/" + rgb_files[1]
            blue_file = "images/" + rgb_files[0]

            print("Merging", red_file, green_file, blue_file, "to", png_file)

            # subprocess.run(["convert", red_file, green_file, blue_file, "-combine", "-depth", "16", png_file], check=True)

            # Load the three 16-bit grayscale TIFF images
            red_channel = Image.open(red_file)
            green_channel = Image.open(green_file)
            blue_channel = Image.open(blue_file)

            # Convert 16-bit images to 8-bit
            red = normalize_16bit_image(red_channel)
            green = normalize_16bit_image(green_channel)
            blue = normalize_16bit_image(blue_channel)

            # Stack the channels into an RGB image
            rgb_image = np.stack((red, green, blue), axis=-1)

            # Convert the numpy array back to an Image object
            rgb_image_pil = Image.fromarray(rgb_image)

            # Save the image as a PNG
            rgb_image_pil.save(png_file)

            frame_num += 1
            rgb_files = []


process_dir("images")
