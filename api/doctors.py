# api/doctors.py
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import Doctor, Availability, db
from schemas import DoctorSchema, AvailabilitySchema
import uuid

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)
availability_schema = AvailabilitySchema()

class DoctorListResource(Resource):
    @jwt_required()
    def get(self):
        doctors = Doctor.query.all()
        return doctors_schema.dump(doctors), 200

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        errors = doctor_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        doctor = Doctor(
            id=str(uuid.uuid4())[:8],
            name=json_data['name'],
            specialization=json_data['specialization'],
            contact=json_data['contact']
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor_schema.dump(doctor), 201

class DoctorAvailabilityResource(Resource):
    @jwt_required()
    def post(self, doctor_id):
        json_data = request.get_json()
        json_data['doctor_id'] = doctor_id
        errors = availability_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        avail = Availability(
            doctor_id=doctor_id,
            date=json_data['date'],
            time_slot=json_data['time_slot']
        )
        db.session.add(avail)
        db.session.commit()
        return {'message': 'Availability added'}, 201
