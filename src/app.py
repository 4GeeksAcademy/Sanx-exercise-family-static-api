"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# todos los miembros
@app.route('/members', methods=['GET'])
def get_all_family_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200
# un miembro
@app.route('/members/<int:id>', methods=['GET'])
def get_family_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404
 #añadir miembro   
@app.route('/members', methods=['POST'])
def add_new_member():
    request_body = request.get_json()
    if request_body is None:
        raise APIException("You need to specify the request body as a json", status_code=400)
    member = {
        "first_name": request_body.get("first_name"),
        "last_name": "Jackson",
        "age": request_body.get("age"),
        "lucky_numbers": request_body.get("lucky_numbers")
    }
    if all(key in member for key in ("first_name", "age", "lucky_numbers")):
        jackson_family.add_member(member)
        new_member = jackson_family.get_all_members()[-1]
        return jsonify(new_member), 200 
    else:
        return jsonify({"msg": "Invalid member data"}), 400
    
 # borrar miembro   
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    if jackson_family.delete_member(id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"msg": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
