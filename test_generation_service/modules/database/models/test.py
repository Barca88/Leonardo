from pymodm import fields, MongoModel, connect
from modules.database.models.question import Question
import settings

DATABASE_HOST=settings.MONGODB_HOST
DATABASE_PORT=settings.MONGODB_PORT
DATABASE=settings.MONGODB_DB

connect('mongodb://' + DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE, alias='tests')

class DateSchema(MongoModel):
    start = fields.CharField(required=True)
    finish = fields.CharField(required=True)

    class Meta:
        final = True


class CompromisesSchema(MongoModel):
    avg_difficulty = fields.FloatField(required=True)
    number_questions = fields.IntegerField(required=True)

    class Meta:
        final = True


class Config(MongoModel):
    description = fields.CharField(required=True)
    test_type = fields.CharField(required=True, blank=True)
    number_questions = fields.IntegerField(required=True)
    maximum_displayed_answers = fields.IntegerField(required=False)
    avg_difficulty = fields.IntegerField(
        required=True, min_value=1, max_value=5)
    total_time = fields.IntegerField(required=True)
    question_types = fields.ListField(fields.CharField(blank=True))
    language = fields.CharField(required=False)
    domain = fields.DictField(required=True)
    subdomains = fields.ListField(fields.CharField(required=False))
    inserted_by = fields.CharField(required=True)
    last_updated = fields.CharField(required=True)
    date = fields.EmbeddedDocumentField(DateSchema)
    obs = fields.CharField(required=False, min_length=None)
    visibility = fields.CharField(choices=('public', 'private'))

    class Meta:
        final = True


class Test(MongoModel):
    id = fields.CharField(required=True)
    questions = fields.EmbeddedDocumentListField(Question)
    config = fields.EmbeddedDocumentField(Config)
    compromises = fields.EmbeddedDocumentField(CompromisesSchema)

    class Meta:
        connection_alias = 'tests'
        collection_name = 'tests'
        final = True


