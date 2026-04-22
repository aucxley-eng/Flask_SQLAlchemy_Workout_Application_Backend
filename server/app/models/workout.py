from . import db
from sqlalchemy.orm import validates

class Workout(db.Model):
    """
    Represents a specific workout session on a given date.
    Includes validations for positive duration.
    """
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationships: Deleting a workout removes its entries in workout_exercises (Cascade)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not duration or duration <= 0:
            raise ValueError("Workout duration must be a positive integer.")
        return duration

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'
