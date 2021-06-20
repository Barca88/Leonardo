from pymodm import fields, MongoModel, connect
import settings

DATABASE_HOST=settings.MONGODB_HOST
DATABASE_PORT=settings.MONGODB_PORT
DATABASE=settings.MONGODB_DB

connect('mongodb://' + DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE, alias='questions')

class Question(MongoModel):
    id = fields.CharField()
    language = fields.CharField(blank=True)
    domain = fields.DictField(blank=True)
    subdomain = fields.CharField(blank=True)
    subsubdomain = fields.CharField(blank=True)
    difficulty_level = fields.CharField(blank=True)
    display_mode = fields.CharField(blank=True)
    answering_time = fields.CharField(blank=True)
    type = fields.CharField(blank=True)
    precedence = fields.ListField(fields.CharField(
        blank=True), required=True, blank=True)
    repetitions = fields.CharField(blank=True)
    header = fields.CharField(blank=True)
    body = fields.ListField(fields.DictField())
    solution = fields.CharField(blank=True)
    images = fields.CharField(blank=True)
    videos = fields.CharField(blank=True)
    source = fields.CharField(blank=True)
    notes = fields.CharField(blank=True)
    status = fields.CharField(blank=True)
    inserted_by = fields.CharField(blank=True)
    inserted_at = fields.CharField(blank=True)
    validated_by = fields.CharField(blank=True)
    validated_at = fields.CharField(blank=True)

    class Meta:
        connection_alias = 'questions'
        collection_name = 'questions'
        final = True
