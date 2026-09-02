import logging
from typing import Optional
from transformers import pipeline
from src.analyzer.parser import LogEntry

class AIAgentParser:
    """
    Real AI-powered parser using Hugging Face transformers 
    for zero-shot log level classification.
    """
    def __init__(self) -> None:
        logging.info("Loading AI model (Hugging Face Zero-Shot Classifier)... This may take a moment.")
        # We use a lightweight zero-shot classification pipeline
        # It classifies text into candidate labels without prior specific training
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        self.candidate_labels = ["INFO", "WARNING", "ERROR"]

    def parse_line(self, line: str) -> Optional[LogEntry]:
        line = line.strip()
        if not line:
            return None
        
        try:
            # Ask the AI model to classify the log message
            result = self.classifier(line, self.candidate_labels)
            # Get the label with the highest score
            best_label = result["scores"][0]
            top_category = result["labels"][0]
            
            # If confidence is high enough (e.g., > 0.5), accept it
            if best_label > 0.4:
                return LogEntry(level=top_category, message=f"[AI-Classified] {line}")
                
        except Exception as e:
            logging.error(f"AI classification failed: {e}")
            
        return None