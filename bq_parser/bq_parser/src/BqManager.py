import os

from google.cloud import bigquery
from typing import List, Tuple
import requests
import datetime


def get_datasets() -> List[bigquery.dataset.DatasetReference]:
    """Make calls to BigQuery API to get Datasets informations and send the result
       to Database API.

    Returns:
        list: list of all datasets
    """
    client = bigquery.Client()
    datasets = list(client.list_datasets())
    for datasetref in datasets:
        dataset = client.get_dataset(datasetref.reference)
        requests.post(
            f"{os.getenv('API_DATABASE_URI')}/datasets",
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
        print(dataset)
    return datasets


def clean_table_name(table_name: str) -> str:
    """Cleant table name when table is indexed by date

    Args:
        table_name (str): table name like foo_bar_20200101

    Returns:
        str: table name without date like foo_bar_
    """
    table_name_split = table_name.split("_")
    try:
        datetime.datetime.strptime(table_name_split[-1], "%Y%m%d")
    except ValueError:
        return table_name

    return "_".join(table_name_split[:-1]) + "_"


def build_recursive_schema(
    schema: List[bigquery.schema.SchemaField], parent: str = None
) -> List[Tuple[str]]:
    """Build schema list, can be recursive call in case of record field type

    Args:
        schema (List[google.cloud.bigquery.schema.SchemaField]): List of schemaField
        parent ([str], optional): Parent name inc ase of record field type. Defaults to None.

    Returns:
        List[Tuple[str]]: List of fields unested
    """
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


def get_tables_of_dataset(
    project_name: str, dataset_id: str
) -> List[bigquery.table.TableReference]:
    """List all table in scpecific dataset

    Args:
        project_name (str): project name
        dataset_id (str): dataset name

    Returns:
        List[google.cloud.bigquery.table.TableReference]: List of table
    """
    client = bigquery.Client()
    tables = list(client.list_tables("{}.{}".format(project_name, dataset_id)))

    for tableref in tables:
        table = client.get_table(tableref.reference)
        requests.post(
            f"{os.getenv('API_DATABASE_URI')}/tables",
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

        requests.post(f"{os.getenv('API_DATABASE_URI')}/schema", json=values_to_insert)

    return tables
