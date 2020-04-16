from marshmallow import ValidationError
from sqlalchemy import func

import app.models as ms


def get_dataset():
    query_result = (
        ms.db.session.query(
            ms.Datasets.dataset_name,
            ms.Datasets.description,
            ms.Datasets.project_name,
            func.count(ms.Tables.table_name).label("nb_table"),
        )
        .outerjoin(ms.Tables, ms.Tables.dataset_id == ms.Datasets.id)
        .group_by(ms.Datasets.dataset_name)
        .order_by(ms.Datasets.dataset_name)
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
    return {"datasets": list_dataset}, 200


def post_dataset(request):
    content = request.get_json()
    print(content)

    try:
        validation = ms.SchemaDatasets().load(content)
    except ValidationError as err:
        print(err.messages)
        return err.messages, 400

    dataset = ms.Datasets.query.filter_by(
        project_name=content["project_name"], dataset_name=content["dataset_name"]
    ).first()

    if dataset:
        old_dataset = ms.db.session.query(ms.Datasets).filter(
            ms.Datasets.dataset_name == dataset.dataset_name
        )
        for key, value in content.items():
            setattr(old_dataset, key, value)
    else:
        dataset = ms.Datasets(**content)
        ms.db.session.add(dataset)

    ms.db.session.commit()
    return "OK", 200
