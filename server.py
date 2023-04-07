from flask import Flask,jsonify
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import string
import random
import asyncio
load_dotenv()

app = Flask(__name__)


host = os.getenv("HOST_NAME")
database  = os.getenv("DATABASE")
username  =os.getenv("USER")
password = os.getenv("PWD")
port = os.getenv("PORT_ID")



def get_db_connection():
   
    connection = psycopg2.connect(host = host,
                            dbname = database,
                            user = username,
                            password = password,
                            port = port)
    return connection



@app.route("/trigger_report")
def trigger_report():
    report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


    


    connection = get_db_connection()
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


@app.route("/get_report/<report_id>")
def get_report(report_id):
    
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"SELECT status FROM report WHERE report_id='{report_id}'")
        status = cursor.fetchone()
        

        if status is None:
            return jsonify({'error' : "Report ID not found"})
        elif status[0] == 'Running':
            return jsonify({'status' : 'Running'})
        else:
            #TODO : Implement report generation logic 
            pass



    
        
           

    except:
        return "Does not exist"
    finally:
        cursor.close()
        connection.close()


    


if __name__ == '__main__':
    app.run(debug=True)





 