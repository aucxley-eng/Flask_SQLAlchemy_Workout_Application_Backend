from . import db
from sqlalchemy.orm import validates

class Exercise(db.Model):
    """
    Represents a specific physical exercise (e.g., Pushups, Running).
    Includes validations for name length and category presence.
    """
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationships: Deleting an exercise removes its entries in workout_exercises (Cascade)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Exercise must have a name.")
        if len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return name

    @validates('category')
    def validate_category(self, key, category):
        if not category:
            raise ValueError("Exercise must have a category.")
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'
