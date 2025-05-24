from NLPProcessor import NLPProcessor
from IntentProcessor import IntentProcessor
from Model import Model
import hashlib
import os
import logging

def compute_file_hash(filename):
    with open(filename, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

class Chatbot:
    def __init__(self,intents_file):
        logging.basicConfig(filename='chatbot.log',level=logging.INFO)

        self._intents_file = intents_file
        self._intent_processor = IntentProcessor(intents_file)
        self._nlp_processor = NLPProcessor()
        self._model_trainer = Model()
        self._hash_file = "intents.hash"
        self._model_file = "model.pkl"
        self._vectorizer_file = "vectorizer.pkl"

        self.initialize()

    def train(self):
        patterns,labels = self._intent_processor.get_patterns_and_labels()
        self._model_trainer.train(patterns,labels)
        self._model_trainer.save_model(self._model_file,self._vectorizer_file)

    def get_response(self,user_input):
        intent = self._model_trainer.predict(user_input)
        response = self._intent_processor.get_response(intent)
        logging.info(f"Input: {user_input}, Intent: {intent}, Response: {response}")
        return response
    
    def initialize(self):
        current_hash = compute_file_hash(self._intents_file)
        saved_hash = " "

        #If there is saved hash
        if os.path.exists(self._hash_file):
            with open(self._hash_file,"r") as f:
                saved_hash = f.read()

        #If the hash remaim the same and there are saved files we load the model
        if current_hash == saved_hash and os.path.exists(self._model_file):
            print("Loading the saved model.")
            self._model_trainer.load_model(self._model_file,self._vectorizer_file)
        else:
            print("Training a new model.")
            self.train()
            #Save the new hash
            with open(self._hash_file,"w") as f:
                f.write(current_hash)
    