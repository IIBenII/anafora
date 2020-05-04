from flask import request
from flask import current_app as app
from marshmallow import ValidationError
from sqlalchemy import func

from vivlio.src import datasets as ds
from vivlio.src import tables as ts
from vivlio.src import table_infos as ti
from vivlio.src import schema as sm
from vivlio.src import search as sc


@app.route("/health")
def health():
    return "OK"


@app.route("/datasets", methods=["POST", "GET"])
def insert_dataset():
    if request.method == "GET":
        return ds.get_dataset()
    else:
        return ds.post_dataset(request)


@app.route("/tables", methods=["POST", "GET"])
def get_tables():
    if request.method == "GET":
        return ts.get_tables(request)
    else:
        return ts.post_tables(request)


@app.route("/table_infos", methods=["GET"])
def get_table_infos():
    if request.method == "GET":
        return ti.get_table_infos(request)


@app.route("/schema", methods=["GET", "POST"])
def get_schema():
    if request.method == "GET":
        return sm.get_schema(request)
    else:
        return sm.post_schema(request)


@app.route("/search", methods=["GET"])
def search_datasets():
    if request.method == "GET":
        return sc.search(request)
