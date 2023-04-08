from typing import Optional, Any
import logging

import pymongo
import uuid
from datetime import datetime

import config
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(config.mongodb_uri)
        self.db = self.client["chatgpt_telegram_bot"]
        
        self.user_collection = self.db["user"]
        self.dialog_collection = self.db["dialog"]
        self.allowed_users = self.db["allowed_users"]

    def check_if_user_exists(self, user_id: int, raise_exception: bool = False):
 
        if self.user_collection.count_documents({"_id": user_id}) > 0:
  
            return True
        else:
            if raise_exception:
                raise ValueError(f"User {user_id} does not exist")
            else:
                return False

    def add_new_user(
        self,
        user_id: int,
        chat_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
    ):
        user_dict = {
            "_id": user_id,
            "chat_id": chat_id,

            "username": username,
            "first_name": first_name,
            "last_name": last_name,

            "last_interaction": datetime.now(),
            "first_seen": datetime.now(),

            "current_dialog_id": None,
            "current_chat_mode": "assistant",
            "current_model": config.models["available_text_models"][0],

            "n_used_tokens": {},
            "n_tokens_balance": config.n_default_tokens,
            "n_transcribed_seconds": 0.0  # voice message transcription
        }

        if not self.check_if_user_exists(user_id):
            self.user_collection.insert_one(user_dict)
    
    def find_user_id(self,username):
        query = {'username': username}

        # Use the find_one method to retrieve the first matching entry
        result = self.user_collection.find_one(query)
        return result['chat_id']
    

    async def is_user_allowed(self,username):
            query = {'usernames': username}
            existing_user = self.allowed_users.find_one(query)
            
            if existing_user:
                logger.info(f"Username {username} already exists in the collection")
                return True
            return False

    async def add_alllowed_user(self,username):
            query = {'usernames': username}
            existing_user = self.allowed_users.find_one(query)
            
            if existing_user:
                logger.info(f"Username {username} already exists in the collection")
                return
            
            # If the username doesn't exist, add it to the collection
            result = self.allowed_users.update_one({}, {'$push': {'usernames': username}})
            if result.modified_count == 1:
                logger.info(f"Added username {username} to the collection")
            else:
                logger.info(f"Failed to add username {username} to the collection")


    async def remove_allowed_user(self,username):
            query = {'usernames': username}
            existing_user = self.allowed_users.find_one(query)
            
            if not existing_user:
                logger.info(f"Username {username} not exists in the collection")
                return
            
            # If the username doesn't exist, add it to the collection
            result = self.allowed_users.update_one({}, {'$pull': {'usernames': username}})
            if result.modified_count == 1:
                logger.info(f"Deleted username {username} to the collection")
            else:
                logger.info(f"Failed to Delete username {username} to the collection")

    async def recharge_user_balance(self,user_id,new_balance):
         current_balance = self.get_user_attribute(user_id, "n_tokens_balance")
         self.set_user_attribute(user_id,'n_tokens_balance',current_balance+new_balance)
         return current_balance+new_balance
 

        
    async def isHasBalance(self,user_id):
        return self.get_user_attribute(user_id,"n_tokens_balance")>150
    

    def start_new_dialog(self, user_id: int):
        self.check_if_user_exists(user_id, raise_exception=True)

        dialog_id = str(uuid.uuid4())
        dialog_dict = {
            "_id": dialog_id,
            "user_id": user_id,
            "chat_mode": self.get_user_attribute(user_id, "current_chat_mode"),
            "start_time": datetime.now(),
            "model": self.get_user_attribute(user_id, "current_model"),
            "messages": []
        }

        # add new dialog
        self.dialog_collection.insert_one(dialog_dict)

        # update user's current dialog
        self.user_collection.update_one(
            {"_id": user_id},
            {"$set": {"current_dialog_id": dialog_id}}
        )

        return dialog_id

    def get_user_attribute(self, user_id: int, key: str):
        self.check_if_user_exists(user_id, raise_exception=True)
        user_dict = self.user_collection.find_one({"_id": user_id})

        if key not in user_dict:
            return None

        return user_dict[key]

    def set_user_attribute(self, user_id: int, key: str, value: Any):
        self.check_if_user_exists(user_id, raise_exception=True)
        self.user_collection.update_one({"_id": user_id}, {"$set": {key: value}})

    def update_n_used_tokens(self, user_id: int, model: str, n_input_tokens: int, n_output_tokens: int):
        n_used_tokens_dict = self.get_user_attribute(user_id, "n_used_tokens")
        n_overall_used_tokens = n_input_tokens+n_output_tokens
        if model in n_used_tokens_dict:
            n_used_tokens_dict[model]["n_input_tokens"] += n_input_tokens
            n_used_tokens_dict[model]["n_output_tokens"] += n_output_tokens
        else:
            n_used_tokens_dict[model] = {
                "n_input_tokens": n_input_tokens,
                "n_output_tokens": n_output_tokens
            }
        current_balance = self.get_user_attribute(user_id, "n_tokens_balance")
        if n_overall_used_tokens < current_balance:
            self.set_user_attribute(user_id,'n_tokens_balance',current_balance - n_overall_used_tokens)
        else:
            self.set_user_attribute(user_id,'n_tokens_balance',0)
        self.set_user_attribute(user_id, "n_used_tokens", n_used_tokens_dict)
         

    def get_dialog_messages(self, user_id: int, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)

        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")

        dialog_dict = self.dialog_collection.find_one({"_id": dialog_id, "user_id": user_id})
        return dialog_dict["messages"]

    def set_dialog_messages(self, user_id: int, dialog_messages: list, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)

        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")

        self.dialog_collection.update_one(
            {"_id": dialog_id, "user_id": user_id},
            {"$set": {"messages": dialog_messages}}
        )
