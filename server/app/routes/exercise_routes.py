from flask import Blueprint, request, jsonify
from app.models import db, Exercise
from app.schemas import exercise_schema, exercises_schema, exercise_detail_schema

exercise_bp = Blueprint('exercise_bp', __name__)

@exercise_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@exercise_bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
    return jsonify(exercise_detail_schema.dump(exercise)), 200

@exercise_bp.route('/exercises', methods=['POST'])
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

@exercise_bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify(errors={"message": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return '', 204
