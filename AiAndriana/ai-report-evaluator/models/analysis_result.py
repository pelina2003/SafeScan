# models/analysis_result.py

class AnalysisResult:
    def __init__(self, relevant: bool, confidence: float, summary: str = None):
        self.relevant = relevant
        self.confidence = confidence
        self.summary = summary
