from extensions import db
from app.models.users import User
from app.models.roles import Role
from typing import List, Optional

class UserService:

    @staticmethod
    def get_user_all() -> List[User]:
        return User.query.order_by(User.id).all()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
    @staticmethod
    def create_user(data: dict, password: str, role_id: Optional[int] = None) -> User:
        user = User(
            username = data["username"],
            email = data["email"],
            full_name = data["full_name"],
            is_active = data.get("is_active", True)
        )

        user.set_password(password)

        if role_id:
            role = Role.query.get(role_id)
            if role:
                user.roles = [role]
        else:
            # Assign default 'user' role if no role specified
            default_role = Role.query.filter_by(name='user').first()
            if default_role:
                user.roles = [default_role]

        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user: User, data: dict, password: Optional[str] = None, role_id: Optional[int] = None) -> User:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True)

        if password:
            user.set_password(password)

        if role_id is not None:
            role = Role.query.get(role_id)
            if role:
                user.roles = [role]
            else:
                # If role_id is provided but invalid, assign default user role
                default_role = Role.query.filter_by(name='user').first()
                if default_role:
                    user.roles = [default_role]

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        db.session.delete(user)
        db.session.commit()

