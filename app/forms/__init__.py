from app.forms.users import CreateUserForm, UpdateUserForm, DeleteUserForm
from app.forms.roles import CreateRoleForm, UpdateRoleForm, DeleteRoleForm
from app.forms.permissions import CreatePermissionForm, UpdatePermissionForm, DeletePermissionForm
from app.forms.diseases import CreateDiseaseForm, UpdateDiseaseForm, DeleteDiseaseForm
from app.forms.modules import CreateModuleForm, UpdateModuleForm, DeleteModuleForm

__all__ = [ 
    'CreateUserForm', 'UpdateUserForm', 'DeleteUserForm',
    'CreateRoleForm', 'UpdateRoleForm', 'DeleteRoleForm',
    'CreatePermissionForm', 'UpdatePermissionForm', 'DeletePermissionForm',
    'CreateDiseaseForm', 'UpdateDiseaseForm', 'DeleteDiseaseForm',
    'CreateModuleForm', 'UpdateModuleForm', 'DeleteModuleForm'
]