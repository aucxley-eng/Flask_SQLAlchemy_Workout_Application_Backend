from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import db
from app.models.workout_exercise import WorkoutExercise

class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True
        include_relationships = True
        sqla_session = db.session

    reps = fields.Integer(validate=[validate.Range(min=0, error="Reps must be non-negative.")])
    sets = fields.Integer(validate=[validate.Range(min=0, error="Sets must be non-negative.")])
    duration_seconds = fields.Integer(validate=[validate.Range(min=0, error="Duration must be non-negative.")])
    
    exercise = fields.Nested("ExerciseSchema", dump_only=True)
    workout = fields.Nested("WorkoutSchema", dump_only=True)
