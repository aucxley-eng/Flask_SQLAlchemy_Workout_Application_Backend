# Flask SQLAlchemy Workout Application Backend

This project is a complete backend API for a workout tracking application used by personal trainers. It allows for tracking workouts and their associated exercises, including sets, reps, and duration for each exercise within a workout.

## Features

- **Workouts Management**: Create, view, and delete workouts.
- **Exercises Management**: Create, view, and delete exercises.
- **Exercise Tracking**: Add exercises to workouts with specific metrics (reps, sets, duration).
- **Validations**: Robust validations at the database level (Table Constraints), model level (SQLAlchemy @validates), and API level (Marshmallow Schema validations).
- **Serialization**: Efficient serialization and deserialization using Marshmallow, including complex relationships.

## Built With

- **Flask**: A lightweight WSGI web application framework.
- **Flask-SQLAlchemy**: SQLAlchemy support for Flask.
- **Flask-Migrate**: SQLAlchemy database migrations for Flask.
- **Marshmallow**: A library for converting complex data types to and from native Python data types.

## Installation

1. Clone the repository.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies:
   ```bash
   pipenv install
   ```
4. Navigate to the `server` directory:
   ```bash
   cd server
   ```
5. Run database migrations:
   ```bash
   flask db upgrade
   ```
6. Seed the database:
   ```bash
   python seed.py
   ```

## Running the Application

To start the Flask development server:
```bash
python app.py
```
The server will run on `http://localhost:5555`.

## API Endpoints

### Workouts
- `GET /workouts`: List all workouts.
- `GET /workouts/<id>`: Show a single workout with its associated exercises (includes reps, sets, and duration).
- `POST /workouts`: Create a new workout.
- `DELETE /workouts/<id>`: Delete a workout and its associated exercise mappings.

### Exercises
- `GET /exercises`: List all exercises.
- `GET /exercises/<id>`: Show a single exercise and its associated workouts.
- `POST /exercises`: Create a new exercise.
- `DELETE /exercises/<id>`: Delete an exercise and its associated workout mappings.

### Workout Exercises (Join Table)
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`: Add an exercise to a workout with specific reps, sets, and duration.

## Database Schema

### Exercise
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `category` (String, Required)
- `equipment_needed` (Boolean)

### Workout
- `id` (Integer, Primary Key)
- `date` (Date, Required)
- `duration_minutes` (Integer, Required)
- `notes` (Text)

### WorkoutExercise
- `id` (Integer, Primary Key)
- `workout_id` (Integer, Foreign Key to Workout)
- `exercise_id` (Integer, Foreign Key to Exercise)
- `reps` (Integer)
- `sets` (Integer)
- `duration_seconds` (Integer)
