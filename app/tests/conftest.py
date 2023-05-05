# import pytest to access to functionality - especially the .fixture
import pytest
# import to make an instance of the app that we will run - instance for our testing environment
# create_app returns an instance of create_app
from app import create_app
# import db to make an instance of the database we are working in
from app import db
# routes can get cached on memory - line 11-13 makes sure that we are working with the most recent data
# doesn't store older information
from flask.signals import request_finished
# import our Crystal model
from app.models.crystal import Crystal

@pytest.fixture
def app():
    # we could set to True or test_config=True
    # True can be 1 or "Hello, I miss you"
    app = create_app({"TESTING": True})

    # remove anything from the old session to end
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    # create all the tables and then yield for everything to populate
    with app.app_context():
        # use to create the tables we want to use
        db.create_all()
        # like return but it waits for all the fixtures and tests to pass and run
        # then continue with the rest of the code
        yield app

    # after everything is done then it wil continue and remove the database being used
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def make_two_crystals(app):
    crystal_1 = Crystal(
        name = "pearl",
        color = "white",
        powers = "pretty powers"
    )
    crystal_2 = Crystal(
        name = "garnet",
        color = "red",
        powers = "awesomeness + protection against disasters, evil spirits, and mental insanity"
    )
    
    # populate our database with our two crystals
    db.session.add_all([crystal_1, crystal_2])
    db.session.commit()
