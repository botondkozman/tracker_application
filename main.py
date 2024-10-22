import cv2
import time
import firebase_admin
from firebase_admin import credentials, firestore
from backend import Database
from dominant_color import *

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

