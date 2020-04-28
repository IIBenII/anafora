import datetime

from flask import request
from flask import current_app as app
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy import func
from rq import Queue, cancel_job
from rq.job import Job
import requests

from bq_parser.src import BqManager as bq

import bq_parser.models as ms
from bq_parser.redis import conn

q = Queue(connection=conn)


@app.route("/health")
def health():
    return "OK"


@app.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job_status(job_id):
    job = Job.fetch(job_id, connection=conn)

    if job.get_status() != "started":

        old_job = ms.db.session.query(ms.Jobs).filter(ms.Jobs.job_id == job_id).first()
        old_job.job_status = "delete"
        ms.db.session.commit()
        job.cancel()
        return f"Can't delete running job {job_id}", 403

    return f"Job {job_id} delete"


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job_status(job_id):
    job = Job.fetch(job_id, connection=conn)
    return job.get_status()


@app.route("/jobs", methods=["GET"])
def get_jobs():
    query_result = ms.db.session.query(ms.Jobs).order_by(ms.Jobs.job_start.desc()).all()

    list_jobs = []
    for elt in query_result:
        list_jobs.append(
            {
                "job_id": elt.job_id,
                "job_type": elt.job_type,
                "job_status": elt.job_status,
                "job_start": elt.job_start,
            }
        )
    return jsonify({"jobs": list_jobs})


@app.route("/datasets", methods=["POST"])
def submit_dataset():
    result = q.enqueue(bq.get_datasets, job_timeout="-1")

    job = ms.Jobs(
        job_id=result.id,
        job_start=datetime.datetime.now(),
        job_type="build_datasets",
        job_status=Job.fetch(result.id, connection=conn).get_status(),
    )

    ms.db.session.add(job)
    ms.db.session.commit()

    return result.id


@app.route("/tables", methods=["POST"])
def submit_tables():

    datasets = requests.get("http://172.17.0.1:5000/datasets")

    all_ids = []
    for datatset in datasets.json().get("datasets")[:4]:
        result = q.enqueue(
            bq.get_tables_of_dataset,
            args=(datatset.get("project_id"), datatset.get("dataset_name")),
            job_timeout="-1",
        )
        all_ids.append(result.id)

        job = ms.Jobs(
            job_id=result.id,
            job_start=datetime.datetime.now(),
            job_type=f"build_table--{datatset.get('dataset_name')}",
            job_status=Job.fetch(result.id, connection=conn).get_status(),
        )

        ms.db.session.add(job)
        ms.db.session.commit()

    return {"all_ids": all_ids}
