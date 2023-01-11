from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
import uvicorn


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


INPUT_SHAPE = (256,256)
MODEL = tf.keras.models.load_model("/Path")
CLASS_NAMES=['Apis mellifera', 'BumbleBee']

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    return image

def preproccesing(image:Image.Image):
    image = image.resize(INPUT_SHAPE)
    #image = np.asfarray(image)
    #image = image/255.0-1.0
    image = np.expand_dims(image,0)

    return image




@app.get("/alive")
async def alive():
    return {"status": "Alive"}


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = preproccesing(image)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    print(predicted_class, confidence)
    return {"class": predicted_class, "confidence": float(confidence)}



if __name__ == '__main__':
    uvicorn.run(app,host='localhost',port=8000)

