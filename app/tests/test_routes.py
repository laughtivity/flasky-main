
# test 1 = get all the crystals but we want it to be empty
# clean database

def test_read_all_crystals_return_empty_list(client):
    # arrange
    # does not need to be used

    # act
    # gets us access to all the methods
    response = client.get("/crystals")
    response_body = response.get_json()

    # assert
    # check to make sure the list is empty
    assert response_body == []
    # check the status code of the response - successful request because the resources was found
    assert response.status_code == 200

def test_read_crystal_by_id(client, make_two_crystals):
    response = client.get("/crystals/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "garnet",
        "color": "red",
        "powers": "awesomeness + protection against disasters, evil spirits, and mental insanity"
    }
    
def test_create_crystal(client):
    response = client.post("/crystals", json={
        "name" : "tiger's eye",
        "color": "golden brown",
        "powers": "focus the mind, promoting mental clarity, assisting us to resolve problems objectively and unclouded by emotions."
    })

    # get the json from the response
    response_body = response.get_json()

    # check for status code and response body is a successfully created message
    assert response.status_code == 201
    # if we did not return a json then it returns none
    #
    assert response_body == "Yayyyy Crystal tiger's eye successfully created!"