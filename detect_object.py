from rembg import remove
from PIL import Image
import numpy as np

def detect_object(path: str):
    image = Image.open(path)
    cropped_image = remove(image)
    cropped_image.save('picture/ball_cropped.png')


def convert_image_bw(image_path, output_path):
    # Open image and convert to grayscale
    img = Image.open(image_path).convert("L")
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Apply transformation: nonzero pixels -> black (0), zero pixels -> white (255)
    processed_array = np.where(img_array == 0, 255, 0).astype(np.uint8)
    
    # Convert back to image and save
    processed_img = Image.fromarray(processed_array)
    processed_img.save(output_path)

detect_object('picture/ball.png')
convert_image_bw('picture/ball_cropped.png', 'picture/ball2.png')