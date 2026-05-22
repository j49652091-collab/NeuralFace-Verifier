import json

def login(username,password):

    with open("users.json","r") as f:
        user=json.load(f)

    if username==user["username"] and password==user["password"]:
        return True

    return False
