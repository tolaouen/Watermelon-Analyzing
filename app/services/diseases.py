from typing import List, Optional

from extensions import db
from app.models.diseases import Disease


class DiseaseService:
    @staticmethod
    def seed_initial_diseases() -> None:
        """Seed initial knowledge base if empty."""
        if Disease.query.count() != 0:
            return

        initial_diseases = [
            {
                "name": "Anthracnose",
                "symptoms": [
                    "Brown spots on leaves",
                    "Angular spots on fruit",
                    "Stem lesions",
                ],
                "causes": "Fungus Colletotrichum orbiculare, spread by rain and wind",
                "treatments": "Fungicides like chlorothalonil, remove infected plants, crop rotation",
                "prevention": "Use resistant varieties, avoid overhead watering, space plants properly",
            },
            {
                "name": "Fusarium Wilt",
                "symptoms": [
                    "Wilting leaves",
                    "Yellowing foliage",
                    "Vascular discoloration",
                ],
                "causes": "Fungus Fusarium oxysporum, soil-borne",
                "treatments": "No cure; remove affected plants, soil fumigation",
                "prevention": "Resistant varieties, soil solarization, crop rotation",
            },
            # Add more diseases as needed...
        ]

        for data in initial_diseases:
            symptom_names = data.get("symptoms", [])
            symptoms_text = ", ".join(s.strip() for s in symptom_names if s.strip())

            disease = Disease(
                name=data["name"],
                symptoms=symptoms_text,
                causes=data["causes"],
                treatments=data["treatments"],
                prevention=data["prevention"],
            )

            db.session.add(disease)

        db.session.commit()

    @staticmethod
    def diagnose_disease(user_symptoms: List[str]):
        """Diagnose based on user symptoms."""
        diseases = Disease.query.all()
        results = []

        for disease in diseases:
            match_score = disease.calculate_match_score(user_symptoms)
            if match_score >= 30:
                results.append(
                    {
                        "id": disease.id,
                        "name": disease.name,
                        "match_score": match_score,
                        "symptoms": disease.symptoms_list,
                        "causes": disease.causes,
                        "treatments": disease.treatments,
                        "prevention": disease.prevention,
                    }
                )

        return sorted(results, key=lambda x: x["match_score"], reverse=True)

    @staticmethod
    def get_all_symptoms() -> List[str]:
        """Get all possible symptoms for the diagnosis form."""
        diseases = Disease.query.all()
        symptom_set: set[str] = set()

        for disease in diseases:
            for symptom in disease.symptoms_list:
                symptom_set.add(symptom)

        return sorted(symptom_set)

    @staticmethod
    def get_disease_by_id(disease_id: int) -> Optional[Disease]:
        return Disease.query.get(disease_id)

    @staticmethod
    def create_disease(data: dict) -> Disease:
        """
        Create a new disease using the data from the form.

        `data["symptoms"]` is expected to be a comma-separated string, which we
        store directly in the `symptoms` column. Helper methods on the model
        turn this into lists when needed.
        """
        disease = Disease(
            name=data["name"],
            symptoms=data.get("symptoms", ""),
            causes=data["causes"],
            treatments=data["treatments"],
            prevention=data["prevention"],
        )

        db.session.add(disease)
        db.session.commit()
        return disease

    @staticmethod
    def update_disease(disease: Disease, data: dict) -> Disease:
        """
        Update an existing disease with new data from the form.
        """
        disease.name = data["name"]
        disease.symptoms = data.get("symptoms", "")
        disease.causes = data["causes"]
        disease.treatments = data["treatments"]
        disease.prevention = data["prevention"]

        db.session.commit()
        return disease

    @staticmethod
    def delete_disease(disease: Disease) -> None:
        db.session.delete(disease)
        db.session.commit()