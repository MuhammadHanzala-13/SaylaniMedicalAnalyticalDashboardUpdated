import re
from datetime import datetime

class IntentParser:
    def __init__(self):
        self.intents = {
            "book_appointment": [r"book", r"appointment", r"schedule", r"visit", r"see a doctor"],
            "cancel_appointment": [r"cancel", r"reschedule"],
            "get_info": [r"info", r"about", r"what is", r"tell me", r"symptoms", r"treatment"],
            "check_availability": [r"available", r"when", r"time", r"open"]
        }
        
    def parse(self, text):
        text = text.lower()
        intent = "unknown"
        
        # Simple keyword matching for intent
        max_score = 0
        for int_name, keywords in self.intents.items():
            score = sum(1 for k in keywords if re.search(k, text))
            if score > max_score:
                max_score = score
                intent = int_name
                
        entities = self.extract_entities(text)
        return {"intent": intent, "entities": entities}

    def extract_entities(self, text):
        entities = {}
        
        # Extract Doctor Name (Dr. X)
        doctor_match = re.search(r"dr\.?\s+([a-z]+(\s+[a-z]+)?)", text)
        if doctor_match:
            entities["DOCTOR_NAME"] = doctor_match.group(0).title()
            
        # Extract Specialty (Simple list based)
        specialties = ["cardiology", "pediatrics", "dermatology", "neurology", "orthopedics", "general practice", "ophthalmology", "gynecology"]
        for s in specialties:
            if s in text:
                entities["SPECIALTY"] = s.title()
                
        # Extract Branch/Area (Simple heuristic)
        areas = ["gulshan", "korangi", "saddar", "nazimabad", "malir", "clifton", "pechs"]
        for a in areas:
            if a in text:
                entities["AREA"] = a.title()
                
        # Extract Disease (Simple heuristic)
        diseases = ["cold", "flu", "fever", "dengue", "fracture", "pain", "headache", "migraine"]
        for d in diseases:
            if d in text:
                entities["DISEASE"] = d.title()
                
        return entities

if __name__ == "__main__":
    parser = IntentParser()
    sample = "I want to book an appointment with Dr. Ayesha for flu in Gulshan"
    print(parser.parse(sample))
