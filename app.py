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

class MessageClass:
    def __init(self):
        self.author = ""
        self.message = ""
        self.room_number = 0
        self.time = 0

class RoomClass:
    def __init__(self):
        self.name = ""
        self.owner = ""
        self.members = []

    def get_message_history(self):
        # Make database call
        pass


class Session:
    def __init__(self):
        self.room_count = 0
        self.rooms = {}

    def new_room(self):
        self.room_count += 1
        self.rooms[f"Room {self.room_count}"] = "Room Placeholder"
        return f"Room {self.room_count}"

    def delete_room(self, room_number):
        self.rooms.pop(f"Room {room_number}")
        db = client["ComputerScience"]
        collection = db["ComputerScience"]
        collection.delete_many({"room_number": room_number})

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

@app.post("/api/new_room")
async def new_session():
    room_name = session.new_room()
    return {"sessions": session.room_count,
            "created_room_name": room_name,
            "rooms": session.rooms}

@app.get("/api/current_rooms")
async def sessions():
    return {"room_count": session.room_count,
            "rooms": session.rooms}


@app.post("/api/delete_room/")
async def delete_session(room_number: int):
    room_name = session.delete_room(room_number)
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

class Message(BaseModel):
    author: str
    room_number: int
    message: str
    time: int

@app.post("/api/add_message")
async def add_message(message: Message):
    db = client["ComputerScience"]
    collection = db["ComputerScience"]

    print("before database")
    print(message.dict())
    blah = collection.insert_one(message.dict()).inserted_id

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

    response = collection.find({"room_number": room_num})
    # print(response)
    formatted_response = []
    for message in response:
        data = {"message": message["message"],
                "time": message["time"],
                "author": message["author"],
                }

        formatted_response.append(data)
    print(formatted_response)
    return {
        "return": formatted_response
    }


@app.post("/api/header_test")
async def header_test(message: Message):
    return {
        "user_agent": message
    }
