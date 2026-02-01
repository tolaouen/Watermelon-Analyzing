from extensions import db
from datetime import datetime

class Symptoms:
    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.Datetime, default=datetime.utcnow())
    updated_at = db.Column(db.Datetime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # relation with disease table
    diseases = db.relationship('Diseases', secondary='disease_symptoms', back_populates='symptoms')
    rules = db.relationship('Rules', secondary='rule_symptoms', back_populates='symptoms')

    
    def __repr__(self):
        return f'<Symptom {self.name}>'

    
