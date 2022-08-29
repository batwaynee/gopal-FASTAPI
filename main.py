from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import logger

app = FastAPI()

# declaring an empty list to store data
datalist = []

# sql database connection - creating database by name sql
sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()

# Creating table with name address
table = """CREATE TABLE ADDRESS(ID VARCHAR(255),Name VARCHAR(255), Address VARCHAR(255),Coordinates VARCHAR(255));"""
cursor.execute(table)

# intering list of value into database
var_string = ', '.join('?' * len(datalist))
cursor.execute(var_string)


# A basic model in which the data is stored,displayed
class Address(BaseModel):
    id: int
    Name: str
    Address: str
    Coordinates: float


# this function display's welcome message on landing screen
@app.get("/")
def read_welcome_message():
    logger.info("Inside Welcome message function")
    return {
        "greetings": "Welcome This is Address Book Application to access Swagger documentation please got to the link http://127.0.0.1:8000/docs"}


# This function will fetch all the address available
@app.get("/addresses")
def get_all_address():
    return datalist


# This function will fetch the single address required
@app.get("/addresses/{address_id}")
def get_a_address(address_id: int):
    address = address_id - 1
    return datalist[address]


# This function adds/inserts new data into the table
@app.post("/addresses")
def add_address(address: Address):
    datalist.append(address.dict())
    return datalist[-1]


# this function is used to delete any particular entry
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    datalist.pop(address_id - 1)
    return {"task": "deleted address Entry successfully"}
