import re
import spacy
from .base import Agent

nlp = spacy.load("en_core_web_sm")

class ClauseExtractorAgent(Agent):
    def __init__(self):
        super().__init__("ClauseExtractor")

    def run(self, text: str):
        # Split by numbered headings like "1. Title"
        clause_pattern = r'(?:\n|^)(\d{1,2}\.\s*[A-Z][^\n]*)'
        parts = re.split(clause_pattern, text)

        clauses = []
        current_title = "Preamble"
        current_text = ""

        for i, part in enumerate(parts):
            if re.match(r'\d{1,2}\.\s*[A-Z]', part):
                if current_text.strip():
                    clauses.append({
                        "id": f"clause-{len(clauses)+1}",
                        "title": current_title,
                        "text": current_text.strip(),
                        "category": self._categorize(current_title)
                    })
                current_title = part.strip()
                current_text = ""
            else:
                current_text += part + "\n"

        # Last clause
        if current_text.strip() or current_title != "Preamble":
            clauses.append({
                "id": f"clause-{len(clauses)+1}",
                "title": current_title,
                "text": current_text.strip(),
                "category": self._categorize(current_title)
            })
        return clauses

    def _categorize(self, title: str):
        title_lower = title.lower()
        if any(w in title_lower for w in ['payment', 'fee', 'price', 'compensation']):
            return 'payment'
        elif any(w in title_lower for w in ['termination', 'cancel', 'end']):
            return 'termination'
        elif any(w in title_lower for w in ['confidential', 'non-disclosure', 'nda']):
            return 'confidentiality'
        elif any(w in title_lower for w in ['liability', 'indemn', 'damage']):
            return 'liability'
        elif any(w in title_lower for w in ['govern', 'law', 'jurisdiction']):
            return 'governing_law'
        elif any(w in title_lower for w in ['renew', 'auto-renewal']):
            return 'renewal'
        else:
            return 'general'