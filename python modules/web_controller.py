import firebase_admin
from firebase_admin import credentials, firestore, storage


# Put your local file path


# Opt : if you want to make public access from the URL

class web_controller:
    def __init__(self, json_cred_path, storage_bucket):
        self.app = firebase_admin.initialize_app(credentials.Certificate(json_cred_path), {'storageBucket': storage_bucket})
        self.update_firebase("signals", "gameReady", False)
        self.update_firebase("signals", "choosePieceReady", False)
        self.update_firebase("signals", "hint", -1)
        self.update_firebase("signals", "pieceChosen", -1)
        self.update_firebase("signals", "CurrPhotoURL", "")



    def upload_photo_and_return_public_url(self, photo_path):
        bucket = storage.bucket()
        blob = bucket.blob(photo_path)
        blob.upload_from_filename(photo_path)
        blob.make_public()
        return blob.public_url


    def update_firebase(self, collection, document, new_val):
        db = firestore.client()
        doc_ref = db.collection(collection).document(document)
        doc_ref.update({
            u'val': new_val,
        })
        print("updated document " + document + " in firebase to " + str(new_val))

    def wait_for_needed_val_input(self, collection, document, needed_val):
        print("waiting for " + str(needed_val) + "in document " + document)
        while self.get_value_from_firebase(collection, document) is not needed_val:
            pass
        print("found!!!")

    def wait_for_new_val_input(self, collection, document, old_val):
        print("waiting for document " + document + " to change")
        while self.get_value_from_firebase(collection, document) == old_val:
            pass
        print("changed!!!")
        if (document == "pieceChosen"):
            return self.get_value_from_firebase(collection, document)


    def delete_photo_from_firebase(self, photo_path):
        bucket = storage.bucket()
        blob = bucket.blob(photo_path)
        blob.upload_from_filename(photo_path)
        blob.delete()

    def get_value_from_firebase(self, collection, document):
        db = firestore.client()
        doc_ref = db.collection(collection).document(document)
        return doc_ref.get().to_dict()["val"]









"""
cred = credentials.Certificate('./Puzzkey.json')

app = firebase_admin.initialize_app(cred, {'storageBucket': 'puzz-a02e2.appspot.com'})
fileName = "small_yorai.jpeg"
bucket = storage.bucket()
blob = bucket.blob(fileName)


blob.upload_from_filename(fileName)
db = firestore.client()
doc_ref = db.collection(u'signals').document(u'CurrPhotoURL')
blob.make_public()

doc_ref.update({
    u'val': blob.public_url,
})

x = -1
while (x == -1):
    x = doc_ref.get().to_dict()['val']

print(x)
"""