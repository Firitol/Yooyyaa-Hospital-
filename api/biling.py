# api/billing.py
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import Bill, Patient, db
from schemas import BillSchema
import uuid

bill_schema = BillSchema()
bills_schema = BillSchema(many=True)

class BillListResource(Resource):
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        errors = bill_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        patient = Patient.query.get(json_data['patient_id'])
        if not patient:
            return {'message': 'Patient not found'}, 404

        bill = Bill(
            id=str(uuid.uuid4())[:8],
            patient_id=patient.id,
            amount=json_data['amount'],
            description=json_data['description']
        )
        db.session.add(bill)
        db.session.commit()
        return bill_schema.dump(bill), 201

class PayBillResource(Resource):
    @jwt_required()
    def post(self, bill_id):
        bill = Bill.query.get_or_404(bill_id)
        bill.paid = True
        db.session.commit()
        return {'message': 'Bill marked as paid'}, 200
