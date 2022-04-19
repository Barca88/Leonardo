from marshmallow import Schema, fields, validate
from modules.validation.question_schemas import QuestionSchema, DomainSchema

DateSchema = Schema.from_dict(
    {
        "start": fields.Date(required=True),
        "finish": fields.Date(required=True)
    }
)

CompromisesSchema = Schema.from_dict(
    {
        "number_questions": fields.Int(required=True),
        "avg_difficulty": fields.Float(required=True)
    }
)

TestConfig = Schema.from_dict(
    {
        "description": fields.Str(required=True),
        "test_type": fields.Str(required=True, validate=validate.OneOf(['assessment', 'gauging'])),
        "number_questions": fields.Int(required=True),
        "maximum_displayed_answers": fields.Int(required=True),
        "avg_difficulty": fields.Int(allow_none=True),
        "total_time": fields.Int(allow_none=True),
        "question_types": fields.List(fields.Str(allow_none=True)),
        "language": fields.Str(allow_none=True),
        "domain": fields.Nested(DomainSchema, required=True),
        "subdomains": fields.List(fields.Str(allow_none=True)),
        "inserted_by": fields.Str(required=True),
        "last_updated": fields.Date(required=False),
        "date": fields.Nested(DateSchema, required=True),
        "obs": fields.Str(allow_none=True),
        "visibility": fields.Str(required=True, validate=validate.OneOf(['public', 'private']))
    }
)

TestConfiguration = Schema.from_dict(
    {
        "id": fields.Str(required=True),
        "config": fields.Nested(TestConfig, required=True)
    }
)

TestSchema = Schema.from_dict(
    {
        "id": fields.Str(required=True),
        "questions": fields.Nested(QuestionSchema(many=True)),
        "config": fields.Nested(TestConfig, required=True),
        "compromises": fields.Nested(CompromisesSchema, required=True)
    }
)

TestEditSchema = Schema.from_dict(
    {
        "replace": fields.List(fields.Int(allow_none=True)),
        "test": fields.Nested(TestSchema, required=True)
    }
)

OptionSchema = Schema.from_dict(
    {
        "answer": fields.Str(required=True),
        "selected": fields.Bool(required=True),
        "correct": fields.Bool(required=False)
    }
)

QuestionEvaluationSchema = Schema.from_dict(
    {
        "id": fields.Str(required=True),
        "header": fields.Str(required=True),
        "answering_time": fields.Int(required=True),
        "body": fields.Nested(OptionSchema, many=True),
        "result": fields.Int(required=False)
    }
)

TestEvaluationSchema = Schema.from_dict(
    {
        "id": fields.Str(required=True),
        "student_id": fields.Str(required=True),
        "config": fields.Nested(TestConfig, required=True),
        "compromises": fields.Nested(CompromisesSchema, required=True),
        "questions": fields.Nested(QuestionEvaluationSchema, many=True),
        "result": fields.Int(required=False)
    }

)
