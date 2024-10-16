import cv2
import time

image_path = "../../../Downloads/parquet_images/image_2.png"
image = cv2.imread(image_path)
height, width, channel = image.shape

cv2.imshow('original',image)
data = [
    {
        "label": "laptop",
        "rectangle": [0.737857, 0.323604, 0.140476, 0.178511]
    },
    {
        "label": "phone",
        "rectangle": [0.500000, 0.500000, 0.100000, 0.150000]
    }
]

tracking_data = []
for obj in data:
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

def check_mouse_in_rect(event, mx, my, flags, param):
    global tracking_data
    
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


cv2.namedWindow("Image")
cv2.setMouseCallback("Image", check_mouse_in_rect)

while True:
    display_image = image.copy()
    for obj in tracking_data:
        x, y, w, h = obj['x'], obj['y'], obj['w'], obj['h']
        cv2.rectangle(display_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow("Image", display_image)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

for obj in tracking_data:
    if obj['mouse_is_inside']:
        time_spent = time.time() - obj['start_time']
        obj['touch_events'].append(time_spent)
      
    print(f"\nObject '{obj['label']}' was touched {len(obj['touch_events'])} times")
    for i, duration in enumerate(obj['touch_events']):
        print(f"Occasion {i+1}: {duration:.2f} seconds")

    total_time = sum(obj['touch_events'])
    print(f"Total time inside the '{obj['label']}': {total_time:.2f} seconds")