from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
import io
import base64
#import models from settings.py
from MoneyVision.settings import ENCRYPTOR_MODEL, CLASSIFIER_MODEL, LABELS_ENCODED


def resize_and_square(img, output_path, size):
    width, height = img.size
    new_size = max(width, height)
   #if avarage brightness of the image is greater than 200, then the image is considered as white
    if np.mean(img) > 200:
        squared_img = Image.new("RGB", (new_size, new_size), (255, 255, 255))
    else:
        squared_img = Image.new("RGB", (new_size, new_size), (0, 0, 0))
    paste_position = ((new_size - width) // 2, (new_size - height) // 2)
    squared_img.paste(img, paste_position)
    resized_img = squared_img.resize((size, size), Image.LANCZOS)
    return resized_img

def identyfy_bill(image_file):
    model = ENCRYPTOR_MODEL
    image_file = Image.open(image_file)
    img = resize_and_square(image_file, image_file, 224)
    img = tf.keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    predictions = model.predict(img)
    classify_model = CLASSIFIER_MODEL
    score = classify_model.predict(predictions)
    labels_encoded = LABELS_ENCODED
    return ({
        "currency": labels_encoded.columns[np.argmax(score)].split(':')[0],
        'denomination': labels_encoded.columns[np.argmax(score)].split(':')[1].split("_")[0],
        "confidence": np.max(score)*100,
    })


if __name__ == "__main__":
    print(identyfy_bill('100rupes.jpg'))
