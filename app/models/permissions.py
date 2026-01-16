from extensions import db
from datetime import datetime
from app.models.associations import role_permissions, module_permissions

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    roles = db.relationship('Role', secondary=role_permissions, back_populates="permissions")
    modules = db.relationship('Module', secondary=module_permissions, back_populates="permissions")


    def __repr__(self):
        return f'<Permission {self.name}: {self.description}>'