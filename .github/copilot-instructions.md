# Watermelon System - AI Coding Agent Instructions

## Project Overview

A Flask-based web application for disease analysis with RBAC (Role-Based Access Control). Uses SQLAlchemy ORM, Flask-Login for authentication, and WTForms for form validation.

## Architecture Pattern: Service-Oriented Layering

The app follows a clean separation of concerns across four layers:

1. **Routes** (`app/routes/*.py`) - Handle HTTP requests/responses, form validation trigger
2. **Services** (`app/services/*.py`) - Business logic, database operations (UserService, RoleService, etc.)
3. **Models** (`app/models/*.py`) - SQLAlchemy ORM models with relationships
4. **Forms** (`app/forms/*.py`) - WTForms validation with custom validators (e.g., `strong_password`)

**Data Flow**: Request → Route (form validation) → Service (business logic) → Model (DB interaction) → Response

## Key Technical Decisions

### Authentication & Authorization

- **Flask-Login** for session management with `UserMixin`
- **Password Hashing**: Use `User.set_password(pwd)` and `check_password()` methods
- **Role-Based Access**: Users have many-to-many roles; roles have many-to-many permissions
- **Permission Check**: Use `User.has_permission(name)` or `User.is_admin` for checks

### Database Relationships

- **Many-to-Many**: User↔Role (`user_roles` table), Role↔Permission (`role_permissions`), Module↔Permission (`module_permissions`)
- All association tables include `created_at` timestamp
- Models use `db.relationship()` with `back_populates` for bidirectional access

### Form Validation

- Custom validators as functions (e.g., `strong_password()`) raise `ValidationError`
- Always pass `original_user` when initializing update forms to avoid self-validation conflicts
- Forms handle CSRF protection via `FlaskForm` (csrf token auto-included)

## Developer Workflows

### Running the Application

```bash
source .venv/bin/activate
pip install -r requirements.txt
python run.py  # Starts on port 5002 with debug=True
```

### Database Setup

- Models auto-create on app startup via `db.create_all()` in `create_app()`
- Environment: Configure `DATABASE_URL` and `SECRET_KEY` in `.env`
- Migrations: Flask-Migrate available (use `flask db` commands)

### Adding a New Resource

1. Create model in `app/models/resource.py` with relationships
2. Create form in `app/forms/resource.py` with validators
3. Create service in `app/services/resource.py` with CRUD methods
4. Create routes in `app/routes/resource.py` with `@login_required`
5. Register blueprint in `create_app()` → `app.register_blueprint(resource_router)`
6. Create templates in `app/templates/resource/*.html`

## Code Patterns & Conventions

### Service Methods

- Static methods for stateless operations
- Return type hints: `List[Model]`, `Optional[Model]`, `Model`
- Always `db.session.commit()` and `db.session.refresh()` after CREATE/UPDATE
- Example: `UserService.create_user(role_id, data, password) → User`

### Route Handlers

- Name blueprints with resource name: `user_router = Blueprint("User", __name__, url_prefix="/user")`
- Use Flask's `flash()` for user feedback, redirect to `detail` after create/update
- Abort with 404 for missing resources: `abort(404, "Resource Not Found")`
- Common routes: `/` (list), `/<id>` (detail), `/create` (create), `/<id>/edit` (update), `/<id>/delete` (delete)

### Models

- Include `created_at`, `updated_at` timestamps on all models
- Use `__tablename__` explicitly
- Implement `__repr__` for debugging
- Add helper methods: `has_role()`, `has_permission()`, `is_admin` (property)

## Important Files & Patterns

- **[extensions.py](../../extensions.py)** - Centralized extensions initialization (`db`, `csrf`, `migrate`)
- **[config.py](../../config.py)** - Config class loads from `.env` via `python-dotenv`
- **[app/main.py](../../app/main.py)** - `create_app()` factory; blueprint registration happens here
- **[app/models/associations.py](../../app/models/associations.py)** - All many-to-many tables defined here
- **[app/models/users.py](../../app/models/users.py)** - Reference implementation with role/permission helpers
- **[app/routes/users.py](../../app/routes/users.py)** - Reference route pattern with CRUD ops
- **[app/forms/users.py](../../app/forms/users.py)** - Reference form with custom validators

## Critical Notes

- **No explicit ORM queries in routes** - all DB access through services
- **Form validation errors** prevent service calls - check `form.validate_on_submit()` first
- **Session management** - always commit after modifications; use `db.session.get()` for role/permission lookups
- **Blueprint naming** - must match URL generation in routes (e.g., `url_for("User.detail")`)
- **CSRF protection** - enabled globally; forms must use `{{ form.csrf_token() }}`

## External Dependencies

- Flask 3.x, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- SQLAlchemy 2.x with typed relationships
- WTForms with email-validator, pydantic for settings
- Werkzeug for password hashing
- Oracle DB support (psycopg2-binary, oracledb drivers included)
