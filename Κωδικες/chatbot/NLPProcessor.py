import spacy

class NLPProcessor:
    def __init__(self,language_model="el_core_news_sm"):
        self._nlp = spacy.load(language_model)

    def nlp_process(self,text):
        doc = self._nlp(text)
        tokens = [ 
            token.lemma_.lower() 
            for token in doc
            if not token.is_stop and not token.is_punct
        ]
    
        return " ".join(tokens)

