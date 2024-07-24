import aiosqlite
from dataclasses import dataclass, field

@dataclass
class RequestDTO:
    request_id: str
    channel_username: str
    datetime: str

class Connection:
    pool: aiosqlite.Connection = None
    @classmethod
    async def create_connection(cls) -> None:
        if cls.pool is None:
            print("CREATING CONNECTION...")
            cls.pool = await aiosqlite.connect(
            database="TelegramParser.db",
        )
            print("CREATED CONNECTION!")
        else:
            print("CONNECTION ALREADY RUNNING")
        return cls

class Request(Connection):
    
    @classmethod
    async def create_table(cls):
        async with cls.pool.cursor() as cur:
            await cur.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_username TEXT NOT NULL,
                is_parsed TEXT NOT NULL,
                datetime TEXT NOT NULL,
                answer TEXT NULL 
            ) 
             """)
    
    @classmethod
    async def check_new_data(cls):
        async with cls.pool.cursor() as cur:
            await cur.execute("SELECT * FROM requests WHERE is_parsed = '0'")
            datas = await cur.fetchall()
            return [RequestDTO(
                request_id=data[0],
                channel_username=data[1],
                datetime=data[3]) for data in datas][::-1]
            
    
    @classmethod
    async def add_channel_username(cls, request: RequestDTO):
        async with cls.pool.cursor() as cur:
            await cur.execute("""INSERT INTO requests (channel_username, datetime, is_parsed) VALUES (?, ?, ?) """,
                              (request.channel_username,
                               request.datetime,
                               0))
            await cls.pool.commit()
            await cur.execute("SELECT request_id FROM requests ORDER BY request_id DESC LIMIT 1")
            data = await cur.fetchone()
            return data[0]
            
    @classmethod
    async def set_is_parsed_1(cls, request_id: str | int):
        async with cls.pool.cursor() as cur:
            await cur.execute(f"""UPDATE requests SET is_parsed = '1' WHERE request_id = '{request_id}'""")
            await cls.pool.commit()
            
    @classmethod
    async def set_answer(cls, request_id: str | int, answer):
        async with cls.pool.cursor() as cur:
            await cur.execute(f"""UPDATE requests SET answer = '{answer}' WHERE request_id = '{request_id}'""")
            await cls.pool.commit()
    
    @classmethod
    async def get_answer(cls, request_id: str | int):
        async with cls.pool.cursor() as cur:
            await cur.execute(f"""SELECT answer FROM requests WHERE request_id = '{request_id}'""")
            data = await cur.fetchone()
            return data[0]
    