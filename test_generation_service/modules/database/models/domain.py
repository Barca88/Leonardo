from pymodm import fields, MongoModel, connect
import settings

DATABASE_HOST=settings.MONGODB_HOST
DATABASE_PORT=settings.MONGODB_PORT
DATABASE=settings.MONGODB_DB

connect('mongodb://' + DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE, alias='domains')


class Domain(MongoModel):
    description = fields.CharField(required=True)
    scholarity = fields.CharField(required=True)
    study_cycle = fields.CharField(required=True)

    class Meta:
        connection_alias = 'domains'
        collection_name = 'domains'
        final = True

