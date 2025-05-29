from transformers import pipeline
from models.analysis_result import AnalysisResult


# AI Pipelines
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_analyzer = pipeline("sentiment-analysis")

valid_labels = ["φωτιά", "πλημμύρα", "ατύχημα", "επικίνδυνο περιστατικό", "καταστροφή"]
irrelevant_labels = ["αστείο", "ασαφές", "άσχετο", "χαζό"]

def analyze_text(text):
    print(f"📝 Ανάλυση περιγραφής: \"{text}\"")

    # Θεματική ταξινόμηση
    topic_result = classifier(text, valid_labels + irrelevant_labels)
    top_label = topic_result['labels'][0]
    score = topic_result['scores'][0]

    # Συναισθηματική ανάλυση
    sentiment = sentiment_analyzer(text)[0]['label']

    print(f"🔍 Θέμα: {top_label} (score: {score:.2f}) | Συναισθηματικός τόνος: {sentiment}")

    # Αν είναι άσχετο → απόρριψη
    if top_label in irrelevant_labels:
        return AnalysisResult(relevant=False, confidence=score, summary=top_label)

    # Αν είναι σχετικό → αποδοχή ανεξαρτήτως score
    if top_label in valid_labels:
        return AnalysisResult(relevant=True, confidence=score, summary=top_label)

    # Αν είναι "άλλο" → απόρριψη
    return AnalysisResult(relevant=False, confidence=score, summary=top_label)
