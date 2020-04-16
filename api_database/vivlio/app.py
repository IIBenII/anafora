import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()

    click.echo("Initialized the database.")


@click.command("drop-db")
@with_appcontext
def drop_db_command():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()

    click.echo("Initialized the database.")


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("vivlio.config.Config")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
db.init_app(app)
ma.init_app(app)
CORS(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.cli.add_command(init_db_command)
app.cli.add_command(drop_db_command)

with app.app_context():
    import vivlio.views

    app


if __name__ == "__main__":
    app.run()
