from . import db
from sqlalchemy.orm import validates

class WorkoutExercise(db.Model):
    """
    The Join Table connecting Workouts and Exercises.
    Stores specific metrics like reps, sets, and duration for an exercise within a workout.
    """
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_metrics(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be a non-negative integer.")
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'
