import os
import pickle

# get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# correct model path
model_path = os.path.join(BASE_DIR, "model.pkl")

# load model
model = pickle.load(open(model_path, "rb"))


def predict(features):
    prediction = model.predict([features])[0]
    confidence = max(model.predict_proba([features])[0])
    return prediction, confidence
