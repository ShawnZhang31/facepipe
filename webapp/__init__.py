import os
from flask import Flask
from config import config
from webapp.api.v1 import api_v1

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 注册路由
    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')