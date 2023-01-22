from flask import Blueprint, request, jsonify
from app.helpers import token_required
from app.models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'The': 'Vehicle'}


# CREATE CAR ENDPOINT
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    price = request.json['price']
    trim = request.json['trim']
    added_options = request.json['added_options']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    user_token = current_user_token.token
    print(f"current user token: {user_token}")
    car = Car(make, model, price, trim, added_options,
              dimensions, weight, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


# RETRIEVE ALL CARS ENDPOINT
@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    print(f"current user token: {current_user_token}")
    owner = current_user_token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# RETRIEVE ONE CAR ENDPOINT
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


# UPDATE CAR ENDPOINT
@api.route('/cars/<id>', methods=['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)  # Get Car Instance

    car.make = request.json['make']
    car.model = request.json['model']
    car.price = request.json['price']
    car.trim = request.json['trim']
    car.added_options = request.json['added_options']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE CAR ENDPOINT
@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
