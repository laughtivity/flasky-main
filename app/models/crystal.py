from app import db

class Crystal(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    powers = db.Column(db.String)

    # we want to let the program know we want to use this before we create the instance
    # cls - is a reference to the class itself (not the object)
    @classmethod
    def from_dict(cls, crystal_data):
        new_crystal = Crystal(
            name = crystal_data["name"],
            color = crystal_data["color"],
            powers = crystal_data["powers"]
        )
        return new_crystal
    
    # method that is used on an object - instance of a class 
    # after the object is created an object
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "color":self.color,
            "powers": self.powers
        }

