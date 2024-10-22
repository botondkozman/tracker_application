import firebase_admin
from firebase_admin import credentials, firestore

class Database:
    def __init__(self, credential_path):
        
        try:
            cred = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("Firebase connection established.")
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            raise

    def add_data(self, collection_name, document_id, data):
        
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.set(data)
            print(f"Document {document_id} added to {collection_name}.")
        except Exception as e:
            print(f"Failed to add data: {e}")

    def get_data(self, collection_name, document_id):
        
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                print(f"Document {document_id} data: {doc.to_dict()}")
                return doc.to_dict()
            else:
                print(f"No document found with ID: {document_id}")
                return None
        except Exception as e:
            print(f"Failed to get data: {e}")
            return None
        
    def get_dataCollection(self, collection_name):
        
        doc_ref = self.db.collection(collection_name)
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
            return doc.to_dict()
            

    def update_data(self, collection_name, document_id, new_data):
        
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.update(new_data)
            print(f"Document {document_id} updated.")
        except Exception as e:
            print(f"Failed to update data: {e}")