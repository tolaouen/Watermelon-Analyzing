from app.models.rules import Rules
from extensions import db
from typing import List, Optional


class RuleService:

    @staticmethod
    def get_rules_all() -> List[Rules]:
        return Rules.query.order_by(Rules.id).all()
    
    @staticmethod
    def get_rules_by_id(rule_id: int) -> Optional[Rules]:
        return Rules.query.get(rule_id)

    @staticmethod
    def create_rules(data: dict) -> Rules:

        new_rules = Rules(
            name = data["name"],
            condition = data.get("condition", False),
            answer = data.get("answer") or ""
        )

        db.session.add(new_rules)
        db.session.commit()
        return new_rules
    
    @staticmethod
    def update_rules(rule: Rules, data: dict) -> Rules:
        rule.name = data["name"]
        condition = data.get("condition")
        if condition is not None:
            rule.condition = condition
        else:
            rule.condition = False
            
        rule.answer = data.get("answer") or " "

        db.session.commit()
        return rule

    @staticmethod
    def delete_by_id(rule_id: int) -> None:
        db.session.delete(rule_id)
        db.session.commit()

    @staticmethod
    def delete_all(rule: Rules) -> None:
        db.session.delete(rule)
        db.session.commit()
