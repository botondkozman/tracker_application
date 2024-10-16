import firebase_admin
from firebase_admin import credentials, firestore

cred = firebase_admin.credentials.Certificate("./credential/odin-demo-2c3f0-firebase-adminsdk-dbjmc-732853d4fe.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

def add_data(collection, document, field):
    doc_ref = db.collection(collection).document(document)
    doc_ref.set(field)

def get_data(collection):
    users_ref = db.collection(collection)
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

if __name__ == "__main__":
    test = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "age": 30,
        "rate": 5,
        "list": [1, 2, 3, 4]
    }
    add_data("data", "user2", test)
    get_data("data")