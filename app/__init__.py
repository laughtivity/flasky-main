from flask import Flask
# import SQLALchemy
from flask_sqlalchemy import SQLAlchemy
# import Migrate
from flask_migrate import Migrate
# import libraries for grabbing environment variables
from dotenv import load_dotenv
# used to read environment variables
import os

#gives us access to database operations
db = SQLAlchemy()
migrate = Migrate()
# load the values from our .env file so the os module to be able to see them
load_dotenv()

def create_app(test_config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # set up the database regardless of environment
    if not test_config:
        # development environment configuration
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("RENDER_DATABASE_URI")

    else:
        # testing environment configuration
        # if there is a test_config passed in,
        # this means 
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
        
    #connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    # import routes 
    from .routes import crystal_bp, healer_bp

    #register the blueprint
    app.register_blueprint(crystal_bp)
    app.register_blueprint(healer_bp)
    
    from app.models.crystal import Crystal
    from app.models.healer import Healer
    
    return app
