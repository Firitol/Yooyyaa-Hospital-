
from flask_restful import Resource
from flask import request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from schemas import UserLoginSchema

user_login_schema = UserLoginSchema()

class LoginResource(Resource):
    def post(self):
        json_data = request.get_json()
        errors = user_login_schema.validate(json_data)
        if errors:
            return {'errors': errors}, 400

        user = User.query.filter_by(username=json_data['username']).first()
        if user and check_password_hash(user.password, json_data['password']):
            access_token = create_access_token(identity=user.username)
            return {'access_token': access_token, 'role': user.role}, 200
        return {'message': 'Invalid credentials'}, 401
