from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError

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

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        load_instance = True

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

@app.route('/')
def home():
    return "Welcome to the Fitness Center Database!"

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    try:
        new_member = Member(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            date_of_birth=data.get('date_of_birth')
        )
        db.session.add(new_member)
        db.session.commit()
        return member_schema.jsonify(new_member), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email or phone number already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members', methods=['GET'])
def get_members():
    all_members = Member.query.all()
    return members_schema.jsonify(all_members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return member_schema.jsonify(member), 200

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    data = request.json
    try:
        member.first_name = data['first_name']
        member.last_name = data['last_name']
        member.email = data['email']
        member.phone = data.get('phone')
        member.date_of_birth = data.get('date_of_birth')
        
        db.session.commit()
        return member_schema.jsonify(member), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email or phone number already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Member deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



