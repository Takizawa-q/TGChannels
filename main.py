import asyncio
from pyrogram import Client
from pprint import pprint
from flask import Flask, jsonify, request
import os
from db import Connection, Request, RequestDTO
import datetime
import json

flask_api = Flask(__name__)

def choose_account_from_directory():
    
    accs = [i for i in os.listdir("Accounts/") if "journal" not in i]
    sessions = {i + 1: x for i, x in enumerate(accs)}
    acc_number = input(("\n".join(
                [f"{k} - {v}" for k, v in sessions.items()]) + "\nНапишите цифру аккаунта, в который войти: "))
    account_name_to_login = sessions[int(acc_number)].replace(".session", "")
    
    return account_name_to_login


# @flask_api.route("/post_data/<string:channel_name>", methods=["POST", "GET"])
# async def send_data(channel_name: str):
#     now = datetime.datetime.now()
#     formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
#     requests_table = Request()
#     request_id = await requests_table.add_channel_username(request=RequestDTO(
#         request_id=None,
#         channel_username=channel_name,
#         datetime=formatted_time
#     ))
#     return jsonify({"data_post": "success"})

@flask_api.route("/post_data/<string:channel_name>", methods=["POST", "GET"])
async def send_data(channel_name: str):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    requests_table = Request()
    request_id = await requests_table.add_channel_username(request=RequestDTO(
        request_id=None,
        channel_username=channel_name,
        datetime=formatted_time
    ))  
    return jsonify({"request_id": str(request_id)})

@flask_api.route("/get_data/<string:request_id>", methods=["POST", "GET"])
async def get_data(request_id: str):
    requests_table = Request()
    data = await requests_table.get_answer(request_id=request_id)
    if data:
        return jsonify({"data": json.loads(data)})
    else:
        return jsonify({"data": None})
        

async def main():
    await Connection().create_connection()
    requests_table = Request()
    
    await requests_table.create_table()
    task_1 = asyncio.create_task(flask_api.run(host="149.154.64.48"))
    await asyncio.gather(*[task_1])
   
    




if __name__ == "__main__":
    asyncio.run(main())