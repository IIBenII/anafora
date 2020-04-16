from google.cloud import bigquery


client = bigquery.Client()
datasets = list(client.list_datasets())
for datasetref in datasets[60:]:
    dataset = client.get_dataset(datasetref.reference)

