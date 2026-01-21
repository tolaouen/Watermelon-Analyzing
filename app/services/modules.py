from extensions import db 
from app.models.modules import Module
from typing import List, Optional

class ModuleService:

    @staticmethod
    def get_module_all() ->List[Module]: 
        return Module.query.order_by(Module.name).all()

    @staticmethod
    def get_module_by_id(module_id: int) ->Optional[Module]  :
        return Module.query.get(module_id)
    
    @staticmethod
    def create_module(data: dict) -> Module:
        new_module = Module(
            name=data["name"],
            description=data.get("description")
        )

        db.session.add(new_module)
        db.session.commit()
        return new_module
    
    @staticmethod
    def update_module(data: dict, module: Module) -> Module:
        module.name = data["name"]
        module.description = data.get("description") or ""

        db.session.commit()
        return module

    @staticmethod
    def delete_module(module: Module) -> None:
        db.session.delete(module)
        db.session.commit()

    @staticmethod
    def get_filtered(page: int, per_page: int, search: str):
        query = Module.query

        if search:
            query = query.filter(Module.name.ilike(f'%{search}%'))

        paginated_modules = query.order_by(Module.name).paginate(page=page, per_page=per_page, error_out=False)
        return paginated_modules