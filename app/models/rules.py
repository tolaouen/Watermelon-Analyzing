from extensions import db
from app.models.associations import disease_symptoms
from datetime import datetime

class Rules:
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    condition = db.Column(db.Boolean, default=False)
    answer = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    symptom = db.relationship('Symptoms', secondary=disease_symptoms, back_populates='Rules')
    
    def __repr__(self):
        return f'<Rule {self.name}>'

    

