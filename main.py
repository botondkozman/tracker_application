import cv2
import time
import firebase_admin
from firebase_admin import credentials, firestore
from backend import Database
from dominant_color import *
from cursor_position import *


credential_path = 'C:\\BME\\Msc\\3.félév\\startupunk\\tracker_application\\credential\\odin-demo-2c3f0-firebase-adminsdk-dbjmc-732853d4fe.json'
db = Database(credential_path)
db.add_data('users', 'odin_boss', {'name': 'Fabian Kalman', 'age': 24})
db.add_data('users', 'odin_worker', {'name': 'Bende Barcza', 'age': 24})
#db.update_data('users', 'user123', {'age': 31})   
#db.delete_data('users', 'user123')

user_data = db.get_data('users', 'odin_boss')

image_data=db.get_data_collection('picture')
#print(f"Retrieved data: {user_data}")
#if user_data:
  #  print(f"Retrieved data: {user_data}")
image_data=db.get_data('picture', 'image_5')


""" 
print(f"Image Path: {image_data['path']}")
print(f"Dominant Color: {image_data['dominant_color']}")
print(f"Size (Width x Height): {image_data['size'][0]} x {image_data['size'][1]}")
print("\nSorted Objects:")
 """

#random kép betéve, ezen kell változtatni
image_path = r"cr7.png"
image = cv2.imread(image_path)

tracking_data = prepare_tracking_data(image_data)

#random_pixels=<x=485.000 px, y=302.000 px>



#ebből legyen function?
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", check_mouse_in_rect, tracking_data)

while True:
    display_image = display_image_with_rectangles(image, tracking_data)
    cv2.imshow("Image", display_image)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cv2.destroyAllWindows()
print_interaction_results(tracking_data)
