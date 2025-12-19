
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import Patient, db
from schemas import PatientSchema
import uuid

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

class PatientListResource(Resource):
    @jwt_required()
    def get(self):
        patients = Patient.query.all()
        return patients_schema.dump(patients), 200

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        errors = patient_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        new_patient = Patient(
            id=str(uuid.uuid4())[:8],
            name=json_data['name'],
            age=json_data['age'],
            gender=json_data['gender'],
            contact=json_data['contact'],
            address=json_data['address']
        )
        db.session.add(new_patient)
        db.session.commit()
        return patient_schema.dump(new_patient), 201

class PatientResource(Resource):
    @jwt_required()
    def get(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        return patient_schema.dump(patient), 200
