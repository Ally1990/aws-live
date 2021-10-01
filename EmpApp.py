from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    mobile = request.form['mobile']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    location = request.form['location']
    
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if mobile == "":
        return "Please enter mobile number"

    try:

        cursor.execute(insert_sql, (mobile, fname, lname, email, location))
        db_conn.commit()
        emp_name = "" + fname + " " + lname

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")


        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
