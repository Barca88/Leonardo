from pymodm import fields, MongoModel, connect
from modules.database.models.test import Config, CompromisesSchema
import settings

DATABASE_HOST=settings.MONGODB_HOST
DATABASE_PORT=settings.MONGODB_PORT
DATABASE=settings.MONGODB_DB

connect('mongodb://' + DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE, alias='tests_results')


class Option(MongoModel):
    answer = fields.CharField(required=True)
    selected = fields.BooleanField(required=True)
    correct = fields.BooleanField(required=True)

    class Meta:
        final = True


class QuestionEvaluation(MongoModel):
    id = fields.CharField(required=True)
    header = fields.CharField(required=True)
    answering_time = fields.IntegerField(required=True)
    body = fields.EmbeddedDocumentListField(Option)
    result = fields.IntegerField(required=True)

    class Meta:
        final = True


class TestResult(MongoModel):
    id = fields.CharField(required=True)
    student_id = fields.CharField(required=True)
    config = fields.EmbeddedDocumentField(Config, required=True)
    compromises = fields.EmbeddedDocumentField(CompromisesSchema, required=True)
    questions = fields.EmbeddedDocumentListField(QuestionEvaluation, required=True)
    result = fields.IntegerField(required=True)

    class Meta:
        connection_alias = 'tests_results'
        collection_name = 'tests_results'
        final = True

