from marshmallow import ValidationError
from sqlalchemy import func

import app.models as ms


def get_tables(request):
    project_name = request.args.get("project_name", type=str)
    dataset_name = request.args.get("dataset_name", type=str)
    compact = request.args.get("compact", type=str)

    try:
        validation = ms.SchemaGetTables().load(request.args.to_dict())
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = ms.Datasets.query.filter_by(
        project_name=project_name, dataset_name=dataset_name
    ).first()

    if compact == "true":
        query_result = (
            ms.db.session.query(
                ms.Tables.clean_table_name.label("table_name"),
                ms.Tables.description,
                func.count(ms.Tables.table_name).label("nb_table"),
            )
            .filter_by(dataset_id=dataset.id)
            .order_by(ms.Tables.table_name)
            .group_by(ms.Tables.clean_table_name)
            .distinct(ms.Tables.clean_table_name)
            .all()
        )
    else:
        query_result = (
            ms.db.session.query(
                ms.Tables.table_name,
                ms.Tables.description,
                func.count(ms.Tables.table_name).label("nb_table"),
            )
            .filter_by(dataset_id=dataset.id)
            .order_by(ms.Tables.table_name)
            .group_by(ms.Tables.clean_table_name)
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
    return {"tables": list_tables}, 200


def post_tables(request):
    content = request.get_json()
    print(content)

    try:
        validation = ms.SchemaTables().load(content)
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = ms.Datasets.query.filter_by(
        project_name=content["project_name"], dataset_name=content["dataset_name"]
    ).first()

    table = ms.Tables.query.filter_by(
        table_name=content["table_name"], dataset_id=dataset.id
    ).first()

    if table:
        old_table = ms.db.session.query(ms.Tables).filter(
            ms.Tables.dataset_id == dataset.id
        )
        for key, value in content.items():
            setattr(old_table, key, value)
    else:
        content.pop("project_name")
        content.pop("dataset_name")
        content["dataset_id"] = dataset.id
        table = ms.Tables(**content)
        ms.db.session.add(table)

    ms.db.session.commit()
    return "OK", 200
