from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime
import os

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema, exercise_detail_schema,
    workout_schema, workouts_schema, workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Error handler for Marshmallow validation errors
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(errors=e.messages), 400

# Error handler for model validations (ValueError)
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify(errors={"message": str(e)}), 400

# GET /workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

# GET /workouts/<id>
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200

# POST /workouts
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400
    
    # Convert date string to date object if needed
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

# DELETE /workouts/<id>
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    
    db.session.delete(workout)
    db.session.commit()
    return '', 204

# GET /exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

# GET /exercises/<id>
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
    return jsonify(exercise_detail_schema.dump(exercise)), 200

# POST /exercises
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    errors = exercise_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400
    
    new_exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data.get('equipment_needed', False)
    )
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify(exercise_schema.dump(new_exercise)), 201

# DELETE /exercises/<id>
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return '', 204

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    if not workout:
        return jsonify(errors={"message": "Workout not found"}), 404
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
        
    data = request.get_json() or {}
    # Combine data from URL and body
    full_data = {
        **data,
        "workout_id": workout_id,
        "exercise_id": exercise_id
    }
    
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
    
    # Return workout with updated exercises
    return jsonify(workout_schema.dump(workout)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
