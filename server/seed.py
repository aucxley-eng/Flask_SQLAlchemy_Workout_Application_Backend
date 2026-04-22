#!/usr/bin/env python3

from app import create_app
from app.models import db, Exercise, Workout, WorkoutExercise
from datetime import date

app = create_app()

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    e1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    e2 = Exercise(name="Pullups", category="Strength", equipment_needed=True)
    e3 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    e4 = Exercise(name="Deadlifts", category="Powerlifting", equipment_needed=True)

    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(date=date(2023, 10, 1), duration_minutes=45, notes="Morning session")
    w2 = Workout(date=date(2023, 10, 2), duration_minutes=60, notes="Evening session")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Seeding WorkoutExercises...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=20, sets=3)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e3.id, duration_seconds=1200)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, reps=10, sets=5)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e4.id, reps=5, sets=3)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database seeded successfully!")
