import asyncio
import json

import motor.motor_asyncio
import nest_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')
db = client['employees_db']
coll = db['employees']


async def init_db():
    dblist = await client.list_database_names()
    if 'employees_db' not in dblist:
        with open('employees.json') as data_file:
            data = json.loads(data_file.read())
            await coll.insert_many(data)


async def get_employee_list(params):
    cursor = coll.find(params)
    result = await cursor.to_list(length=200)
    return result


nest_asyncio.apply()
asyncio.run(init_db())
