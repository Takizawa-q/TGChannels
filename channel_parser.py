import asyncio
from db import Request, Connection
from pyrogram import Client

async def check_new_data(request_table,
                         app):
    
    data = await request_table.check_new_data()
    
    for dat in data:
        try:
            channel_info = await app.get_chat(dat.channel_username)
            await request_table.set_answer(request_id=dat.request_id,
                                        answer=channel_info)
        except Exception as e:
            print("ERROR", e)
            data = await request_table.set_is_parsed_1(request_id=dat.request_id)
        
async def main():
    await Connection().create_connection()
    requests_table = Request()
    account_name_to_login = "new_acc"
    app = Client(f"Accounts/{account_name_to_login}")
    await app.start()
    while True:
        await check_new_data(request_table=requests_table,
                             app=app)
    
    
    
    
if __name__ == "__main__":
    asyncio.run(main())