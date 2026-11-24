import os 
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "notafacil.db")
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.inicializar_banco(app.config["DATABASE"])

    from . rotas import bp
    app.register_blueprint(bp)

    return app