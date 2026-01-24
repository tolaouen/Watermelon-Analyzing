from app.services.modules import ModuleService
from app.forms.modules import ModuleCreateForm, UpdateModuleForm, DeleteModuleForm
from flask import Blueprint, flash, redirect, render_template, abort, url_for
from flask_login import login_required
from app.decorators import permission_required

module_route = Blueprint("module", __name__, url_prefix="/module")

@module_route.route("/")
@login_required
def index():
    modules = ModuleService.get_module_all()
    return render_template("modules/index.html", modules=modules)

@module_route.route("/<int:module_id>")
@login_required
def detail(module_id: int):
    module = ModuleService.get_module_by_id(module_id)
    if module is None:
        abort(404, "Module Not Found")
    
    return render_template("modules/detail.html", module=module)


@module_route.route("/create", methods=["GET", "POST"])
@login_required
@permission_required('modules:manage')
def create():
    form = ModuleCreateForm()

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data
        }
        module = ModuleService.create_module(data)
        flash(f"Module {module.name} was created successfully", "success")
        return redirect(url_for('module.detail', module_id=module.id))
    return render_template("modules/create.html", form=form)

@module_route.route("/<int:module_id>/edit", methods=["GET", "POST"])
@login_required
@permission_required('modules:manage')
def edit(module_id: int):
    module = ModuleService.get_module_by_id(module_id)

    if module is None:
        abort(404, "Module Not Found")
    
    form = UpdateModuleForm(original_module=module, obj=module)

    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "description": form.description.data 
        }
        ModuleService.update_module(data, module)
        flash(f"Module {module.name} was updated successfully", "success")
        return redirect(url_for('module.detail', module_id=module.id))
    return render_template("modules/edit.html", form=form)

@module_route.route("/<int:module_id>/delete", methods=["GET"])
@login_required
@permission_required('modules:manage')
def delete_confirm(module_id: int):
    module = ModuleService.get_module_by_id(module_id)

    if module is None:
        abort(404, "Module Not Found")
    
    form = DeleteModuleForm()
    return render_template("modules/delete.html", form=form, module=module)

@module_route.route("/<int:module_id>/delete", methods=["POST"])
@login_required
@permission_required('modules:manage')
def delete(module_id: int):
    module = ModuleService.get_module_by_id(module_id)

    if module is None:
        abort(404, "Module Not Found")

    ModuleService.delete_module(module)
    flash(f"Module {module.name} was deleted successfully", "success")
    return redirect(url_for('module.index'))
