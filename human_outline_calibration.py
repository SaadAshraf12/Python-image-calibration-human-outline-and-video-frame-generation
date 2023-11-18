import cv2
import imageio
import os
import tkinter as tk
from tkinter import filedialog

# Function to select folder
def select_folder():
    folder_path = filedialog.askdirectory()
    return folder_path + '/'

# Function to select file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    return file_path

# Initialize Tkinter
root = tk.Tk()
root.withdraw()  # Hide the main window

# Select input video file
video_file = select_file()

# Select folder to save frames
frames_folder = select_folder() + 'frames/'

# Create a folder to store frames if it doesn't exist
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

vidcap = cv2.VideoCapture(video_file)

success, image = vidcap.read()
count = 0

while success:
    # Convert frame to grayscale for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection (adjust thresholds as needed)
    edges = cv2.Canny(gray, 100, 200)
    
    # Invert the edges to get a white outline on a black background
    edges = cv2.bitwise_not(edges)
    
    # Save processed frame as PNG image
    cv2.imwrite(f"{frames_folder}outline_{count}.png", edges)
    
    success, image = vidcap.read()
    count += 1

vidcap.release()

# Get the list of image filenames in the directory
images = [f"{frames_folder}outline_{i}.png" for i in range(count)]

# Create a list of imageio.imread() for each image filename
images_array = [imageio.imread(image) for image in images]

# Select folder to save GIF
gif_folder = select_folder()

# Ask for the name of the GIF file
gif_file = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")], initialdir=gif_folder)

# Save the images as a GIF
if gif_file:
    selected_images = [images_array[i] for i in range(0, count, max(count // 100, 1))]  # Choose frames wisely to limit GIF size
    imageio.mimsave(gif_file, selected_images, duration=0.1)  # Adjust duration as needed
