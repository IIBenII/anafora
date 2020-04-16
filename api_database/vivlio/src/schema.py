from marshmallow import ValidationError
from sqlalchemy import func

import vivlio.models as ms


def post_schema(request):
    content = request.get_json()
    print(content)

    try:
        validation = ms.SchemaSchema().load(content)
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    table = (
        ms.db.session.query(ms.Datasets.id, ms.Tables.id)
        .filter_by(
            project_name=content["project_name"], dataset_name=content["dataset_name"]
        )
        .outerjoin(ms.Tables, ms.Tables.dataset_id == ms.Datasets.id)
        .filter_by(table_name=content["table_name"])
        .first()
    )

    all_schema = []
    for field in content["schema"]:
        schema = ms.Schema.query.filter_by(
            table_id=table.id, field_name=field["field_name"]
        ).first()

        if schema:
            old_schema = ms.db.session.query(ms.Schema).filter(
                ms.Schema.table_id == table.id,
                ms.Schema.field_name == field["field_name"],
            )
            for key, value in content.items():
                setattr(old_schema, key, value)
        else:

            field["table_id"] = table.id
            all_schema.append(ms.Schema(**field))

    ms.db.session.add_all(all_schema)
    ms.db.session.commit()
    return "OK", 200


def get_schema(request):
    project_name = request.args.get("project_name", type=str)
    dataset_name = request.args.get("dataset_name", type=str)
    table_name = request.args.get("table_name", type=str)

    try:
        validation = ms.SchemaGetSchema().load(request.args.to_dict())
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    table = (
        ms.db.session.query(ms.Datasets.id, ms.Tables.id)
        .filter_by(project_name=project_name, dataset_name=dataset_name)
        .outerjoin(ms.Tables, ms.Tables.dataset_id == ms.Datasets.id)
        .filter_by(table_name=table_name)
        .first()
    )

    print(table)

    query_result = (
        ms.db.session.query(
            ms.Schema.field_name,
            ms.Schema.field_mode,
            ms.Schema.field_type,
            ms.Schema.field_description,
        )
        .filter_by(table_id=table.id)
        .order_by(ms.Schema.field_name.desc())
        .all()
    )

    list_tables = []
    for elt in query_result:
        list_tables.append(
            {
                "field_name": elt.field_name,
                "field_mode": elt.field_mode,
                "field_type": elt.field_type,
                "field_description": elt.field_description,
            }
        )
    return {"schema": list_tables}, 200
