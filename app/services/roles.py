from extensions import db
from app.models.roles import Role
from app.models.permissions import Permission
from typing import List, Optional

class RolesService:

    @staticmethod
    def get_role_all() -> List[Role]:
        return Role.query.order_by(Role.id).all()

    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)
    
    @staticmethod
    def create_role(data: dict, permission_id: Optional[List[int]] = None) -> Role:
        role = Role(
            name = data["name"],
            description = data.get("description", "")
        )

        if permission_id:
            permission = db.session.scalars(
                db.select(Permission).filter(Permission.id.in_(permission_id))
            )
            role.permissions = list(permission)
        
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def update_role(role: Role, data: dict, permission_id: Optional[List[int]] = None) -> Role:
        role.name = data["name"]
        role.description = data.get("description", "")

        if permission_id:
            permission: List[Permission] = []
            if permission_id:
                permission = db.session.scalars(
                    db.select(Permission).filter(Permission.id.in_(permission_id))
                )
            role.permissions = list(permission)

        db.session.commit()
        return role



    @staticmethod
    def delete_role(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()