import mariadb
import random
import os
from dotenv import load_dotenv

async def queryHelper():
    load_dotenv()
    
    # Connect to database
    client = mariadb.connect(
        user = "root",
        password = os.environ.get("DB_PASSWORD"),
        host = "localhost",
        database = "viisausdb"
    )
    client.autocommit = False
    cursor = client.cursor()

    # Get number of rows in database
    cursor.execute("SELECT COUNT(*) FROM viisaudet")
    count = cursor.fetchone()

    # Get random number between 1 and a number of rows in the database
    randInt = random.randint(1, count[0])

    # Get file path from database using random number
    cursor.execute("SELECT file FROM viisaudet WHERE id = ?", (randInt,))
    file = cursor.fetchone()
    
    return file[0]