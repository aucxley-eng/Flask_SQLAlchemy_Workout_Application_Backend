from .exercise import ExerciseSchema, ExerciseDetailSchema
from .workout import WorkoutSchema
from .workout_exercise import WorkoutExerciseSchema

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
