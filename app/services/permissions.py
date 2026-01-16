from extensions import db
from app.models.associations import user_roles
from app.models.permissions import Permission
from typing import List, Optional


class PermissionService:
    
    @staticmethod
    def get_permission_all() -> List[Permission]:
        return Permission.query.order_by(Permission.name).all()

    @staticmethod
    def get_permission_by_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)
    
    @staticmethod
    def create_permission(data: dict) -> Permission:
        new_permission = Permission(
            name = data["name"],
            description = data.get("description") or ""
        )
        db.session.add(new_permission)
        db.session.commit()
        return new_permission

    @staticmethod
    def update_permission(data: dict, permission: Permission) -> Permission:
        permission.name = data["name"]
        permission.description = data.get("description") or ""

        db.session.commit()
        return permission
    
    @staticmethod
    def delete_permission(permission: Permission) -> None:
        db.session.delete(permission)
        db.session.commit()
