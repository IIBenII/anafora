# API DATABASE

This API allow access to all informations about BigQuery Dataset and tables.

# How to run

```bash
docker build -t api_database .

docker run \
-p 5000:5000 \
-v <path of the folder with sqlite file>:/database \
-e SQLALCHEMY_DATABASE_URI=sqlite:////database/database.sqlite3 \
-e FLASK_APP=vivlio.app \
api_database \
flask init-db

#Run this command if you use sqlite as database
docker run \
-p 5000:5000 \
-v <path of the folder with sqlite file>:/database \
-e SQLALCHEMY_DATABASE_URI=sqlite:////database/database.sqlite3 \
api_database
```

# Swagger

You can access to swagger documentation at this adress http://localhost:5000/swagger.