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

if __name__ == "__main__":
    image_path = "../../../Downloads/parquet_images/image_3.png"
    image = cv2.imread(image_path)

    size=(250, 250)
    quantized_image, labels = quantize_image(image, palette_rgb)
    cv2.imshow('photo',quantized_image)
    quantized_image=cv2.resize(quantized_image, size)
    height, width, channels = quantized_image.shape
    color_names = list(color_palette.keys())
    dominant_color, dominant_label = get_dominant_color(labels, color_names)
    print(f'The dominant color is: {dominant_color}')