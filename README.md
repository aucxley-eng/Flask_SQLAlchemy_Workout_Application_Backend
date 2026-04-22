# Flask SQLAlchemy Workout Application Backend

This is a modular backend API for a workout tracking application, built with Flask, SQLAlchemy, and Marshmallow.

## Features
- **Workouts**: Track workout sessions with dates and notes.
- **Exercises**: Reusable exercise database.
- **Workout Exercises**: Join table to track specific sets, reps, and duration for each exercise in a workout.
- **Validations**: Triple-layer validation (Database, Model, and Schema).
- **Modular Structure**: Organized using the App Factory and Blueprint patterns.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pipenv install
   ```
3. Enter the virtual environment:
   ```bash
   pipenv shell
   ```
4. Navigate to the `server` directory:
   ```bash
   cd server
   ```
5. Initialize and run migrations (if starting fresh):
   ```bash
   flask db upgrade
   ```
6. Seed the database:
   ```bash
   python seed.py
   ```

## Running the Application
To start the development server:
```bash
python run.py
```
The server will run on `http://localhost:5555`.

## API Endpoints

### Workouts
- `GET /workouts`: List all workouts.
- `GET /workouts/<id>`: Show a single workout with its associated exercises.
- `POST /workouts`: Create a new workout.
- `DELETE /workouts/<id>`: Delete a workout and its associated exercises.

### Exercises
- `GET /exercises`: List all exercises.
- `GET /exercises/<id>`: Show an exercise and its history in different workouts.
- `POST /exercises`: Create a new exercise.
- `DELETE /exercises/<id>`: Delete an exercise.

### Workout Exercises (The Join)
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`: Add an exercise to a specific workout with `reps`, `sets`, and `duration_seconds`.

## Tech Stack
- **Flask**: Framework
- **SQLAlchemy**: ORM
- **Marshmallow**: Serialization & Validation
- **Flask-Migrate**: Migrations
