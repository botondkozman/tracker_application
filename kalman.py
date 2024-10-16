import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import time

color_palette = {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'yellow': [255, 255, 0],
    'cyan': [0, 255, 255],
    'magenta': [255, 0, 255],
    'black': [0, 0, 0],
    'white': [255, 255, 255],
    'gray': [128, 128, 128],
    'purple': [128, 0, 128],
    'orange': [255, 165, 0],
    'pink': [255, 192, 203],
    'brown': [165, 42, 42],
    'lime': [0, 255, 0],
    'navy': [0, 0, 128],
    'olive': [128, 128, 0],
    'teal': [0, 128, 128],
    'maroon': [128, 0, 0],
    'silver': [192, 192, 192],
    'gold': [255, 215, 0]
}

palette_rgb = np.array(list(color_palette.values()), dtype=np.uint8)

def quantize_image(image, palette):
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=len(palette), random_state=0).fit(pixels)
    labels = kmeans.predict(pixels)
    quantized_image = palette[labels].reshape(image.shape)
    return quantized_image, labels

def get_dominant_color(labels, color_names):
    label_counts = Counter(labels)
    dominant_label = label_counts.most_common(1)[0][0]
    dominant_color_name = color_names[dominant_label]
    return dominant_color_name, dominant_label

def display_images(original, quantized, region=None):
      
    if region:
        x, y, w, h = region
        cv2.rectangle(original, (x, y), (x+w, y+h), (255, 255, 0), 2)
    combined_image = np.vstack((original, quantized))
    cv2.imshow('combined image',combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#ezmi

def find_largest_color_region(image, labels, target_label):
    mask = (labels == target_label).astype(np.uint8).reshape(image.shape[:2])
    num_labels, labels_im = cv2.connectedComponents(mask)

    max_label = 1
    max_size = 0
    for label in range(1, num_labels):
        size = np.sum(labels_im == label)
        if size > max_size:
            max_size = size
            max_label = label

    mask = (labels_im == max_label).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        return x, y, w, h
    return None

image_path = "../../../Downloads/parquet_images/image_2.png"
image = cv2.imread(image_path)
img=image
height, width, channels = image.shape
print(f"Image dimensions: width={width}, height={height}, channels={channels}")
cv2.imshow('original',image)

size=(250, 250)
image = cv2.resize(image, size)
quantized_image, labels = quantize_image(image, palette_rgb)
quantized_image=cv2.resize(quantized_image,size)
height, width, channels = quantized_image.shape
#print(f"QImage dimensions: width={width}, height={height}, channels={channels}")
color_names = list(color_palette.keys())
dominant_color = get_dominant_color(labels, color_names)

dominant_color, dominant_label = get_dominant_color(labels, color_names)
print(f'The dominant color is: {dominant_color}')

region = find_largest_color_region(image, labels, dominant_label)
display_images(image, quantized_image, region)

##############################################
#kurzorozás itt kezdődik
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
    
    display_image = img.copy()
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