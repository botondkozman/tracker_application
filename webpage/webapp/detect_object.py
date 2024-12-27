import cv2
import numpy as np
import os

def detect_object(path: str) -> str:
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4:
        b, g, r, a = cv2.split(image)
    else:
        b, g, r = cv2.split(image)
        a = np.ones_like(b) * 255

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    avg_top_left = int(sum((b[0, 0], g[0, 0], r[0, 0])) / 3)
    tolerance = 10
    lower_threshold = max(0, avg_top_left - tolerance)
    upper_threshold = min(255, avg_top_left + tolerance)
    #mask = cv2.inRange(gray_image, lower_threshold, upper_threshold)

    _, mask = cv2.threshold(gray_image, 245, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    new_mask = np.zeros_like(mask)
    cv2.drawContours(new_mask, contour, -1, (255), thickness=cv2.FILLED)

    alpha = new_mask
    transparent_image = cv2.merge((b, g, r, alpha))

    filename = path.split("/")[-1].split(".")[0] + "_cropped.png"
    file_path = "/".join(path.split("/")[:-1])

    cv2.imwrite(os.path.join(file_path , filename), transparent_image)
    return "images/" + filename