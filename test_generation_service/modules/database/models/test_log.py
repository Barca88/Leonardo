from pymodm import fields, MongoModel, connect
from modules.database.models.test import Test
from modules.database.models.test_result import TestResult
import settings

DATABASE_HOST=settings.MONGODB_HOST
DATABASE_PORT=settings.MONGODB_PORT
DATABASE=settings.MONGODB_DB

connect('mongodb://' + DATABASE_HOST + ':' + str(DATABASE_PORT) + '/' + DATABASE, alias='tests_logs')

class TestLog(MongoModel):
    action = fields.CharField(required=True)
    test = fields.EmbeddedDocumentField(Test, required=False, blank=True)
    test_result = fields.EmbeddedDocumentField(TestResult, required=False, blank=True)
    time_stamp = fields.CharField(required=True)

    class Meta:
        connection_alias = 'tests_logs'
        collection_name = 'tests_logs'
        final = True

