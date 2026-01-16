from extensions import db
from app.models.associations import role_permissions, user_roles
from datetime import datetime 

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    permissions = db.relationship('Permission', secondary=role_permissions, back_populates="roles")
    users = db.relationship('User', secondary=user_roles, back_populates="roles")
    
    def __repr__(self):
        return f'<Role {self.name}: {self.description}>'
    
    def add_permission(self, permission):
        """Add permission to role"""
        if permission not in self.permissions:
            self.permissions.append(permission)