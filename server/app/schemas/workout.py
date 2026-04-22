from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import db
from app.models.workout import Workout

class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        include_fk = True
        sqla_session = db.session

    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=[validate.Range(min=1, error="Duration must be positive.")])
    
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=("workout",)), dump_only=True)
