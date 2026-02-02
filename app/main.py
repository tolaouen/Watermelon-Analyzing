from extensions import db, csrf
from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager
from config import Config

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.users import User
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    from app.routes.users import user_router
    from app.routes.roles import role_router
    from app.routes.permissions import permission_router
    from app.routes.diseases import disease_route
    from app.routes.modules import module_route
    from app.routes.auth import auth_route

    app.register_blueprint(user_router)
    app.register_blueprint(role_router)
    app.register_blueprint(permission_router)
    app.register_blueprint(disease_route)
    app.register_blueprint(module_route)
    app.register_blueprint(auth_route)

    @app.route("/")
    def home():
        # Redirect the root URL to the disease search page
        return redirect(url_for("disease.index"))

    with app.app_context():

        # Import all models so SQLAlchemy knows about them
        from app.models.users import User  
        from app.models.roles import Role  
        from app.models.permissions import Permission 
        from app.models.modules import Module  
        from app.models.diseases import Disease 

        db.create_all()

        # Seed initial permissions, roles, and other data
        from app.seed import seed_database
        seed_database()

    return app
