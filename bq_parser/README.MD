# BQ Parser

This API is used to submit job (get BigQuery datasets and tables infomartions) to Readis worker.

# How to run

Before you need a service account (in JSON) used to access to GCP, with authorization `BigQuery read metadata`.

First you need a Redis container. You can launch one with
```bash
docker pull redis
docker run redis
```

Then you can add redis worker. To achieve that you need to build the image in the folder `worker`.

```bash
docker build -f worker/Dockerfile -t redis-worker .

#Save the URI of the Database API, for example
EXPORT DATABASE_URI=http://172.17.0.1:5000

#Save the redis Database URI, for example
EXPORT REDIS_URI=redis://172.17.0.5:6379

docker run \
-v <your path of the folder containing the gcp service account>:/key \
-e GOOGLE_APPLICATION_CREDENTIALS=/key/key.json \
-v <patch where you clone the repository>/anafora/bq_parser:/app \
-e API_DATABASE_URI=$DATABASE_URI \
redis-worker \
$REDIS_URI
```

Finally build the API by running

```bash
docker build -t bq_parser .

#In case you are using sqlite you need to mount the folder containing the sqllite file

#Init database

docker run \
-v <sqlite folder>:/database \
-e SQLALCHEMY_DATABASE_URI=sqlite:////database/parser.sqlite3 \
-e FLASK_APP=bq_parser.app
bq_parser flask init-db

#Run the API
docker run \
-p 5001:5001 \
-v <sqlite folder>:/database \
-v <your path of the folder containing the gcp service account>:/key \
-e GOOGLE_APPLICATION_CREDENTIALS=/key/key.json \
-e SQLALCHEMY_DATABASE_URI=sqlite:////database/parser.sqlite3 \
-e REDIS_URI=$REDIS_URI \
-e API_DATABASE_URI=$DATABASE_URI \
bq_parser
```

# Swagger

You can access to swagger documentation at this adress http://localhost:5001/swagger.