from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, Workout, Exercise, WorkoutExercise
from app.schemas import workout_schema, workouts_schema, workout_exercise_schema

workout_bp = Blueprint('workout_bp', __name__)

@workout_bp.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@workout_bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200

@workout_bp.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400
    
    if isinstance(data['date'], str):
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
    
    new_workout = Workout(
        date=data['date'],
        duration_minutes=data['duration_minutes'],
        notes=data.get('notes')
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(workout_schema.dump(new_workout)), 201

@workout_bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    
    db.session.delete(workout)
    db.session.commit()
    return '', 204

@workout_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
        
    data = request.get_json() or {}
    full_data = {**data, "workout_id": workout_id, "exercise_id": exercise_id}
    
    errors = workout_exercise_schema.validate(full_data)
    if errors:
        return jsonify(errors=errors), 400
        
    new_we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(new_we)
    db.session.commit()
    
    return jsonify(workout_schema.dump(workout)), 201
