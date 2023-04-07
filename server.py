from flask import Flask,jsonify
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import string
import random
import uuid
load_dotenv()

app = Flask(__name__)


host = os.getenv("HOST_NAME")
database  = os.getenv("DATABASE")
username  =os.getenv("USER")
password = os.getenv("PWD")
port = os.getenv("PORT_ID")



@app.route("/trigger_report")
def trigger_report():
    report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


    connection = psycopg2.connect(host = host,
                            dbname = database,
                            user = username,
                            password = password,
                            port = port)
    
    cursor = connection.cursor()

    try:

        cursor.execute(f"INSERT INTO Report VALUES('{report_id}','Running')")
        connection.commit()

        # TODO : Generate report asyncrhonously
        
        return jsonify({"Report ID" : report_id })
    except:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()







    


if __name__ == '__main__':
    app.run(debug=True)





    # with connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute(f"SELECT * FROM store_data WHERE store_id = {store_id}")
    #         data = cursor.fetchall()

    #         return {"length" : len(data),"data" : data}