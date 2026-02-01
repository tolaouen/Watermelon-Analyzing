from extensions import db
import json
from datetime import datetime

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    causes = db.Column(db.Text, nullable=False)
    treatments = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with table symptoms 
    symptoms = db.relationship('Symptoms', secondary='disease_symptoms', back_populates='diseases')
    
    def __repr__(self):
        return f'<Disease {self.name}>'
