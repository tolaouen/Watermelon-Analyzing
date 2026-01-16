from extensions import db
from app.models.diseases import Disease
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
            if match_score >= 30:  # Threshold for match
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
    def get_all_symptoms():
        """Get all possible symptoms for form"""
        DiseaseService.seed_initial_diseases()
        diseases = Disease.query.all()
        all_symptoms = set()

        for disease in diseases:
            all_symptoms.update(disease.symptoms_list)
        
        return sorted(list(all_symptoms))