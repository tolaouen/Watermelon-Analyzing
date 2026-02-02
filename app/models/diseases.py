from datetime import datetime
from typing import List

from extensions import db


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    causes = db.Column(db.Text, nullable=False)
    treatments = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def symptoms_list(self) -> List[str]:
        """
        Return the list of symptom names associated with this disease.

        The symptoms are stored as a single comma-separated string in the
        `symptoms` column; this helper parses and normalises them.
        """
        if not self.symptoms:
            return []
        return [s.strip() for s in self.symptoms.split(",") if s.strip()]

    def calculate_match_score(self, user_symptoms: list[str]) -> float:
        """
        Calculate how well this disease matches the given user symptoms.

        The score is a simple percentage of matching symptoms between the
        user's selected symptoms and this disease's known symptoms.
        """
        disease_symptoms = set(self.symptoms_list)
        if not disease_symptoms:
            return 0.0

        user_set = {s for s in user_symptoms if s}
        if not user_set:
            return 0.0

        matches = disease_symptoms.intersection(user_set)
        return (len(matches) / len(disease_symptoms)) * 100.0

    def __repr__(self):
        return f"<Disease {self.name}>"
