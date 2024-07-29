from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_initialized = False

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)

    @app.before_request
    def initialize_database():
        global database_initialized
        if not database_initialized:
            print("Initializing database...")
            db.create_all()
            database_initialized = True

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
