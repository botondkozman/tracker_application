from backend import Database
import cv2

if __name__ == "__main__":
    images_path = "../../../Downloads/parquet_images/image_6.png"
    cred = "./credential/odin-demo-2c3f0-firebase-adminsdk-dbjmc-732853d4fe.json"
    db = Database(cred)
    user_data = db.get_data("users", "user1")
    picture_data = db.get_data("picture", "image_6")
    coordinates = user_data["image_6"]["coordinates"]
    objects = picture_data["objects"]
    image = cv2.imread(images_path)
    image = cv2.resize(image, (1280, 670))
    for coordinate in coordinates:
        point = (coordinate["coordinate"][0], coordinate["coordinate"][1])
        cv2.circle(image, point, radius=5, color=(0, 0, 255), thickness=-1)

    for obj in objects:
        origin_point = (int ((obj["rectangle"][0] - obj["rectangle"][2] / 2) * 1280), int((obj["rectangle"][1] - obj["rectangle"][3]/2) * 670))
        end_point = (int((obj["rectangle"][0] + obj["rectangle"][2] / 2) * 1280), int((obj["rectangle"][1] + obj["rectangle"][3] / 2) * 670))
        cv2.rectangle(image, origin_point, end_point, color=(0, 255, 0), thickness=2)

    cv2.imshow('Kép', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()