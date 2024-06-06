
#Citation Scope: Entire app.py File - Adapated basic routing, redirection, add/edit/delete routes, flask imports and mysql config code
#Date: 12JUN2023
#Originality: Adapated 
#Source: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route("/")
def home():
    return redirect("/patients")

# -------- Patient Entity Routes ---------- #

@app.route("/patients", methods=['GET', 'POST'])
def patients():
    # Separate out the request methods, in this case this is for a POST
    # insert a patient into the patient entity
    if request.method == "POST":
        # fire off if user presses the Add Patient button
        if request.form.get("Add_Patient"):
            # grab user form inputs
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            birthday = request.form["birthday"]
            phone = request.form["phone"]
            email = request.form["email"]
            street1 = request.form["street1"]
            street2 = request.form["street2"]
            city = request.form["city"]
            zip = request.form["zip"]

            # perform insert operation
            query = "INSERT INTO Patients (first_name, last_name, birthday, phone, email, street1, street2, city, zip) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, birthday, phone, email, street1, street2, city, zip))
            mysql.connection.commit()

            # redirect back to patients page
            return redirect("/patients")

    # Grab patient data so we send it to our template to display
    else:
        # mySQL query to grab all the people in bsg_people
        query = "SELECT * from Patients"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_patient page passing our query data to the edit_patient template
        return render_template("patients.j2", data=data)

@app.route("/delete_patient/<int:patient_id>")
def delete_patient(patient_id):
    # mySQL query to delete the patient with our passed patient_id
    query = "DELETE FROM Patients WHERE patient_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (patient_id,))
    mysql.connection.commit()

    # redirect back to patients page
    return redirect("/patients")

