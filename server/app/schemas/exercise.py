from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import db
from app.models.exercise import Exercise

class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        include_fk = True
        sqla_session = db.session

    name = fields.String(required=True, validate=[validate.Length(min=3, error="Name must be at least 3 characters.")])
    category = fields.String(required=True, validate=[validate.Length(min=1, error="Category is required.")])

class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=("exercise",)), dump_only=True)
