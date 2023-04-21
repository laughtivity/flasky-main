from flask import Blueprint, jsonify

class Crystal:
    def __init__(self, id, name, color, powers):
        self.id = id
        self.name = name
        self.color = color
        self.powers = powers

#create a list of crystals

crystals = [
    Crystal(1, "Amethyst", "Purple", "Infinite knowledge and wisdom"),
    Crystal(5, "Tiger's Eye", "Gold", "Confidence"),
    Crystal(2, "Sapphire", "Dark Blue", "Peace"),
    Crystal(3, "Rose Quartz", "Pink", "Self Love"),
]

crystals_bp = Blueprint("books", __name__, url_prefix="/crystals")

@crystals_bp.route("", methods=["GET"])

#define the function to handle the crystals
def handle_crystals():

    crystals_response = []

    for crystal in crystals:
        crystals_response.append({
            "id": crystal.id,
            "name": crystal.name,
            "color": crystal.color,
            "powers": crystal.powers
        })

    return jsonify(crystals_response)
