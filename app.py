from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:%24E%40kster1@localhost/fitness_center_db"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    workout_sessions = db.relationship('WorkoutSession', backref='member', lazy=True)

class WorkoutSession(db.Model):
    __tablename__ = 'workoutsessions'
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.Date, nullable=False)
    session_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



