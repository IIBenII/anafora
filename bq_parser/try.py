from google.cloud import bigquery


client = bigquery.Client()

tables = list(
    client.list_tables(
        "{}.{}".format("mdm-data-preprod", "b_transform_dispatch_backup")
    )
)

print(len(tables))
# for tableref in tables:
#     table = client.get_table(tableref.reference)

# datasets = list(client.list_datasets())
# for datasetref in datasets[60:]:
#     dataset = client.get_dataset(datasetref.reference)

# dataset_ref = bigquery.dataset.DatasetReference(
#     "mdm-data-preprod", "a_collecte_pubsub_orders"
# )
# table_ref = bigquery.table.TableReference(
#     dataset_ref, "customer_invoice_events_20200402"
# )
# table = client.get_table(table_ref)

# schema = table.schema


# def recursive_schema(schema, result, parent=None):
#     for elt in schema:
#         if elt.field_type != "RECORD":
#             if not parent:
#                 result.append((elt.name, elt.field_type))
#             else:
#                 result.append((parent + "." + elt.name, elt.field_type))
#         else:
#             if not parent:
#                 recursive_schema(elt.fields, result, elt.name)
#             else:
#                 recursive_schema(elt.fields, result, parent + "." + elt.name)


# def recursive_schema(schema, parent=None):

#     result = []

#     for elt in schema:
#         if not parent:
#             full_name = elt.name
#         else:
#             full_name = parent + "." + elt.name

#         result.append((full_name, elt.field_type, elt.mode, elt.description))

#         if elt.field_type == "RECORD":
#             result += recursive_schema(elt.fields, full_name)
#     return result


# result = recursive_schema(schema)

# for field in result:
#     field_name, field_type, field_mode, field_description = field
#     # print(field_name)


# print("\n\n\n")
# print(result)
