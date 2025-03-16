import mariadb
import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv

# Load .env values
load_dotenv()

# Connect to database
client = mariadb.connect(
    user = "pi",
    password = os.environ.get("DB_PASSWORD"),
    host = "localhost",
    database = "viisausdb"
)
client.autocommit = False
cursor = client.cursor()

# Get number of rows in database
cursor.execute("SELECT COUNT(*) FROM viisaudet")
data = cursor.fetchone()

# Make a list of file paths of all files in specified folder and sort them
path = "/home/pi/Music"
onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
onlyfiles.sort(key = lambda a : len(a))

# See if there are more files in the list than rows in database
subtraction = len(onlyfiles) - data[0]
if subtraction > 0:
    for i in range(len(onlyfiles) - subtraction, len(onlyfiles)):
        try:
            cursor.execute("INSERT INTO viisaudet (file) VALUES (?)", (onlyfiles[i],))
        except mariadb.Error as e:
            client.rollback()
            print(f"Error: {e}")
    client.commit()
    print(f"Last inserted ID: {cursor.lastrowid}")

client.close()