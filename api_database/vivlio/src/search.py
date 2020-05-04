from marshmallow import ValidationError
from sqlalchemy import func

import vivlio.models as ms


def search(request):
    filter = f"%{request.args.get('filter', type=str)}%"
    print(filter)

    if filter == "%%":
        return (
            {
                "search": [
                    {
                        "project_name": "",
                        "dataset_name": "",
                        "table_name": "",
                        "description": "",
                    }
                ]
            },
            200,
        )

    query_result = (
        ms.db.session.query(
            ms.Datasets.dataset_name, ms.Datasets.description, ms.Datasets.project_name,
        )
        .filter(ms.Datasets.dataset_name.like(filter.replace(" ", "_")))
        .order_by(ms.Datasets.dataset_name)
        .all()
    )

    list_datasets = []
    for elt in query_result:
        list_datasets.append(
            {
                "project_name": elt.project_name,
                "dataset_name": elt.dataset_name,
                "description": elt.description,
            }
        )

    query_result = (
        ms.db.session.query(
            ms.Datasets.project_name,
            ms.Datasets.dataset_name,
            ms.Tables.table_name,
            ms.Tables.description,
        )
        .outerjoin(ms.Tables, ms.Tables.dataset_id == ms.Datasets.id)
        .filter(ms.Tables.table_name.like(filter.replace(" ", "_")))
        .order_by(ms.Datasets.dataset_name)
        .all()
    )

    list_tables = []
    for elt in query_result:
        list_tables.append(
            {
                "project_name": elt.project_name,
                "dataset_name": elt.dataset_name,
                "table_name": elt.table_name,
                "description": elt.description,
            }
        )

    query_result = (
        ms.db.session.query(
            ms.Datasets.project_name,
            ms.Datasets.dataset_name,
            ms.Tables.clean_table_name,
            ms.Schema.field_name,
            ms.Schema.field_mode,
            ms.Schema.field_type,
            ms.Schema.field_description,
        )
        .outerjoin(ms.Tables, ms.Tables.id == ms.Schema.table_id)
        .outerjoin(ms.Datasets, ms.Tables.dataset_id == ms.Datasets.id)
        .filter(ms.Schema.field_name.like(filter.replace(" ", "_")))
        .group_by(ms.Tables.clean_table_name)
        .order_by(ms.Datasets.dataset_name.desc())
        .all()
    )

    list_fields = []
    for elt in query_result:
        list_fields.append(
            {
                "project_name": elt.project_name,
                "dataset_name": elt.dataset_name,
                "table_name": elt.clean_table_name,
                "field_name": elt.field_name,
                "field_mode": elt.field_mode,
                "field_type": elt.field_type,
                "field_description": elt.field_description,
            }
        )
    return (
        {"datasets": list_datasets, "tables": list_tables, "fields": list_fields},
        200,
    )
