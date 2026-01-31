from extensions import db
from app.models.diseases import Disease
from typing import List, Optional
import json

class DiseaseService:

    @staticmethod
    def seed_initial_diseases():
        """Seed initial knowledge base if empty"""
        if Disease.query.count() == 0:
            initial_diseases = [
                {
                    'name': 'Anthracnose',
                    'symptoms': json.dumps([
                        'Brown spots on leaves', 'Angular spots on fruit', 'Stem lesions',
                        'Sunken lesions on fruit', 'Pink spore masses'
                    ]),
                    'causes': 'Fungus Colletotrichum orbiculare, spread by rain and wind',
                    'treatments': 'Fungicides like chlorothalonil, remove infected plants, crop rotation',
                    'prevention': 'Use resistant varieties, avoid overhead watering, space plants properly'
                },
                {
                    'name': 'Fusarium Wilt',
                    'symptoms': json.dumps([
                        'Wilting leaves', 'Yellowing foliage', 'Vascular discoloration',
                        'Stunted growth', 'Root rot'
                    ]),
                    'causes': 'Fungus Fusarium oxysporum, soil-borne',
                    'treatments': 'No cure; remove affected plants, soil fumigation',
                    'prevention': 'Resistant varieties, soil solarization, crop rotation'
                },
                # Add more diseases as needed...
            ]
            
            for data in initial_diseases:
                disease = Disease(**data)
                db.session.add(disease)
            db.session.commit()

    @staticmethod
    def diagnose_disease(user_symptoms):
        """Diagnose based on user symptoms"""
        DiseaseService.seed_initial_diseases()
        diseases = Disease.query.all()
        results = []
        
        for disease in diseases:
            match_score = disease.calculate_match_score(user_symptoms)
            if match_score >= 30:  
                results.append({
                    'id': disease.id,
                    'name': disease.name,
                    'match_score': match_score,
                    'symptoms': disease.symptoms_list,
                    'causes': disease.causes,
                    'treatments': disease.treatments,
                    'prevention': disease.prevention
                })
        
        return sorted(results, key=lambda x: x['match_score'], reverse=True)
    
    @staticmethod
    def get_all_symptoms() -> List[str]:
        """Get all possible symptoms for form"""
        DiseaseService.seed_initial_diseases()
        diseases = Disease.query.all()
        all_symptoms = set()

        for disease in diseases:
            all_symptoms.update(disease.symptoms_list)

        return sorted(list(all_symptoms))
    
    @staticmethod
    def get_disease_by_id(disease_id: int) -> Optional[Disease]:
        return Disease.query.get(disease_id)

    @staticmethod
    def create_disease(data: dict) -> Disease:
        disease = Disease(
            name=data["name"],
            symptoms=json.dumps(data["symptoms"].split(',')),
            causes=data["causes"],
            treatments=data["treatments"],
            prevention=data["prevention"]
        )
        db.session.add(disease)
        db.session.commit()
        return disease

    @staticmethod
    def update_disease(disease: Disease, data: dict) -> Disease:
        disease.name = data["name"]
        disease.symptoms = json.dumps(data["symptoms"].split(','))
        disease.causes = data["causes"]
        disease.treatments = data["treatments"]
        disease.prevention = data["prevention"]
        db.session.commit()
        return disease

    @staticmethod
    def delete_disease(disease: Disease) -> None:
        db.session.delete(disease)
        db.session.commit()

    

