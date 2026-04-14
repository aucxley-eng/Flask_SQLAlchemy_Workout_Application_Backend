from marshmallow import Schema, fields, validate, validates, ValidationError
from models import db, Exercise, Workout, WorkoutExercise

class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(min=3, error="Name must be at least 3 characters.")])
    category = fields.String(required=True, validate=[validate.Length(min=1, error="Category is required.")])
    equipment_needed = fields.Boolean()

    class Meta:
        load_instance = True

class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(validate=[validate.Range(min=0, error="Reps must be non-negative.")])
    sets = fields.Integer(validate=[validate.Range(min=0, error="Sets must be non-negative.")])
    duration_seconds = fields.Integer(validate=[validate.Range(min=0, error="Duration must be non-negative.")])
    
    # Nested fields for detailed view
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True, validate=[validate.Range(min=1, error="Duration must be positive.")])
    notes = fields.String()

    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

# Instantiate schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
