from API.python.eyeware.client import TrackerClient
import time
import glob
import os
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np

images_path = "../../../Downloads/parquet_images"
images = None
tracker = None

def initialize_tracker():
    global tracker
    tracker = TrackerClient()
    print(tracker.connected)
    print(tracker)

def connect_tracker():
    while (tracker.connected == False) :
        MESSAGE_PERIOD_IN_SECONDS = 2
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")

def tracking_cursor_position():
    screen_gaze = tracker.get_screen_gaze_info()
    print("Coordinates: <x=%5.3f px, y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))

def parse_folder():
    global images
    images = glob.glob(os.path.join(images_path, '*.*'))

    if not images:
        print("The folder does not contains images")

def show_image_with_input(image_path):
    root = tk.Tk()
    root.title("Images")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    img = Image.open(image_path)
    img = img.resize((screen_width, screen_height - 50), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image = img_tk)
    label.pack()

    number_label = tk.Label(root, text="Give a rate:")
    number_label.pack()

    number_entry = tk.Entry(root)
    number_entry.pack()
    root.focus_force()
    number_entry.focus_force()

    def on_submit(event):
        if event.char.isdigit():
            user_input = number_entry.get()
            number_entry.delete(0, tk.END)
            number_entry.insert(0, user_input)
            number = int(user_input)
            print(f"Rating: {number}")
            root.destroy()

    root.bind('<Key>', on_submit)
    root.mainloop()

if __name__ == "__main__":
    initialize_tracker()
    parse_folder()
    connect_tracker()
    if tracker.connected:
        for image in images:
            start_time = time.time()
            tracking_cursor_position()
            show_image_with_input(image)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
    else:
        print("No connection with tracker server")