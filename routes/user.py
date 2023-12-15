# from fastapi import APIRouter
# from  models.user import User
# from config.db import client
# from schemas.user import user_entity,users_entity
#
# user=APIRouter()
#
# @user.get('/')
# async def find_all_users():
#    print()
#    return users_entity()
from fastapi import APIRouter, HTTPException
from models.user import User
from config.db import client
from schemas.user import user_entity, users_entity

user = APIRouter()

database_name = "user_database_name"


@user.get('/')
async def find_all_users():
    user_collection = client[database_name].users

    if 'users' not in client[database_name].list_collection_names():
        client[database_name].create_collection('users')

    users_data = user_collection.find()

    users_list = users_entity(users_data)

    return {"message": "List of users", "users": users_list}


@user.post('/')
async def create_user(user_data: User):
    user_collection = client[database_name].users

    result = user_collection.insert_one(user_data.dict())

    if result.inserted_id:
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")


@user.get('/{user_id}')
async def find_user_by_id(user_id: str):
    user_collection = client[database_name].users

    user_data = user_collection.find_one({"_id": user_id})

    if user_data:
        return user_entity(user_data)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user.put('/{user_id}')
async def update_user(user_id: str, updated_user_data: User):
    user_collection = client[database_name].users

    result = user_collection.update_one({"_id": user_id}, {"$set": updated_user_data.dict()})

    if result.modified_count > 0:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user.delete('/{user_id}')
async def delete_user(user_id: str):
    user_collection = client[database_name].users

    result = user_collection.delete_one({"_id": user_id})

    if result.deleted_count > 0:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
