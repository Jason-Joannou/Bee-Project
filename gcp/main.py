from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

model = None

BUCKET_NAME = "bee_image_bucket"
class_names=['Apis mellifera', 'Bombus Affinis']
    
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def predict(request):

    global model
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    if model is None:
        download_blob(BUCKET_NAME,"models/Honey_and_BumbleBees_V3.h5", "/tmp/Honey_and_BumbleBees_V3.h5")
        model = tf.keras.models.load_model("/tmp/Honey_and_BumbleBees_V3.h5")

    image = request.files["file"]

    image = np.array(Image.open(image).convert("RGB").resize((256,256)))
    #image = image/255
    img_arr = np.expand_dims(image, axis=0).astype(np.float32)

    predictions = model.predict(img_arr)
    print(predictions)
    
    predicted_class = class_names[np.argmax(predictions[0])]
    print(predicted_class)
    confidence = round(100*(np.max(predictions[0])), 2)
    confidence = confidence/100.0

    res = {"class": predicted_class, "confidence": confidence}
    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (res, 200, headers)


    




