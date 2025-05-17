import json
import random


class IntentProcessor:
    def __init__(self,intents_file):
        with open(intents_file,encoding='utf-8') as file:
            data = json.load(file)
            self.intents = data["intents"] if isinstance(data,dict) and "intents" in data else data

    def get_patterns_and_labels(self):
        patterns = []
        labels = []

        for intent_data in self.intents:
            intent = intent_data["tag"]
            for pattern in intent_data["patterns"]:
                patterns.append(pattern)
                labels.append(intent)
        return patterns,labels
    
    def get_response(self,intent):
        for intent_data in self.intents:
            if intent_data["tag"] == intent:
                return random.choice(intent_data["responses"])
        return self.suggest_question()

    def suggest_question(self):
        sample_patterns = []
        for intent_data in self.intents:
            if intent_data["patterns"]:
                sample_patterns.append(random.choice(intent_data["patterns"]))
        if sample_patterns:
            suggestions = ", ".join(f"\"{p}\"" for p in sample_patterns)
            return f"Δεν κατάλαβα την ερώτησή σου. Δοκίμασε: {suggestions}."
        return "Δεν κατάλαβα την πρόθεση." #Alternative message ig there are no patterns in the json file