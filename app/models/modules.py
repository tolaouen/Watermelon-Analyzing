from extensions import db
from datetime import datetime
from app.models.associations import module_permissions

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    permissions = db.relationship('Permission', secondary=module_permissions, back_populates="modules")

    def __repr__(self):
        return f'<Module {self.name}>'