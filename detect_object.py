import cv2
import numpy as np

def detect_object(path: str):
    image = cv2.imread(path)
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)


    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    new_mask = np.zeros_like(mask)
    cv2.drawContours(new_mask, contour, -1, (255), thickness=cv2.FILLED)

    cropped_object = cv2.bitwise_and(image, image, mask=new_mask)

    cv2.imshow('Cropped image', cropped_object)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_object

detect_object('picture/test.png')