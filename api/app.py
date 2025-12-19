# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config
from models import db, User
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    swagger = Swagger(app, template={
        "info": {
            "title": "Hospital Management API",
            "description": "REST API for hospital workflow management",
            "version": "1.0.0"
        }
    })

    # Create tables
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    # Register API resources
    from api.auth import LoginResource
    from api.patients import PatientListResource, PatientResource
    from api.doctors import DoctorListResource, DoctorAvailabilityResource
    from api.appointments import AppointmentListResource
    from api.billing import BillListResource, PayBillResource

    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(PatientListResource, '/api/patients')
    api.add_resource(PatientResource, '/api/patients/<string:patient_id>')
    api.add_resource(DoctorListResource, '/api/doctors')
    api.add_resource(DoctorAvailabilityResource, '/api/doctors/<string:doctor_id>/availability')
    api.add_resource(AppointmentListResource, '/api/appointments')
    api.add_resource(BillListResource, '/api/bills')
    api.add_resource(PayBillResource, '/api/bills/<string:bill_id>/pay')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'message': 'Resource not found'}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
