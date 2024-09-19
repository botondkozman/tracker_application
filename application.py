from API.python.eyeware.client import TrackerClient
import time
import glob
import os
from PIL import Image, ImageTk
import tkinter as tk
import asyncio
import threading

images_path = "../../../Downloads/parquet_images"
images = None
tracker = None
close_event = None

def initialize_tracker():
    global tracker
    tracker = TrackerClient()

def connect_tracker():
    while not tracker.connected:
        MESSAGE_PERIOD_IN_SECONDS = 1
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")

async def tracking_cursor_position():
    global close_event
    while not close_event.is_set():
        screen_gaze = tracker.get_screen_gaze_info()
        print("Coordinates: <x=%5.3f px, y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))
        await asyncio.sleep(0.1)

def parse_folder():
    global images
    images = glob.glob(os.path.join(images_path, '*.*'))

    if not images:
        print("The folder does not contains images")

def show_image_tk(image_path, close_event):
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

    number_label = tk.Label(root, text = "Give a rate:")
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
            on_close()

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
    global show_image_task
    start_time = time.time()

    show_image_task = asyncio.ensure_future(show_image(image_path))
    tracking_task = asyncio.ensure_future(tracking_cursor_position())

    await show_image_task
    await tracking_task

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

async def main():
    initialize_tracker()
    parse_folder()
    connect_tracker()
    if tracker.connected:
        for image in images:
            await process_image(image)
    else:
        print("No connection with tracker server")

if __name__ == "__main__":
    print("Running")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()