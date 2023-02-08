from flask import Flask, request, json, jsonify
from pymongo import MongoClient
import certifi
from uuid import uuid4
from datetime import datetime as dt

# ********************************
#           APP CONFIG
# ********************************
app = Flask(__name__)

# ********************************
#         MONGODB CONFIG
# ********************************
cluster = MongoClient("mongodb+srv://admin:ethansq@tripfulcluster.govpqrv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["tripful"]

# ********************************
#             VIEWS
# ********************************

# basic sanity check
# @app.route("/api", methods=["GET"])
# def test():
#     return {"names": ["Nick Jonas", "Joe Jonas"]}

# Get all of the trips (for admin view)
@app.route("/api/read-trips", methods=["GET"])
def read_trips():
    trip_info = db["trips"].find()
    trip_info_id = str(trip_info["Object_id"])
    return [*db["trips"].find()]

# Get all of the ideas (for admin view)
@app.route("/api/read-ideas", methods=["GET"])
def read_ideas():
    return [*db["ideas"].find()]

# Post request to create a trip
@app.route("/api/create-trip", methods=["POST"])
def create_trip():
    request_data = json.loads(request.data)

    # lookup mongo user info from firebase user info

    trip = {
        "_id": uuid4().hex,
        # "created_by": "blahblah"
        "name": request_data["name"],
        "start_date": request_data["start_date"],
        "end_date": request_data["end_date"],
        "guests": [],
        "ideas": []
    }

    db["trips"].insert_one(trip)

    return "SUCCESS: Trip created"

# Post request to create a idea
@app.route("/api/create-idea", methods=["POST"])
def create_idea():
    request_data = json.loads(request.data)

    # lookup mongo user info from firebase user info

    idea = {
        "_id": uuid4().hex,
        # "created_by": "blahblah"
        "title": request_data["title"],
        "author": request_data["author"],
        "created_at": dt.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "last_edited": dt.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "content": request_data["content"],
        "upvotes": [],
        "downvotes": []
    }

    db["ideas"].insert_one(idea)

    return "SUCCESS: Idea created"

# Get request to read ideas from a specific trip
@app.route("/api/read-trip-ideas", methods=["GET"])
def read_trip_ideas():
    request_data = json.loads(request.data)
    trip = db["trips"].find_one({"_id": request_data["_id"]})
    trip_ideas_ids = trip["ideas"]
    trip_ideas = []

    for id in trip_ideas_ids:
        trip_ideas.append(db["ideas"].find_one({"_id": id}))

    return trip_ideas

# Get request to read trips for a specific user
@app.route("/api/read-user-trips", methods=["GET"])
def read_user_trips():
    request_data = json.loads(request.data)
    trips = db["trips"].find({"created_by": request_data["created_by"]})

    return trips

# Put request to update a trip
@app.route("api/update-trip", methods=["PUT"])
def update_trip():
    request_data = json.loads(request.data)

    trip = {
        "_id": request_data["_id"],
        # "created_by": "blahblah"
        "name": request_data["name"],
        "start_date": request_data["start_date"],
        "end_date": request_data["end_date"],
        "guests": request_data["guests"],
        "ideas": request_data["ideas"]
    }
    
    db["trips"].replace_one({"_id": id}, trip)

    return "SUCCESS: Trip updated"

# Put request to update  idea
@app.route("/api/update-idea", methods=["PUT"])
def update_idea():
    request_data = json.loads(request.data)

    idea = {
        "_id": request_data["_id"],
        # "created_by": "blahblah"
        "title": request_data["title"],
        "author": request_data["author"],
        "created_at": request_data["created_at"],
        "last_edited": dt.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "content": request_data["content"],
        "upvotes": request_data["upvotes"],
        "downvotes": request_data["downvotes"]
    }

    db["ideas"].replace_one({"_id": id}, idea)

    return "SUCCESS: Idea updated"

# Delete request for a trip
@app.route("/api/delete-trip", methods=["DELETE"])
def delete_trip():
    request_data = json.loads(request.data)
    db["trips"].delete_one({"_id": request_data["_id"]})

    return "SUCCESS: Deleted trip"

# Delete request for idea
@app.route("/api/delete-idea", methods=["DELETE"])
def delete_idea():
    request_data = json.loads(request.data)
    db["ideas"].delete_one({"_id": request_data["_id"]})

    return "SUCCESS: Deleted idea"

if __name__ == "__main__":
    app.run(debug=True)