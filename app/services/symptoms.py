from extensions import db
from app.models.symptom import Symptoms
from app.models.diseases import Disease
from typing import List, Optional   


class SymptomService:

    @staticmethod
    def get_all_symptoms() -> List[Symptoms]:
        return Symptoms.query.order_by(Symptoms.name).all()

    @staticmethod
    def get_symptom_by_id(symptom_id: int) -> Optional[Symptoms]:
        return Symptoms.query.get(symptom_id)
    
    @staticmethod
    def create_symptom(data: dict) -> Symptoms:
        new_symptom = Symptoms(
            name = data["name"],
            description = data.get("description")
        )
        db.session.add(new_symptom)
        db.session.commit()
        return new_symptom

    @staticmethod
    def update_symptom(symptom: Symptoms, data: dict) -> Symptoms:
        symptom.name = data["name"]
        symptom.description = data.get("description") or ""

        db.session.commit()
        return symptom

    @staticmethod
    def delete_symptom(symptom: Symptoms) -> None:
        db.session.delete(symptom)
        db.session.commit()

    @staticmethod
    def delete_by_id(symptom_id: int) -> None:
        db.session.delete(symptom_id)
        db.session.commit()

        
    @staticmethod
    def get_filtered(page: int, per_page: int, search: str):
        query = Symptoms.query

        if search:
            query = query.filter(Symptoms.name.ilike(f'%{search}%'))

        paginated_symptoms = query.order_by(Symptoms.name).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return paginated_symptoms
