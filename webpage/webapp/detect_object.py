from rembg import remove
from PIL import Image
import os

def detect_object(path: str) -> str:
    image = Image.open(path)
    cropped_image = remove(image)
    
    filename = path.split("/")[-1].split(".")[0] + "_cropped.png"
    file_path = "/".join(path.split("/")[:-1])

    cropped_image.save(os.path.join(file_path , filename))
    return "images/" + filename