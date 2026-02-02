from app.forms.users import UserCreateForm, UserUpdateForm, UserDeleteForm
from app.forms.roles import CreateRoleForm, UpdateRoleForm, DeleteRoleForm
from app.forms.permissions import CreatePermissionForm, UpdatePermissionForm, DeletePermissionForm
from app.forms.diseases import CreateDiseaseForm, UpdateDiseaseForm, DeleteDiseaseForm
from app.forms.modules import ModuleCreateForm, UpdateModuleForm, DeleteModuleForm

__all__ = [ 
    'UserCreateForm', 'UserUpdateForm', 'UserDeleteForm',
    'CreateRoleForm', 'UpdateRoleForm', 'DeleteRoleForm',
    'CreatePermissionForm', 'UpdatePermissionForm', 'DeletePermissionForm',
    'CreateDiseaseForm', 'UpdateDiseaseForm', 'DeleteDiseaseForm',
    'ModuleCreateForm', 'UpdateModuleForm', 'DeleteModuleForm',
]