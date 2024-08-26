from API.python.eyeware.client import TrackerClient
import time
import glob
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog
import numpy as np


images_path = "../../../Downloads/parquet_images"
images = None
tracker = None
root = None

def initialize_tracker():
    tracker = TrackerClient()
    tracker.initialize()

def start_tracker():
    try:
        tracker.start()
        print("Tracking started")
    except Exception as e:
        print(f"Failed to start tracking: {e}")

def tracking_cursor_position():
    tracking_data = tracker.get_tracking_data()
    screen_gaze = tracker.get_screen_gaze_info()
    gaze_x = tracking_data.get("gaze_x")
    gaze_y = tracking_data.get("gaze_y")
    print(f"Gaze coordinates: X={gaze_x}, Y={gaze_y}, time={time.time()}")
    print("Coordinates: <x=%5.3f px, y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))

def stop_tracker():
    tracker.stop()
    print("Tracking stopped")

def parse_folder():
    global images
    images = glob.glob(os.path.join(images_path, '*.*'))

    if not images:
        print("The folder does not contains images")

def initialize_window():
    global root
    root = tk.Tk()
    root.title("Images")

def show_image_with_input(image_path):
    img = Image.open(image_path)

    #screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()
    #img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=img_tk)
    label.pack()

    number_label = tk.Label(root, text="Give a rate:")
    number_label.pack()

    number_entry = tk.Entry(root)
    number_entry.pack()

    def on_submit(event):
        if event.char.isdigit():
            user_input = number_entry.get()
            number_entry.delete(0, tk.END)
            number_entry.insert(0, user_input)
            number = int(user_input)
            print(f"Rating: {number}")

    root.bind('<Key>', on_submit)
    root.mainloop()

def delete_window():
    root.quit()

if __name__ == "__main__":
    initialize_tracker()
    start_tracker()
    parse_folder()
    initialize_window()
    if tracker.connected:
        for image in images:
            start_time = time.time()
            tracking_cursor_position()
            show_image_with_input(image)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
        delete_window()
        stop_tracker()
    else:
        print("No connection with tracker server")