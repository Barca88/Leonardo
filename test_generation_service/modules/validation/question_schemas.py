from marshmallow import Schema, fields

BodySchema = Schema.from_dict(
    {
        "answer": fields.Str(),
        "correction": fields.Int(),
        "mandatory": fields.Boolean()
    }
)

DomainSchema = Schema.from_dict(
    {
        "study_cycle": fields.Str(),
        "scholarity": fields.Str(),
        "description": fields.Str()
    }
)

QuestionSchema = Schema.from_dict(
    {
        "id": fields.Str(),
        "language": fields.Str(),
        "domain": fields.Nested(DomainSchema),
        "subdomain": fields.Str(),
        "difficulty_level": fields.Str(),
        "display_mode": fields.Str(),
        "answering_time": fields.Str(),
        "type": fields.Str(),
        "precedence": fields.List(fields.Str(required=True)),
        "repetitions": fields.Str(),
        "header": fields.Str(),
        "body": fields.Nested(BodySchema(many=True)),
        "solution": fields.Str(),
        "images": fields.Str(),
        "videos": fields.Str(),
        "source": fields.Str(),
        "notes": fields.Str(),
        "status": fields.Str(),
        "inserted_by": fields.Str(),
        "inserted_at": fields.Str(),
        "validated_by": fields.Str(),
        "validated_at": fields.Str()
    }
)

QuestionUpdateSchema = Schema.from_dict(
    {
        "id": fields.Str(allow_none=True),
        "language": fields.Str(allow_none=True),
        "domain": fields.Nested(DomainSchema, allow_none=True),
        "subdomain": fields.Str(allow_none=True),
        "difficulty_level": fields.Str(allow_none=True),
        "display_mode": fields.Str(allow_none=True),
        "answering_time": fields.Str(allow_none=True),
        "type": fields.Str(allow_none=True),
        "precedence": fields.List(fields.Str(required=True), allow_none=True),
        "repetitions": fields.Str(allow_none=True),
        "header": fields.Str(allow_none=True),
        "body": fields.Nested(BodySchema(many=True), allow_none=True),
        "solution": fields.Str(allow_none=True),
        "images": fields.Str(allow_none=True),
        "videos": fields.Str(allow_none=True),
        "source": fields.Str(allow_none=True),
        "notes": fields.Str(allow_none=True),
        "status": fields.Str(allow_none=True),
        "inserted_by": fields.Str(allow_none=True),
        "inserted_at": fields.Str(allow_none=True),
        "validated_by": fields.Str(allow_none=True),
        "validated_at": fields.Str(allow_none=True)
    }
)
