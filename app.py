from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    student_number = db.Column(db.String(50), unique=True)
    course = db.Column(db.String(100))

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.get_json()
    student = Student(name=data['name'], student_number=data['student_number'], course=data['course'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'})

@app.route('/students')
def get_students():
    students = Student.query.all()
    return jsonify([{'name': s.name, 'student_number': s.student_number, 'course': s.course} for s in students])

if __name__ == '__main__':
    if not os.path.exists('students.db'):
        db.create_all()
    app.run(debug=True)
