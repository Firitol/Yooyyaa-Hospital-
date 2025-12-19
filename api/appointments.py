# api/appointments.py
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import Appointment, Availability, Patient, Doctor, db
from schemas import AppointmentSchema
import uuid
from datetime import datetime

appointment_schema = AppointmentSchema()

class AppointmentListResource(Resource):
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        errors = appointment_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        # Validate existence
        patient = Patient.query.get(json_data['patient_id'])
        doctor = Doctor.query.get(json_data['doctor_id'])
        if not patient or not doctor:
            return {'message': 'Patient or doctor not found'}, 404

        # Check availability
        slot = Availability.query.filter_by(
            doctor_id=doctor.id,
            date=json_data['date'],
            time_slot=json_data['time_slot'],
            is_booked=False
        ).first()
        if not slot:
            return {'message': 'Slot not available'}, 400

        # Book appointment
        appt = Appointment(
            id=str(uuid.uuid4())[:8],
            patient_id=patient.id,
            doctor_id=doctor.id,
            date=json_data['date'],
            time_slot=json_data['time_slot']
        )
        slot.is_booked = True
        db.session.add(appt)
        db.session.commit()
        return appointment_schema.dump(appt), 201
