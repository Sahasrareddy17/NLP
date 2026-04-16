import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_language(text):
    vector = vectorizer.transform([text])
    result = model.predict(vector)
    return result[0]