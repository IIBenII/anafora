from marshmallow import ValidationError
from sqlalchemy import func

import app.models as ms


def get_table_infos(request):
    project_name = request.args.get("project_name", type=str)
    dataset_name = request.args.get("dataset_name", type=str)
    clean_table_name = request.args.get("clean_table_name", type=str)

    try:
        validation = ms.SchemaGetTablesInfos().load(request.args.to_dict())
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = ms.Datasets.query.filter_by(
        project_name=project_name, dataset_name=dataset_name
    ).first()

    query_result = (
        ms.db.session.query(
            ms.Tables.table_name,
            ms.Tables.clean_table_name,
            ms.Tables.description,
            ms.Tables.num_rows,
            ms.Tables.num_bytes,
        )
        .filter_by(dataset_id=dataset.id, clean_table_name=clean_table_name)
        .order_by(ms.Tables.table_name.desc())
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
    return {"table_infos": list_tables}, 200
