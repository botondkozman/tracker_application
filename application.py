from API.python.eyeware.client import TrackerClient
import time
import glob
import os
from PIL import Image, ImageTk
import tkinter as tk
import asyncio
import threading
import random
from backend import Database

username = "boti"
images_path = "./parquet_images"
images = None
tracker = None
close_event = None
cred = "./credential/odin-demo-2c3f0-firebase-adminsdk-dbjmc-732853d4fe.json"
db = Database(cred)
rating = -1
coordinates = []
elapsed_time = None
size = None
name = None


def initialize_tracker():
    global tracker
    tracker = TrackerClient()

def connect_tracker():
    while not tracker.connected:
        MESSAGE_PERIOD_IN_SECONDS = 1
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")

async def tracking_cursor_position():
    global close_event, coordinates
    while not close_event.is_set():
        screen_gaze = tracker.get_screen_gaze_info()
        coordinates.append({"coordinate":[screen_gaze.x, screen_gaze.y]})
        await asyncio.sleep(0.1)

def parse_folder():
    global images
    images = glob.glob(os.path.join(images_path, '*.*'))
    random.shuffle(images)
    if not images:
        print("The folder does not contains images")

def write_database():
    global images_path, size, rating, elapsed_time, coordinates, username
    field_pciture = {"path": images_path.split('/')[-1] + '/' + name,
             "size": size}
    field_user = {name.split('.')[0] : {"picture": name.split('.')[0],
             "rating": rating,
             "time": elapsed_time,
             "coordinates": coordinates}}
    coordinates = []
    rating = -1
    db.add_data("picture", name.split('.')[0], field_pciture)
    if (db.has_document("users", username)):
        db.update_data("users", username, field_user)
    else:
        db.add_data("users", username, field_user)

def show_image_tk(image_path, close_event):
    global size, name
    root = tk.Tk()
    root.title("Images")

    screen_width = min(root.winfo_screenwidth(), 1600)
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    img = Image.open(image_path)
    img = img.resize((screen_width, screen_height - 50), Image.LANCZOS)
    size = img.size
    name = os.path.basename(image_path)

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image = img_tk)
    label.pack()

    number_label = tk.Label(root, text = "Give a rate:")
    number_label.pack()

    number_entry = tk.Entry(root)
    number_entry.pack()
    root.focus_force()
    number_entry.focus_force()

    def on_submit(event):
        global rating
        if event.char.isdigit():
            user_input = number_entry.get()
            number_entry.delete(0, tk.END)
            number = int(user_input)
            rating = number
            on_close()
        else:
            number_entry.get()
            number_entry.delete(0, tk.END)

    root.bind('<Key>', on_submit)

    def on_close():
        print("closing")
        close_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

async def show_image(image_path):
    global close_event
    close_event = threading.Event()

    tk_thread = threading.Thread(target=show_image_tk, args=(image_path, close_event))
    tk_thread.start()

    while not close_event.is_set():
        await asyncio.sleep(0.1)

    tk_thread.join()

async def process_image(image_path):
    global show_image_task, elapsed_time
    start_time = time.time()

    show_image_task = asyncio.ensure_future(show_image(image_path))
    tracking_task = asyncio.ensure_future(tracking_cursor_position())

    await show_image_task
    await tracking_task

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    write_database()

async def main():
    initialize_tracker()
    parse_folder()
    connect_tracker()
    if tracker.connected:
        for image in images:
            image_name = image.split("\\")[-1].split(".")[0]
            if not db.has_field("users", username, image_name):
                await process_image(image)
        print('All picture is rated')
    else:
        print("No connection with tracker server")

if __name__ == "__main__":
    print("Running")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()