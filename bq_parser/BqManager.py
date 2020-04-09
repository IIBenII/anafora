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

    return tables
