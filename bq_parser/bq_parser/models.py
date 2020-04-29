from marshmallow import fields
from bq_parser.database import db


class Jobs(db.Model):

    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(), index=True, nullable=False)
    job_type = db.Column(db.String(), index=False, nullable=False)
    job_status = db.Column(db.String(), index=False, nullable=True)
    job_start = db.Column(db.String(), index=False, nullable=False)


# class SchemaJobs(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Jobs