@app.route("/edit_patient/<int:patient_id>", methods=["POST", "GET"])
def edit_patient(patient_id):
    if request.method == "GET":
        # mySQL query to grab the info of the patient with our passed id
        query = "SELECT * FROM Patients WHERE Patient_id = %s" % (patient_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_patients page passing our query data to the edit_patient template
        return render_template("edit_patient.j2", data=data)
    
    if request.method == "POST":
        # fire off if user clicks the 'Edit Patient' button
        if request.form.get("Edit_Patient"):
            patient_id = request.form["patient_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            birthday = request.form["birthday"]
            phone = request.form["phone"]
            email = request.form["email"]
            street1 = request.form["street1"]
            street2 = request.form["street2"]
            city = request.form["city"]
            zip = request.form["zip"]

           
            query = "UPDATE Patients SET Patients.first_name = %s, Patients.last_name = %s, Patients.birthday = %s, Patients.phone = %s, Patients.email = %s, Patients.street1 = %s, Patients.street2 = %s, Patients.city = %s, Patients.zip = %s WHERE Patients.patient_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, birthday, phone, email, street1, street2, city, zip, patient_id))
            mysql.connection.commit()

            return redirect("/patients")

# ------------- Patient Entity Routes End ---------------- #

# ------------- Test Entity Routes ----------------------- #

@app.route("/tests", methods=['GET', 'POST'])
def tests():
    # Separate out the request methods, in this case this is for a POST
    # insert a test into the test entity
    if request.method == "POST":
        # fire off if user presses the Add Test button
        if request.form.get("Add_Test"):
            # grab user form inputs. form variable is actually the dept_id due to the option value selected.
            test_name = request.form["test_name"]
            test_desc = request.form["test_desc"]
            dept_name = request.form["dept_name"]

            # perform insert operation
            query = "INSERT INTO Tests (test_name, test_desc, dept_id) VALUES(%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (test_name, test_desc, dept_name))
            mysql.connection.commit()

            # redirect back to tests page
            return redirect("/tests")

    # Grab test data so we send it to our template to display
    else:
        # mySQL query to grab all the people in tests
        query = "SELECT Tests.test_id, Tests.test_name, Tests.test_desc, Departments.dept_name FROM Tests INNER JOIN Departments ON Tests.dept_id = Departments.dept_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab all the department names in departments
        query2 = "SELECT dept_id, dept_name from Departments"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        department_data = cur.fetchall()

        # render tests page passing our query data to the tests template
        return render_template("tests.j2", data=data, departments=department_data)

# Delete a test
@app.route("/delete_test/<int:test_id>")
def delete_tests(test_id):
    # mySQL query to delete the patient with our passed patient_id
    query = "DELETE FROM Tests WHERE test_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (test_id,))
    mysql.connection.commit()

    # redirect back to patients page
    return redirect("/tests")

# Edit a test
@app.route("/edit_test/<int:test_id>", methods=["POST", "GET"])
def edit_test(test_id):
    if request.method == "GET":
        # mySQL query to grab the info of the patient with our passed id
        query = "SELECT Tests.test_id, Tests.test_name, Tests.test_desc, Departments.dept_name FROM Tests INNER JOIN Departments ON Tests.dept_id = Departments.dept_id WHERE test_id = %s" % (test_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT dept_id, dept_name FROM Departments"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        departments = cur.fetchall()

        # render edit_patients page passing our query data to the edit_patient template
        return render_template("edit_test.j2", data=data, departments=departments)
    
    if request.method == "POST":
        # fire off if user clicks the 'Edit Patient' button
        if request.form.get("Edit_Test"):
            test_id = request.form["test_id"]
            test_name = request.form["test_name"]
            test_desc = request.form["test_desc"]
            dept_id = request.form["dept_name"]
            
            query = "UPDATE Tests SET Tests.test_name = %s, Tests.test_desc = %s, Tests.dept_id = %s WHERE Tests.test_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (test_name, test_desc, dept_id, test_id))
            mysql.connection.commit()

            return redirect("/tests")

# ------------- Test Entity Routes End -------------------- #

# ------------- Departments Entity Routes ----------------- #

@app.route("/departments", methods=['GET', 'POST'])
def departments():
    # Separate out the request methods, in this case this is for a POST
    # insert a department into the departments entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Department"):
            # grab user form inputs
            dept_name = request.form["dept_name"]
            total_tests = request.form["total_tests"]

            # perform insert operation
            query = "INSERT INTO Departments (dept_name, total_tests) VALUES(%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (dept_name, total_tests))
            mysql.connection.commit()

            # redirect back to departments page
            return redirect("/departments")

    # Grab departments data so we send it to our template to display
    else:
        # mySQL query to grab all the departments in departments
        query = "SELECT * from Departments"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render departments page passing our query data to the departments template
        return render_template("departments.j2", data=data)

# ------------- Departments Entity END Routes -------------- #


# ------------- Test Records Entity ------------------------ #

@app.route("/testrecords", methods=['GET', 'POST'])
def testrecords():
    # Separate out the request methods, in this case this is for a POST
    # insert a test record into the test records entity
    if request.method == "POST":
        # fire off if user presses the Add Test Record button
        if request.form.get("Add_TestRecord"):
            # grab user form inputs
            patient_id = request.form["patient_name"]
            test_id = request.form["test_name"]
            requested_date = request.form["requested_date"]
            priority = request.form["priority"]

            # perform insert operation
            query = "INSERT INTO Test_Records (patient_id, test_id, requested_date, priority) VALUES(%s,%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (patient_id, test_id, requested_date, priority))
            mysql.connection.commit()

            # redirect back to departments page
            return redirect("/testrecords")
        
    # Grab test records data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the tests in test records
        query = "SELECT Test_Records.record_id, Patients.patient_id, CONCAT(Patients.first_name, ' ', Patients.last_name) as patient_name, Tests.test_id, Tests.test_name, Test_Records.requested_date, (CASE WHEN Test_Records.completed = 1 THEN 'YES' ELSE 'NO' END) AS completed,IFNULL(Test_Records.completed_date, '') AS completed_date, Test_Records.priority FROM Test_Records LEFT JOIN Patients ON Test_Records.patient_id = Patients.patient_id LEFT JOIN Tests ON Test_Records.test_id = Tests.test_id ORDER BY Test_Records.completed, Test_Records.priority, Test_Records.requested_date ASC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT patient_id, CONCAT(last_name, ', ', first_name) AS name FROM Patients"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        patient_names_data = cur.fetchall()

        query3 = "SELECT test_id, test_name from Tests"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        tests_data = cur.fetchall()


        # render test records page passing our query data to the test records template
        return render_template("test_records.j2", data=data, patient_names=patient_names_data, tests_names=tests_data)

@app.route("/testrecords/search", methods=['GET'])
def searchTestRecord():
    fname = request.args.get('patient_fname', None)
    lname = request.args.get('patient_lname', None)
    query = "SELECT Test_Records.record_id, CONCAT(Patients.first_name, ' ', Patients.last_name) as patient_name, Patients.patient_id, Tests.test_name, Test_Records.requested_date, (CASE WHEN Test_Records.completed = 1 THEN 'YES' ELSE 'NO' END) AS completed, IFNULL(Test_Records.completed_date, '') AS completed_date, Test_Records.priority FROM Test_Records INNER JOIN Patients ON Test_Records.patient_id = Patients.patient_id INNER JOIN Tests ON Test_Records.test_id = Tests.test_id WHERE Patients.first_name = '%s' AND Patients.last_name = '%s' ORDER BY Test_Records.completed, Test_Records.priority, Test_Records.requested_date ASC;" % (fname, lname)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    
    # if cur.rowcount == 0:
    #     do something
    
    return render_template("search_test_record.j2", data=data, fname=fname, lname=lname)

# ------------- Test Records Entity END --------------------- #

# ------------- Equipment Entity ---------------------------- #

@app.route("/equipment", methods=['GET', 'POST'])
def equipment():
    # Separate out the request methods, in this case this is for a POST
    # insert equipment into the equipment entity
    if request.method == "POST":
        # fire off if user presses the Add Equipment button
        if request.form.get("Add_Equipment"):
            # grab user form inputs
            equip_name = request.form["equip_name"]
            availability = request.form["availability"]
            calibration_date = request.form["calibration_date"]
            next_maintenance = request.form["next_maintenance"]

            # perform insert operation
            query = "INSERT INTO Equipment (equip_name, availability, calibration_date, next_maintenance) VALUES(%s,%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (equip_name, availability, calibration_date, next_maintenance))
            mysql.connection.commit()

            # redirect back to equipment page
            return redirect("/equipment")

    # Grab equipment data so we send it to our template to display
    else:
        # mySQL query to grab all the equipment in equipment table
        query = "SELECT equip_id,equip_name,(CASE WHEN availability = 1 THEN 'Yes' ELSE 'No' END) AS availability,calibration_date,next_maintenance FROM Equipment GROUP BY equip_id ORDER BY equip_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render equipment page passing our query data to the equipment template
        return render_template("equipment.j2", data=data)

# Delete an equipment
@app.route("/delete_equip/<int:equip_id>")
def delete_equip(equip_id):
    # mySQL query to delete the patient with our passed patient_id
    query = "DELETE FROM Equipment WHERE equip_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (equip_id,))
    mysql.connection.commit()

    # redirect back to patients page
    return redirect("/equipment")

# Edit an equipment
@app.route("/edit_equip/<int:equip_id>", methods=["POST", "GET"])
def edit_equip(equip_id):
    if request.method == "GET":
        # mySQL query to grab the info of the patient with our passed id
        query = "SELECT Equipment.equip_id, Equipment.equip_name, (CASE WHEN Equipment.availability = 1 THEN 'Yes' ELSE 'No' END) AS availability, Equipment.calibration_date, Equipment.next_maintenance FROM Equipment WHERE equip_id = %s" % (equip_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_patients page passing our query data to the edit_patient template
        return render_template("edit_equipment.j2", data=data)
    
    if request.method == "POST":
        # fire off if user clicks the 'Edit Patient' button
        if request.form.get("Edit_Equipment"):
            equip_id = request.form["equip_id"]
            equip_name = request.form["equip_name"]
            availability = request.form["availability"]
            calibration_date = request.form["calibration_date"]
            next_maintenance = request.form["next_maintenance"]
            
            query = "UPDATE Equipment SET Equipment.equip_name = %s, Equipment.availability = %s, Equipment.calibration_date = %s, Equipment.next_maintenance = %s WHERE Equipment.equip_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (equip_name, availability, calibration_date, next_maintenance, equip_id))
            mysql.connection.commit()

            return redirect("/equipment")

# ------------- Equipment Entity END ------------------------- #

# ------------- Tests_Equipment Entity ----------------------- #

@app.route("/testsequipment", methods=['GET', 'POST'])
def testsequipment():
    # Separate out the request methods, in this case this is for a POST
    # insert a tests equipment into the testsequipment entity
    if request.method == "POST":
        # fire off if user presses the Add TestsEquipment button
        if request.form.get("Add_TestsEquipment"):
            # grab user form inputs
            test_id = request.form["test_name"]
            equip_id = request.form["equip_name"]
           

            # perform insert operation
            query = "INSERT INTO Tests_Equipment (test_id, equip_id) VALUES(%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (test_id, equip_id))
            mysql.connection.commit()

            # redirect back to testsequipment page
            return redirect("/testsequipment")

    # Grab testsequipment data so we can send it to our template to display
    else:
        # mySQL query to grab all the rows in tests equipment
        query = "SELECT Tests_Equipment.test_equip_id, Tests.test_name, Equipment.equip_name FROM Tests_Equipment INNER JOIN Tests ON Tests_Equipment.test_id = Tests.test_id INNER JOIN Equipment ON Tests_Equipment.equip_id = Equipment.equip_id ORDER BY Tests_Equipment.test_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab all the test names in departments
        query2 = "SELECT test_id, test_name from Tests"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        test_data = cur.fetchall()

        # mySQL query to grab all the test names in departments
        query3 = "SELECT equip_id, equip_name from Equipment"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        equipment_data = cur.fetchall()

        # render tests_equipment page passing our query data to the tests_equipment template
        return render_template("tests_equipment.j2", data=data, tests=test_data, equipment=equipment_data)

# Delete a test_equipment
@app.route("/delete_test_equip/<int:test_equip_id>")
def delete_test_equip(test_equip_id):
    # mySQL query to delete the patient with our passed patient_id
    query = "DELETE FROM Tests_Equipment WHERE test_equip_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (test_equip_id,))
    mysql.connection.commit()

    # redirect back to patients page
    return redirect("/testsequipment")
# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=12513, debug=True)
