from google.cloud import bigquery
import requests
import datetime


def get_datasets():
    client = bigquery.Client()
    datasets = list(client.list_datasets())
    for datasetref in datasets:
        dataset = client.get_dataset(datasetref.reference)
        requests.post(
            "http://172.17.0.1:5000/datasets",
            json={
                "project_name": dataset.project,
                "dataset_name": dataset.dataset_id,
                "created": dataset.created.strftime("%Y-%m-%d %H:%M:%S"),
                "modified": dataset.modified.strftime("%Y-%m-%d %H:%M:%S"),
                "description": dataset.description,
                "default_table_expiration_ms": dataset.default_table_expiration_ms,
                "default_partition_expiration_ms": dataset.default_partition_expiration_ms,
                "default_encryption_configuration": dataset.default_encryption_configuration,
            },
        )
    return datasets


def clean_table_name(table_name):
    table_name_split = table_name.split("_")
    try:
        datetime.datetime.strptime(table_name_split[-1], "%Y%m%d")
    except ValueError:
        return table_name

    return "_".join(table_name_split[:-1]) + "_"


def build_recursive_schema(schema, parent=None):
    result = []
    for elt in schema:
        if not parent:
            full_name = elt.name
        else:
            full_name = parent + "." + elt.name

        result.append((full_name, elt.field_type, elt.mode, elt.description))

        if elt.field_type == "RECORD":
            result += build_recursive_schema(elt.fields, full_name)

    return result


def get_tables_of_dataset(project_name, dataset_id):
    client = bigquery.Client()
    tables = list(client.list_tables("{}.{}".format(project_name, dataset_id)))

    for tableref in tables:
        table = client.get_table(tableref.reference)
        requests.post(
            "http://172.17.0.1:5000/tables",
            json={
                "project_name": table.project,
                "dataset_name": table.dataset_id,
                "table_name": table.table_id,
                "clean_table_name": clean_table_name(table.table_id),
                "created": table.created.strftime("%Y-%m-%d %H:%M:%S"),
                "modified": table.modified.strftime("%Y-%m-%d %H:%M:%S"),
                "description": table.description,
                "num_bytes": table.num_bytes,
                "num_rows": table.num_rows,
            },
        )
        unpack_schema = build_recursive_schema(table.schema)

        values_to_insert = {
            "project_name": table.project,
            "dataset_name": table.dataset_id,
            "table_name": table.table_id,
            "schema": [],
        }

        for field in unpack_schema:
            field_name, field_type, field_mode, field_description = field

            values_to_insert["schema"].append(
                {
                    "field_name": field_name,
                    "field_type": field_type,
                    "field_mode": field_mode,
                    "field_description": field_description,
                }
            )

        requests.post("http://172.17.0.1:5000/schema", json=values_to_insert)

    return tables
