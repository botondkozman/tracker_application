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
is_tracking_needed = False

def initialize_tracker():
    global tracker
    tracker = TrackerClient()

def connect_tracker():
    while not tracker.connected :
        MESSAGE_PERIOD_IN_SECONDS = 1
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")

async def tracking_cursor_position():
     while is_tracking_needed:
        screen_gaze = tracker.get_screen_gaze_info()
        print("Coordinates: <x=%5.3f px, y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))

def parse_folder():
    global images
    images = glob.glob(os.path.join(images_path, '*.*'))

    if not images:
        print("The folder does not contains images")

async def show_image(image_path):
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
        global is_tracking_needed
        if event.char.isdigit():
            user_input = number_entry.get()
            number_entry.delete(0, tk.END)
            number_entry.insert(0, user_input)
            number = int(user_input)
            print(f"Rating: {number}")
            root.destroy()
            is_tracking_needed = False

    root.bind('<Key>', on_submit)
    
    def run_tkinter_loop():
        root.mainloop()

    # Run Tkinter event loop in a separate thread
    tkinter_thread = threading.Thread(target=run_tkinter_loop)
    tkinter_thread.start()

    # Wait for the Tkinter thread to finish
    tkinter_thread.join()

async def process_image(image_path) :
    global is_tracking_needed
    start_time = time.time()
    is_tracking_needed = True
    tracking_task = asyncio.ensure_future(tracking_cursor_position())
    show_image_taks = asyncio.ensure_future(show_image(image_path))
    done, pending = await asyncio.wait([show_image_taks, tracking_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        print(f"Canceling {task.get_name()}")
        task.cancel()

    for task in done:
        await task
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