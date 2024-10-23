import cv2
import time

def prepare_tracking_data(image_data):
    # Extract the width and height from the image_data
    width, height = image_data['size']
    # Extract the objects from the image_data
    objects = image_data['objects']

    tracking_data = []
    for obj in objects:
        x, y, w, h = obj['rectangle']
        x = int(x * width)
        y = int(y * height)
        w = int(w * width)
        h = int(h * height)
        tracking_data.append({
            'label': obj['label'],
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'mouse_is_inside': False,
            'touch_events': [],
            'start_time': 0
        })
    return tracking_data



def check_mouse_in_rect(event, mx, my, flags, param):
    tracking_data = param
    for obj in tracking_data:
        x, y, w, h = obj['x'], obj['y'], obj['w'], obj['h']

        if x <= mx <= x + w and y <= my <= y + h:
            if not obj['mouse_is_inside']:
                obj['mouse_is_inside'] = True
                obj['start_time'] = time.time()
        else:
            if obj['mouse_is_inside']:
                obj['mouse_is_inside'] = False
                time_spent = time.time() - obj['start_time']
                obj['touch_events'].append(time_spent)

def display_image_with_rectangles(image, tracking_data):
    display_image = image.copy()
    for obj in tracking_data:
        x, y, w, h = obj['x'], obj['y'], obj['w'], obj['h']
        cv2.rectangle(display_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return display_image

def print_interaction_results(tracking_data):
    for obj in tracking_data:
        if obj['mouse_is_inside']:
            time_spent = time.time() - obj['start_time']
            obj['touch_events'].append(time_spent)

        print(f"\nObject '{obj['label']}' was touched {len(obj['touch_events'])} times")
        for i, duration in enumerate(obj['touch_events']):
            print(f"Occasion {i+1}: {duration:.2f} seconds")

        total_time = sum(obj['touch_events'])
        print(f"Total time inside the '{obj['label']}': {total_time:.2f} seconds")

