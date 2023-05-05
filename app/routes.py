from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal

# class Crystal:
#     def __init__(self, id, name, color, powers):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.powers = powers

#create a list of crystals
# crystals = [
#     Crystal(1, "Amethyst", "Purple", "Infinite knowledge and wisdom"),
#     Crystal(5, "Tiger's Eye", "Gold", "Confidence"),
#     Crystal(2, "Sapphire", "Dark Blue", "Peace"),
#     Crystal(3, "Rose Quartz", "Pink", "Self Love"),
# ]


# Blueprint to glue all our crystal routes together
crystal_bp = Blueprint("books", __name__, url_prefix="/crystals")

# # define the function to handle the crystals
# @crystals_bp.route("", methods=["GET"])
# def handle_crystals():
#     crystals_response = []
#     for crystal in crystals:
#         crystals_response.append({
#             "id": crystal.id,
#             "name": crystal.name,
#             "color": crystal.color,
#             "powers": crystal.powers
#         })
#     return jsonify(crystals_response)

# # route will look like localhost:5000/crystals/1
# # create a decorator to group the same route to crystals
# @crystals_bp.route("/<crystal_id>", methods=["GET"])
# determine respresentation and return response.
# def handle_crystal(crystal_id):
#     crystal = validate_crystal_id(crystal_id)

#     return {
#         "id" : crystal.id,
#         "name": crystal.name,
#         "color": crystal.color,
#         "powers": crystal.powers
#             }

# HELPER FUNCTION - VALIDATES CRYSTAL ID EXISTS
# responsible for validating and returning crystal instance
def validate_crystal_id(crystal_id):
    # makes sure the data type is an integer
    try: 
        crystal_id = int(crystal_id)
    except ValueError:
        abort(make_response({"message": f"{crystal_id} is not a valid type. A {(type(crystal_id))} data type was provided. Must be a valid integer data type."},400))
    
    # crystal_id is confirmed an integer so connect with db
    crystal = Crystal.query.get(crystal_id)

    if not crystal:
        abort(make_response({"message:" : f"crystal {crystal_id} does not exist"},404))
    
    return crystal
    

# define a route to create a new crystal
# POST /crystals
# CREATE NEW CRYSTAL - POST METHOD
@crystal_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def handle_crystal():
    request_body = request.get_json()  

    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"]
    )

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f'Yayyyy Crystal {new_crystal.name} successfully created!'), 201

# define a route for getting all crystals
# GET /crystals
# READ ALL CRYSTAL - GET METHOD
@crystal_bp.route("", methods=['GET'])
# read all crystals
def read_all_crystals():
    crystals_response = []

    #filter the crystal query results
    # to those whose color match the 
    # query param
    color_query = request.args.get("color")
    powers_query = request.args.get("powers")

    if color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        crystals = Crystal.query.filter_by(powers=powers_query)
    else:
        crystals = Crystal.query.all()

    for crystal in crystals:
        crystals_response.append({
            "id": crystal.id,
            "name": crystal.name,
            "color": crystal.color,
            "powers": crystal.powers
        })
    return jsonify(crystals_response)

# define a route for getting a single crystal
# GET /crystals/<crystal_id>
# READ ONE CRYSTAL - GET METHOD
@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    # Query our db to grab the crystal that has the id we want
    crystal = validate_crystal_id(crystal_id)

    # show a single crystal
    return {
        "id" : crystal.id,
        "name": crystal.name,
        "color": crystal.color,
        "powers": crystal.powers
    }, 200

# define a route for updating a crystal
# PUT /crystals/<crystal_id>
# UPDATE ONE CRYSTAL - PUT METHOD
@crystal_bp.route("/<crystal_id>", methods=["PUT"])
def update_crystal(crystal_id):
    crystal = validate_crystal_id(crystal_id)

    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    db.session.commit()

    return {
        "id" : crystal.id,
        "name": crystal.name,
        "color": crystal.color,
        "powers": crystal.powers
    }, 200

# define a route for deleting a crystal
# DELETE /crystals/<crystal_id>
# DELETE A CRYSTAL - DELETE METHOD
@crystal_bp.route("/<crystal_id>", methods=["DELETE"])
def delete_crystal(crystal_id):
    crystal = validate_crystal_id(crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal #{crystal_id} successfully deleted")
