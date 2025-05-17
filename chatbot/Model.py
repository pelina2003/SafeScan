from NLPProcessor import NLPProcessor
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class Model:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        
    def train(self,patterns,labels):
        cleaned = [NLPProcessor().nlp_process(p) for p in patterns]
        X = self.vectorizer.fit_transform(cleaned)
        self.model.fit(X, labels)

    def save_model(self,model_file="model.pkl",vectorizer_file="vectorizer.pkl"):
        joblib.dump(self.model,model_file)
        joblib.dump(self.vectorizer,vectorizer_file)

    def load_model(self,model_file="model.pkl",vectorizer_file="vectorizer.pkl"):
        self.model = joblib.load(model_file)
        self.vectorizer = joblib.load(vectorizer_file)

    def predict(self,user_input):
        cleaned_input = NLPProcessor().nlp_process(user_input)
        vector = self.vectorizer.transform([cleaned_input])
        probabilities = self.model.predict_proba(vector)[0]
        max_prob = max(probabilities)
        predicted_index = probabilities.argmax()
        predicted_intent = self.model.classes_[predicted_index]
        if max_prob <0.3:
            return "αγνωστη_πρόθεση"
        return predicted_intent