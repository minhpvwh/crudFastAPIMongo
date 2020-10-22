import motor.motor_asyncio
from bson.objectid import ObjectId
from configs import IP_MONGO_DETAIL

# MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.
MONGO_DETAILS = IP_MONGO_DETAIL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.fface

student_collection = database.get_collection("abc")
device_collection = database.get_collection("device")


# helpers


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        # "email": student["email"],
        # "course_of_study": student["course_of_study"],
        # "year": student["year"],
        # "GPA": student["gpa"],
    }


def device_helper(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": device["name"],
        "location": device["location"],
        "temp_from": device["temp_from"],
        "temp_to": device["temp_to"],
        "client_id": device["client_id"],
        "secret_key": device["secret_key"],
        "status": device["status"],
        "version": device["version"]
    }


def create_device_helper(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": device["name"],
        "location": device["location"],
        "temp_from": device["temp_from"],
        "temp_to": device["temp_to"],
        "client_id": str(device["_id"]),
        "secret_key": device["secret_key"],
        "status": device["status"],
        "version": device["version"]
    }


# crud operations
# ===> DEVICE
# Retrieve a student with a matching ID
async def retrieve_device(id: str) -> dict:
    device = await device_collection.find_one({"_id": ObjectId(id)})
    if device:
        return device_helper(device)


# Retrieve all device present in the database
async def retrieve_devices():
    devices = []
    async for device in device_collection.find():
        devices.append(device_helper(device))
    return devices


# Add a new device into to the database
async def add_device(device_data: dict) -> dict:
    device = await device_collection.insert_one(device_data)
    data = {
        "client_id": str(device.inserted_id)
    }
    new_device = await device_collection.find_one_and_update({"_id": device.inserted_id}, {"$set": data}, upsert=True)
    return create_device_helper(new_device)


# Update a device with a matching ID
async def update_device(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    device = await device_collection.find_one({"_id": ObjectId(id)})
    if device:
        updated_device = await device_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        print(type(updated_device))  # <class 'pymongo.results.UpdateResult'>
        print(updated_device)  # <pymongo.results.UpdateResult object at 0x7efdf5a43780>
        if updated_device:
            return True
        return False


# Delete a device from the database
async def delete_device(id: str):
    device = await device_collection.find_one({"_id": ObjectId(id)})
    if device:
        await device_collection.delete_one({"_id": ObjectId(id)})
        return True


# ===> STUDENT

# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        print(student)
        students.append(student_helper(student))
    return students


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
