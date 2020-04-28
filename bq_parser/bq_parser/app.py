import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS

# from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow
from apscheduler.schedulers.background import BackgroundScheduler


# db = SQLAlchemy()
from bq_parser.database import db
from bq_parser.models import Jobs
from bq_parser.redis import conn
from rq.job import Job


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


def test_job():
    with app.app_context():
        print("Subroutin update status")

        query_result = (
            db.session.query(Jobs.job_id,)
            .filter(~Jobs.job_status.in_(["finished", "delete"]))
            .all()
        )
        for job_id in query_result:
            new_job_status = Job.fetch(job_id[0], connection=conn).get_status()
            old_job = db.session.query(Jobs).filter(Jobs.job_id == job_id[0]).first()
            old_job.job_status = new_job_status
            db.session.commit()


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("bq_parser.config.Config")
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
    import bq_parser.views

    app

if __name__ == "__main__":

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(test_job, "interval", seconds=10)
    scheduler.start()

    app.run(port=5001)
