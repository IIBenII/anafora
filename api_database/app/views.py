from flask import request
from flask import current_app as app
from marshmallow import ValidationError
from sqlalchemy import func


from .models import db, ma, Datasets, Tables, SchemaDatasets, SchemaTables


@app.route("/health")
def health():
    return "OK"


def get_dataset():
    query_result = (
        db.session.query(
            Datasets.dataset_name,
            Datasets.description,
            Datasets.project_name,
            func.count(Tables.table_name).label("nb_table"),
        )
        .outerjoin(Tables, Tables.dataset_id == Datasets.id)
        .group_by(Datasets.dataset_name)
        .order_by(Datasets.dataset_name)
        .all()
    )
    list_dataset = []
    for elt in query_result:
        list_dataset.append(
            {
                "project_name": elt.project_name,
                "dataset_name": elt.dataset_name,
                "description": elt.description,
                "nb_table": elt.nb_table,
            }
        )
    return {"datasets": list_dataset}


@app.route("/datasets", methods=["POST", "GET"])
def insert_dataset():
    if request.method == "GET":
        return get_dataset()

    content = request.get_json()
    print(content)

    try:
        validation = SchemaDatasets().load(content)
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = Datasets.query.filter_by(
        project_name=content["project_name"], dataset_name=content["dataset_name"]
    ).first()

    if dataset:
        old_dataset = db.session.query(Datasets).filter(
            Datasets.dataset_name == dataset.dataset_name
        )
        for key, value in content.items():
            setattr(old_dataset, key, value)
    else:
        dataset = Datasets(**content)
        db.session.add(dataset)

    db.session.commit()
    return "OK", 200


@app.route("/tables", methods=["GET"])
def get_tables():

    project_name = request.args.get("project_name", type=str)
    dataset_name = request.args.get("dataset_name", type=str)
    compact = request.args.get("compact", type=str)

    dataset = Datasets.query.filter_by(
        project_name=project_name, dataset_name=dataset_name
    ).first()

    if compact == "true":
        query_result = (
            db.session.query(
                Tables.clean_table_name.label("table_name"),
                Tables.description,
                func.count(Tables.table_name).label("nb_table"),
            )
            .filter_by(dataset_id=dataset.id)
            .order_by(Tables.table_name)
            .group_by(Tables.clean_table_name)
            .distinct(Tables.clean_table_name)
            .all()
        )
    else:
        query_result = (
            db.session.query(
                Tables.table_name,
                Tables.description,
                func.count(Tables.table_name).label("nb_table"),
            )
            .filter_by(dataset_id=dataset.id)
            .order_by(Tables.table_name)
            .group_by(Tables.clean_table_name)
            .all()
        )

    list_tables = []
    for elt in query_result:
        list_tables.append(
            {
                "project_name": project_name,
                "dataset_name": dataset_name,
                "table_name": elt.table_name,
                "description": elt.description,
                "nb_table": elt.nb_table,
            }
        )
    return {"tables": list_tables}


@app.route("/table_infos", methods=["GET"])
def get_table_infos():

    project_name = request.args.get("project_name", type=str)
    dataset_name = request.args.get("dataset_name", type=str)
    clean_table_name = request.args.get("clean_table_name", type=str)

    dataset = Datasets.query.filter_by(
        project_name=project_name, dataset_name=dataset_name
    ).first()

    query_result = (
        db.session.query(
            Tables.table_name,
            Tables.clean_table_name,
            Tables.description,
            Tables.num_rows,
            Tables.num_bytes,
        )
        .filter_by(dataset_id=dataset.id, clean_table_name=clean_table_name)
        .order_by(Tables.table_name.desc())
        .all()
    )

    list_tables = []
    for elt in query_result:
        list_tables.append(
            {
                "table_name": elt.table_name,
                "clean_table_name": elt.clean_table_name,
                "description": elt.description,
                "num_rows": elt.num_rows,
                "table_size": elt.num_bytes,
            }
        )
    return {"table_infos": list_tables}


@app.route("/tables", methods=["POST"])
def insert_table():
    content = request.get_json()
    print(content)

    try:
        validation = SchemaTables().load(content)
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = Datasets.query.filter_by(
        project_name=content["project_name"], dataset_name=content["dataset_name"]
    ).first()

    table = Tables.query.filter_by(
        table_name=content["table_name"], dataset_id=dataset.id
    ).first()

    if table:
        old_table = db.session.query(Tables).filter(Tables.dataset_id == dataset.id)
        for key, value in content.items():
            setattr(old_table, key, value)
    else:
        content.pop("project_name")
        content.pop("dataset_name")
        content["dataset_id"] = dataset.id
        table = Tables(**content)
        db.session.add(table)

    db.session.commit()
    return "Done"
