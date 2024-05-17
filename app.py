from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import time
from typing import Annotated

app = FastAPI()
origins = ["*"]

app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)
username = "okee3853"
password = "CS351"
uri = f"mongodb+srv://{username}:{password}@cloudcomputingcspace0.e9vkjsj.mongodb.net/ComputerScience?retryWrites=true&w=majority&appName=CloudComputingCSpace0"
# Create a new client and connect to the server
ca = certifi.where()
client = MongoClient(uri, tls=True,
                     tlsAllowInvalidCertificates=True)


class Room(BaseModel):
    name: str
    owner: str
    number: int

class Message:
    def __init(self):
        self.author = ""
        self.message = ""
        self.room = ""
        self.time = 0

class Room:
    def __init__(self):
        self.name = ""
        self.owner = ""
        self.members = ""

    def get_message_history(self):
        # Make database call
        pass


class Session:
    def __init__(self):
        self.room_count = 0
        self.rooms = {}

    def new_session(self):
        self.room_count += 1
        self.rooms[f"Room {self.room_count}"] = "Room Placeholder"
        return f"Room {self.room_count}"

    def delete_session(self, room_number):
        self.rooms.pop(f"Room {room_number}")
        self.room_count -= 1
        return f"Room {self.room_count + 1}"


session = Session()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api")
async def authenticate():
    return {"message": "done"}


# @app.put("/new_room/{name}")
# async def new_room(name: str, room: Room):
#
#    return {"message": "success", "room_name": {room.name}}

@app.get("/api/new_session")
async def new_session():
    room_name = session.new_session()
    return {"sessions": session.room_count,
            "created_room_name": room_name,
            "rooms": session.rooms}

@app.get("/api/sessions")
async def sessions():
    return {"sessions": session.room_count,
            "rooms": session.rooms}


@app.put("/api/delete_session/{session_num}")
async def delete_session(session_num: int):
    room_name = session.delete_session(session_num)
    return {"sessions": session.room_count,
            "deleted_room_name": room_name,
            "rooms": session.rooms}


@app.get("/api/ping_database")
async def ping_database():
    db = client["ComputerScience"]
    collection = db["ComputerScience"]

    post = {
        "room": "test"
    }

    response = collection.find_one({"room_name": "test"}, {'_id': 0})

    return {"response": response}


@app.get("/api/add_message/{room_num}/{message}")
async def add_message(room_num: int, message: str):
    db = client["ComputerScience"]
    collection = db["ComputerScience"]
    message_data = {
        "author": "Placeholder McGee",
        "message": message,
        "room": f"Room {room_num}",
        "time": "test",
    }
    print("before database")
    blah = collection.insert_one(message_data).inserted_id

    print(blah)

    return {
        "return": [
            "okie"
        ]
    }
@app.get("/api/get_messages/{room_num}")
async def get_messages(room_num: int):
    db = client["ComputerScience"]
    collection = db["ComputerScience"]

    response = collection.find({"room": f"Room {room_num}"})
    print(response)
    formatted_response = []
    for message in response:
        formatted_response.append(message["message"])
    return {
        "return": formatted_response
    }

class Message(BaseModel):
    name: str
    message: str

@app.post("/api/header_test")
async def header_test(message: Message):
    return {
        "user_agent": message
    }
