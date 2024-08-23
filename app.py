from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from password import my_password
from marshmallow import ValidationError




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@localhost/new_schema'
db = SQLAlchemy(app)
ma= Marshmallow(app)



class MembersSchema():
    id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)
    class Meta:
        fields = ("id", "name", "age")



class WorkoutSessionsSchema():
    session_id = fields.String(required=True)
    member_id = fields.String(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)
    class Meta:
        fields = ("session_id", "member_id", "session_date", "session_time", "activity")



members_schema = MembersSchema()
workoutsessions_schema = WorkoutSessionsSchema()



class Member(db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    age = db.Column(db.Integer(3))
    workouts = db.relationship("WorkoutSessions", backref = "Members")

class WorkoutSession(db.Model):
    __tablename__ = "WorkoutSessions"
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer(3), db.ForeignKey("Members.id"))
    session_date = db.Column(db.String(9))
    session_time = db.Column(db.String(5))
    activity = db.Column(db.String(100))

#Members CRUD Info

@app.route('/members', methods=['GET'])
def get_member():
    members = Member.query.all()
    return members_schema.jsonify(members)


@app.route("/members/<int:id>", methods = ['GET'])
def get_members(id):
    customer = Member.query.get_or_404(id)
    return members_schema.jsonify(customer)



@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = members_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_member = Member(name=member_data['name'], id=member_data['id'], age=member_data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "New Customer added succesfully!"}), 201



@app.route('/members/<int:id>', methods = ['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)

    try:
        member_data = members_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    member.name = member_data['name']
    member.email = member_data['email']
    member.phone = member_data['phone']

    db.session.commit()
    return jsonify({"message":"Customer details updated succesfully!"}), 200
    


@app.route('/members/<int:id>', methods = ['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message":"Customer Deleted succesfully!"}), 200


#WorkoutSessions CRUD Info

@app.route('/workoutsessions', methods=['GET'])
def get_workout_sessions():
    members = WorkoutSession.query.all()
    return workoutsessions_schema.jsonify(members)


@app.route("/workoutsessions/<int:id>", methods = ['GET'])
def get_workoutsessions(id):
    session = WorkoutSession.query.get_or_404(id)
    return workoutsessions_schema.jsonify(session)



@app.route('/workoutsessions', methods=['POST'])
def add_workoutsession():
    try:
        workoutsession_data = workoutsessions_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_session = WorkoutSession(session_id = workoutsession_data["session id"], member_id = workoutsession_data["member id"], session_date = workoutsession_data["session date"], session_time = workoutsession_data["session time"], activity = workoutsession_data["activity"])
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "New Customer added succesfully!"}), 201



@app.route('/workoutsessions/<int:id>', methods = ['PUT'])
def update_workoutsession(id):
    session = WorkoutSession.query.get_or_404(id)
    try:
        workoutsession_data = workoutsessions_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    session.session_id = workoutsession_data["session id"]
    session.session_member = workoutsession_data["member id"]
    session.session_date = workoutsession_data["session date"]
    session.session_time = workoutsession_data["session tim"]
    session.activity = workoutsession_data["activity"]

    db.session.commit()
    return jsonify({"message":"Customer details updated succesfully!"}), 200
    


@app.route('/workoutsession/<int:id>', methods = ['DELETE'])
def delete_workoutsession(id):
    session = WorkoutSession.query.get_or_404(id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({"message":"Customer Deleted succesfully!"}), 200



with app.app_context():
    db.create_all()



if __name__ =="__main__":
    app.run(debug = True)