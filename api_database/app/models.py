from marshmallow import fields
from . import db, ma


class Datasets(db.Model):

    __tablename__ = "datasets"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(), index=True, nullable=False)
    dataset_name = db.Column(db.String(), index=True, nullable=False)
    created = db.Column(db.String(), index=False, nullable=True)
    modified = db.Column(db.String(), index=False, nullable=True)
    description = db.Column(db.String(), index=False, nullable=True)
    default_table_expiration_ms = db.Column(db.Integer(), index=False, nullable=True)
    default_partition_expiration_ms = db.Column(
        db.Integer(), index=False, nullable=True
    )
    default_encryption_configuration = db.Column(
        db.String(), index=False, nullable=True
    )

    db.Index("_datasets", project_name, dataset_name, unique=True)


class SchemaDatasets(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Datasets


class Tables(db.Model):

    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(), index=True, nullable=False)
    clean_table_name = db.Column(db.String(), index=False, nullable=False)
    created = db.Column(db.String(), index=False, nullable=True)
    modified = db.Column(db.String(), index=False, nullable=True)
    description = db.Column(db.String(), index=False, nullable=True)
    num_bytes = db.Column(db.Integer(), nullable=True)
    num_rows = db.Column(db.Integer(), nullable=True)

    __table_args__ = (db.UniqueConstraint("dataset_id", "table_name", name="_tables"),)


class SchemaTables(ma.Schema):

    dataset_name = fields.Str()
    project_name = fields.Str()
    table_name = fields.Str()
    clean_table_name = fields.Str()
    created = fields.Str(allow_none=True)
    modified = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    num_bytes = fields.Int(allow_none=True)
    num_rows = fields.Int(allow_none=True)
