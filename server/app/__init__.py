
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

def init_app(logger, secret_key, jwt_token_expiration, jwt_rtoken_expiration):

    app = Flask(__name__, 
        template_folder = 'assets/templates', 
        static_url_path='',
        static_folder='assets/static')
    app.logger = logger
    
    app.config["SECRET_KEY"] = secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=jwt_token_expiration)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=jwt_rtoken_expiration)

    jwt = JWTManager(app)
    
    with app.app_context():
        
        from app.blueprints.backend import comm_blueprint
        from app.blueprints.backend import manage_blueprint
        from app.blueprints.frontend import dash_blueprint
        
        app.register_blueprint(comm_blueprint, url_prefix='/api/v1.0')
        app.register_blueprint(manage_blueprint, url_prefix='/api/v1.0/manage')
        app.register_blueprint(dash_blueprint, url_prefix='/panel')
    
    return app