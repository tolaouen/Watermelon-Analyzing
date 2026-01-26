from extensions import db
import json
from datetime import datetime

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    symptoms = db.Column(db.Text, nullable=False)  
    causes = db.Column(db.Text, nullable=False)
    treatments = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Disease {self.name}>'
    
    @property
    def symptoms_list(self):
        """Get symptoms as list"""
        if isinstance(self.symptoms, str):
            try:
                return json.loads(self.symptoms)
            except:
                return self.symptoms.split(',')
        return self.symptoms
    
    def calculate_match_score(self, user_symptoms):
        """Calculate match percentage with user symptoms"""
        disease_symptoms = self.symptoms_list
        if not disease_symptoms or not user_symptoms:
            return 0

        # Simple overlap calculation (case insensitive)
        user_symptoms_lower = [s.lower() for s in user_symptoms]
        disease_symptoms_lower = [s.lower() for s in disease_symptoms]
        matches = len(set(user_symptoms_lower) & set(disease_symptoms_lower))
        return (matches / len(disease_symptoms)) * 100
