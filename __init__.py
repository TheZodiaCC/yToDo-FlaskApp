from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

#Global vars
database = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    database.init_app(app)

    with app.app_context():
        import routes

        app.register_blueprint(routes.home_)
        app.register_blueprint(routes.profile_)
        app.register_blueprint(routes.login_)
        app.register_blueprint(routes.register_)
        app.register_blueprint(routes.register_reg_)
        app.register_blueprint(routes.logout_)
        app.register_blueprint(routes.forget_)
        app.register_blueprint(routes.forget_get_)
        app.register_blueprint(routes.settings_)
        app.register_blueprint(routes.change_password_)
        app.register_blueprint(routes.add_thing_)
        app.register_blueprint(routes.delete_thing_)

        return app
