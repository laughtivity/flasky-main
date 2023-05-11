from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal
from app.models.healer import Healer

# Blueprint to glue all our crystal routes together
crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")
healer_bp = Blueprint("healers", __name__, url_prefix = "/healers")
# HELPER FUNCTION - VALIDATES CRYSTAL ID EXISTS
# responsible for validating and returning crystal instance
def validate_model(cls, model_id):
    # makes sure the data type is an integer
    try: 
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{model_id} is not a valid type. A {(type(model_id))} data type was provided. Must be a valid integer data type."},400))
    
    # model_id is confirmed an integer so connect with db
    # changed Crystal to cls to utilize
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message:" : f"{cls.__name__} {model_id} does not exist"},404))
    
    return model
    

# define a route to create a new crystal
# POST /crystals
# CREATE NEW CRYSTAL - POST METHOD
@crystal_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_crystal():
    request_body = request.get_json()  

    new_crystal = Crystal.from_dict(request_body)

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
        crystals_response.append(crystal.to_dict())
    return jsonify(crystals_response)

# define a route for getting a single crystal
# GET /crystals/<crystal_id>
# READ ONE CRYSTAL - GET METHOD
@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    # Query our db to grab the crystal that has the id we want
    crystal = validate_model(crystal_id)

    # show a single crystal
    return crystal.to_dict(), 200

# define a route for updating a crystal
# PUT /crystals/<crystal_id>
# UPDATE ONE CRYSTAL - PUT METHOD
@crystal_bp.route("/<crystal_id>", methods=["PUT"])
def update_crystal(crystal_id):
    crystal = validate_model(crystal_id)

    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    db.session.commit()

    return crystal.to_dict(), 200

# define a route for deleting a crystal
# DELETE /crystals/<crystal_id>
# DELETE A CRYSTAL - DELETE METHOD
@crystal_bp.route("/<crystal_id>", methods=["DELETE"])
def delete_crystal(crystal_id):
    crystal = validate_model(crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal #{crystal_id} successfully deleted")


## PASTED FROM STUDY HALL FROM MIKELLE
## HEALER
@healer_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_healer():
    request_body = request.get_json()
    
    new_healer = Healer(
        name=request_body["name"]
    )
    
    db.session.add(new_healer)
    db.session.commit()
    
    return jsonify(f"Yayyyy Healer {new_healer.name} successfully created!"), 201


@healer_bp.route("", methods=["GET"])
def read_all_healers():
    
    healers = Healer.query.all()
        
    healers_response = []
    
    for healer in healers:
        healers_response.append({ "name": healer.name, "id": healer.id})
    
    return jsonify(healers_response)

# POST METHOD - CREATE A CRYSTAL BY ID linking it to the healer
# already established a crystal by crystal_id route so it does not need
@healer_bp.route("/<healer_id>/crystals", methods = ["POST"])
def create_crystal_by_id(healer_id):
    
    healer = validate_model(Healer,healer_id)
    request_body = request.get_json()

    # can we use todict from Crystal?
    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"],
        healer = healer
    )

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} owned by {new_crystal.healer.name} was successfully created."), 201

# GET METHOD - READ CRYSTALS BY HEALER ID
@healer_bp.route("/<healer_id>/crystals", methods=["GET"])
def get_all_crystals_with_id(healer_id):
    healer = validate_model(Healer, healer_id)

    crystal_response = []

    for crystal in healer.crystals:
        crystal_response.append(crystal.to_dict())
    
    return jsonify(crystal_response), 200