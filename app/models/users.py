from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from app.models.associations import user_roles
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    full_name = db.Column(db.String(120), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    roles = db.relationship('Role', secondary=user_roles, back_populates="users")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_code):
        """Check if user has specific permission through roles"""
        for role in self.roles:
            if any(permission.code == permission_code for permission in role.permissions):
                return True
        return False
    
    @property
    def is_admin(self):
        """Quick admin check"""
        return self.has_role('admin')

    @property
    def is_user(self):
        """Check if user has basic user role (no admin, no professional)"""
        return self.has_role('user') and not self.has_role('admin') and not self.has_role('professional')

    @property
    def is_professional(self):
        """Check if user has professional role"""
        return self.has_role('professional')

    def can_access(self, permission_code):
        """Check if user has specific permission by code"""
        return self.has_permission(permission_code)

    def require_permission(self, permission_code):
        """Raise exception if user doesn't have permission"""
        if not self.can_access(permission_code):
            from flask import abort
            abort(403, f"Permission denied: {permission_code}")

    def require_role(self, role_name):
        """Raise exception if user doesn't have role"""
        if not self.has_role(role_name):
            from flask import abort
            abort(403, f"Role required: {role_name}")
