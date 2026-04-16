import pickle

# load trained model
model = pickle.load(open("../ml_model/model.pkl","rb"))

def predict(features):

    prediction = model.predict([features])[0]

    confidence = max(model.predict_proba([features])[0])

    return prediction, confidence