from marshmallow import fields
from vivlio.app import db, ma


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


class SchemaGetTables(ma.Schema):
    project_name = fields.Str(required=True)
    dataset_name = fields.Str(required=True)
    compact = fields.Str(required=True)


class SchemaGetTablesInfos(ma.Schema):
    project_name = fields.Str(required=True)
    dataset_name = fields.Str(required=True)
    clean_table_name = fields.Str(required=True)


class Schema(db.Model):

    __tablename__ = "schema"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, index=True, nullable=False)
    field_name = db.Column(db.String(), index=False, nullable=False)
    field_type = db.Column(db.String(), index=False, nullable=False)
    field_mode = db.Column(db.String(), index=False, nullable=False)
    field_description = db.Column(db.String(), index=False, nullable=True)

    __table_args__ = (db.UniqueConstraint("table_id", "field_name", name="_schema"),)


class SchemaFields(ma.Schema):
    field_name = fields.Str(allow_none=False)
    field_type = fields.Str(allow_none=False)
    field_mode = fields.Str(allow_none=False)
    field_description = fields.Str(allow_none=True)


class SchemaSchema(ma.Schema):

    dataset_name = fields.Str()
    project_name = fields.Str()
    table_name = fields.Str()
    schema = fields.List(fields.Nested(SchemaFields))


class SchemaGetSchema(ma.Schema):
    project_name = fields.Str(required=True)
    dataset_name = fields.Str(required=True)
    table_name = fields.Str(required=True)
