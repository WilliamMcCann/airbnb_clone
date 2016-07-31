from flask import jsonify, request
from flask_json import json_response
from app.models.city import City
from app import app
from peewee import *

@app.route('/states/<state_id>/cities', methods=['GET','POST'])
def city(state_id):
    ''' city returns a list of all cities in the database where state = state_id in the case of a GET request, and creates a new city in the database in the case of a POST request '''
    if request.method == 'GET':
        list = []
        for record in City.select().where(City.state == state_id):
            hash = record.to_hash()
            list.append(hash)
        return jsonify(list)

    elif request.method == 'POST':
        try:
            record = City(name=request.form["name"], state=state_id)
            record.save()
            return jsonify(record.to_hash())

        # return 409 if city with given name already exists
        except IntegrityError:
                return json_response(
                    add_status_=False,
                    status_=409,
                    code=10002,
                    msg="City already exists in this state"
                )

@app.route('/states/<state_id>/cities/<city_id>', methods=['GET','DELETE'])
def city_id(state_id, city_id):
    ''' '''
    # check whether resource exists:
    # --------------------------------------------------------------------------
    try:
        record = City.get(City.id == city_id)

    # return 404 not found if it does not
    except City.DoesNotExist:
        return json_response(
            add_status_=False,
            status_=404,
            code=404,
            msg="not found"
        )

    # if exception does not arise:
    # --------------------------------------------------------------------------
    if request.method == 'GET':
        return jsonify(record.to_hash())

    elif request.method == "DELETE":
        record.delete_instance()
        record.save()
        return 'deleted city\n'
