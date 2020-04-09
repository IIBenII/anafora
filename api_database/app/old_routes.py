from flask import request
from flask import current_app as app
from marshmallow import ValidationError
from .models import db, ma, Datasets, Tables, SchemaDatasets


@app.route("/tables", methods=["POST"])
def insert_table():
    content = request.get_json()
    dataset = Datasets.query.filter_by(
        project_id=content["project_id"], dataset_id=content["dataset_id"]
    ).first()

    table = Tables.query.filter_by(
        table_id=content["table_id"], dataset_id=dataset.id
    ).first()

    if table:
        Tables.query.filter_by(
            table_id=content["table_id"], dataset_id=dataset.id
        ).update()
    else:
        table = Tables(table_id=content["table_id"], dataset_id=dataset.id)
        db.session.add(table)
    db.session.commit()
    return "Done"
