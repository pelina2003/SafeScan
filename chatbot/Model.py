from NLPProcessor import NLPProcessor
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import logging

logging.basicConfig(filename='model_predictions.log',level=logging.INFO,encoding='utf-8')

class Model:
    def __init__(self):
        self._vectorizer = CountVectorizer()
        self._model = MultinomialNB()
        
    def train(self,patterns,labels):
        cleaned = [NLPProcessor().nlp_process(p) for p in patterns]
        X = self._vectorizer.fit_transform(cleaned)
        self._model.fit(X, labels)

    def save_model(self,model_file="model.pkl",vectorizer_file="vectorizer.pkl"):
        joblib.dump(self._model,model_file)
        joblib.dump(self._vectorizer,vectorizer_file)

    def load_model(self,model_file="model.pkl",vectorizer_file="vectorizer.pkl"):
        self._model = joblib.load(model_file)
        self._vectorizer = joblib.load(vectorizer_file)

    def predict(self,user_input):
        cleaned_input = NLPProcessor().nlp_process(user_input)
        vector = self._vectorizer.transform([cleaned_input])
        probabilities = self._model.predict_proba(vector)[0]
        max_prob = max(probabilities)
        predicted_index = probabilities.argmax()
        predicted_intent = self._model.classes_[predicted_index]
        logging.info(f"Input: {user_input}, Cleaned: {cleaned_input}, Probabilities: {probabilities}, Max Prob: {max_prob}, Predicted Intent: {predicted_intent}")
        if max_prob <0.4:
            return "αγνωστη_πρόθεση"
        return predicted_intent