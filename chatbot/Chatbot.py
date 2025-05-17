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

        self.intents_file = intents_file
        self.intent_processor = IntentProcessor(intents_file)
        self.nlp_processor = NLPProcessor()
        self.model_trainer = Model()
        self.hash_file = "intents.hash"
        self.model_file = "model.pkl"
        self.vectorizer_file = "vectorizer.pkl"

        self.initialize()

    def train(self):
        patterns,labels = self.intent_processor.get_patterns_and_labels()
        self.model_trainer.train(patterns,labels)
        self.model_trainer.save_model(self.model_file,self.vectorizer_file)

    def get_response(self,user_input):
        intent = self.model_trainer.predict(user_input)
        response = self.intent_processor.get_response(intent)
        logging.info(f"Input: {user_input}, Intent: {intent}, Response: {response}")
        return response
    
    def initialize(self):
        current_hash = compute_file_hash(self.intents_file)
        saved_hash = " "

        #If there is saved hash
        if os.path.exists(self.hash_file):
            with open(self.hash_file,"r") as f:
                saved_hash = f.read()

        #If the hash remaim the same and there are saved files we load the model
        if current_hash == saved_hash and os.path.exists(self.model_file):
            print("Loading the saved model.")
            self.model_trainer.load_model(self.model_file,self.vectorizer_file)
        else:
            print("Training a new model.")
            self.train()
            #Save the new hash
            with open(self.hash_file,"w") as f:
                f.write(current_hash)
    