# schemas.py
from marshmallow import Schema, fields, validate, ValidationError

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class PatientSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    age = fields.Int(required=True, validate=validate.Range(min=0, max=150))
    gender = fields.Str(required=True, validate=validate.OneOf(['Male', 'Female', 'Other']))
    contact = fields.Str(required=True)
    address = fields.Str(required=True)

class DoctorSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    specialization = fields.Str(required=True)
    contact = fields.Str(required=True)

class AvailabilitySchema(Schema):
    doctor_id = fields.Str(required=True)
    date = fields.Date(required=True)
    time_slot = fields.Str(required=True)

class AppointmentSchema(Schema):
    id = fields.Str(dump_only=True)
    patient_id = fields.Str(required=True)
    doctor_id = fields.Str(required=True)
    date = fields.Date(required=True)
    time_slot = fields.Str(required=True)
    status = fields.Str(dump_only=True)

class BillSchema(Schema):
    id = fields.Str(dump_only=True)
    patient_id = fields.Str(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.Str(required=True)
    paid = fields.Bool(dump_only=True)
