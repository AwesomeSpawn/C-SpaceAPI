from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

app = FastAPI()
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
        return f"Room {self.room_count+1}"




session = Session()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/authenticate")
async def authenticate():
    return {"message": "done"}



#@app.put("/new_room/{name}")
#async def new_room(name: str, room: Room):
#
#    return {"message": "success", "room_name": {room.name}}

@app.get("/new_session")
async def new_session():
    room_name = session.new_session()
    return {"sessions": session.room_count,
            "created_room_name": room_name,
            "rooms": session.rooms}

@app.put("/delete_session/{session_num}")
async def delete_session(session_num: int):
    room_name = session.delete_session(session_num)
    return {"sessions": session.room_count,
            "deleted_room_name": room_name,
            "rooms": session.rooms}

@app.get("/ping_database")
async def ping_database():

    db = client["ComputerScience"]
    collection = db["ComputerScience"]

    post = {
        "room": "test"
    }
    
    response = collection.find_one({"room_name": "test"}, {'_id': 0})

    return {"response": response}

