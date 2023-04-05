from flask import Flask
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2

load_dotenv()

app = Flask(__name__)


host = os.getenv("HOST_NAME")
database  = os.getenv("DATABASE")
username  =os.getenv("USER")
password = os.getenv("PWD")
port = os.getenv("PORT_ID")

try:
    connection = psycopg2.connect(host = host,
                            dbname = database,
                            user = username,
                            password = password,
                            port = port)
except Exception as error:
    print(error)


@app.route("/api/data/store_data")
def fetch_data():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM store_data")
            data = cursor.fetchall()[:50]
            return {"data" : data}


if __name__ == '__main__':
    app.run(debug=True)