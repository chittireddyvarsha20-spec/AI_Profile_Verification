import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# load dataset
data = pd.read_csv("dataset.csv")

# split features and label
X = data.drop("label", axis=1)
y = data["label"]

# create model
model = RandomForestClassifier()

# train model
model.fit(X, y)

# save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained successfully and saved as model.pkl")