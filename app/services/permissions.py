from extensions import db
from app.models.associations import user_roles
from app.models.permissions import Permission
from app.models.modules import Module
from typing import List, Optional


class PermissionService:
    
    @staticmethod
    def get_permission_all() -> List[Permission]:
        return Permission.query.order_by(Permission.name).all()

    @staticmethod
    def get_permission_by_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)
    
    @staticmethod
    def create_permission(data: dict, module_id: int) -> Permission:
        new_permission = Permission(
            name = data["name"],
            code = data["code"],
            description = data.get("description") or ""
        )
        module = db.session.get(Module, module_id)
        if module:
            new_permission.modules.append(module)
        db.session.add(new_permission)
        db.session.commit()
        return new_permission

    @staticmethod
    def update_permission(permission: Permission, data: dict, module_id: int) -> Permission:
        permission.name = data["name"]
        permission.code = data["code"]
        permission.description = data.get("description") or ""
        # Clear existing modules and add new one
        permission.modules.clear()
        module = db.session.get(Module, module_id)
        if module:
            permission.modules.append(module)

        db.session.commit()
        return permission
    
    @staticmethod
    def delete_permission(permission: Permission) -> None:
        db.session.delete(permission)
        db.session.commit()
