from extensions import db
from app.models.permissions import Permission
from app.models.roles import Role
from app.models.modules import Module

def seed_permissions():
    """Create basic permissions if they don't exist"""

    # Basic permissions
    permissions_data = [
        {
            'name': 'Read Users',
            'code': 'users:read',
            'description': 'Can view user information'
        },
        {
            'name': 'Create Users',
            'code': 'users:create',
            'description': 'Can create new users'
        },
        {
            'name': 'Update Users',
            'code': 'users:update',
            'description': 'Can update user information'
        },
        {
            'name': 'Delete Users',
            'code': 'users:delete',
            'description': 'Can delete users'
        },
        {
            'name': 'Read Roles',
            'code': 'roles:read',
            'description': 'Can view roles'
        },
        {
            'name': 'Manage Roles',
            'code': 'roles:manage',
            'description': 'Can create, update, and delete roles'
        },
        {
            'name': 'Read Permissions',
            'code': 'permissions:read',
            'description': 'Can view permissions'
        },
        {
            'name': 'Manage Permissions',
            'code': 'permissions:manage',
            'description': 'Can create, update, and delete permissions'
        },
        {
            'name': 'Read Diseases',
            'code': 'diseases:read',
            'description': 'Can view diseases'
        },
        {
            'name': 'Manage Diseases',
            'code': 'diseases:manage',
            'description': 'Can create, update, and delete diseases'
        },
        {
            'name': 'Read Modules',
            'code': 'modules:read',
            'description': 'Can view modules'
        },
        {
            'name': 'Manage Modules',
            'code': 'modules:manage',
            'description': 'Can create, update, and delete modules'
        },
        {
            'name': 'Admin Access',
            'code': 'admin:full',
            'description': 'Full administrative access'
        }
    ]

    for perm_data in permissions_data:
        existing = Permission.query.filter_by(code=perm_data['code']).first()
        if not existing:
            permission = Permission(
                name=perm_data['name'],
                code=perm_data['code'],
                description=perm_data['description']
            )
            db.session.add(permission)
            print(f"Created permission: {perm_data['name']}")

    db.session.commit()

def seed_roles():
    """Create basic roles if they don't exist"""

    # User role - basic access
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', description='Basic user access')
        db.session.add(user_role)
        print("Created role: user")

    # Admin role - full access
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator with full access')
        db.session.add(admin_role)
        print("Created role: admin")

    db.session.commit()

    # Assign permissions to roles
    assign_permissions_to_roles()

def assign_permissions_to_roles():
    """Assign appropriate permissions to user and admin roles"""

    user_role = Role.query.filter_by(name='user').first()
    admin_role = Role.query.filter_by(name='admin').first()

    if user_role:
        # User permissions - limited access
        user_permissions = [
            'users:read',
            'users:create',
            'diseases:read',
            'modules:read',
            'modules:manage',
            'roles:read',
            'permissions:read'
        ]

        for code in user_permissions:
            permission = Permission.query.filter_by(code=code).first()
            if permission and permission not in user_role.permissions:
                user_role.permissions.append(permission)
                print(f"Assigned {code} to user role")

    if admin_role:
        # Admin permissions - all permissions
        all_permissions = Permission.query.all()
        for permission in all_permissions:
            if permission not in admin_role.permissions:
                admin_role.permissions.append(permission)
                print(f"Assigned {permission.code} to admin role")

    db.session.commit()

def create_default_admin_user():
    """Create a default admin user if it doesn't exist"""
    from app.models.users import User
    from app.models.roles import Role

    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', full_name='Administrator')
        admin_user.set_password('admin')
        db.session.add(admin_user)
        print("Created default admin user")

    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role and admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
        print("Assigned admin role to admin user")

    db.session.commit()

def assign_default_roles_to_existing_users():
    """Assign default 'user' role to users who don't have any roles"""
    from app.models.users import User
    from app.models.roles import Role

    default_role = Role.query.filter_by(name='user').first()
    if not default_role:
        print("Warning: Default 'user' role not found, skipping user role assignment")
        return

    users_without_roles = User.query.filter(~User.roles.any()).all()
    for user in users_without_roles:
        user.roles = [default_role]
        print(f"Assigned default 'user' role to {user.username}")

    if users_without_roles:
        db.session.commit()
        print(f"Assigned default roles to {len(users_without_roles)} users")
    else:
        print("All users already have roles assigned")

def seed_database():
    """Run all seed functions"""
    print("Starting database seeding...")

    try:
        seed_permissions()
        seed_roles()
        assign_default_roles_to_existing_users()
        create_default_admin_user()
        print("Database seeding completed successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error during seeding: {e}")
        raise

if __name__ == "__main__":
    from app.main import create_app

    app = create_app()
    with app.app_context():
        seed_database()