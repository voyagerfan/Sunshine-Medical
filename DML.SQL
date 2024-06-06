-- Patient Page --

-- Display all patient information to populate Patient page
SELECT  * 
FROM Patients;

-- Add new patient
INSERT INTO Patients (first_name, last_name, birthday, phone, email, street1, street2, city, zip)
VALUES (:first_name_input, :last_name_input, :birthday_input, :phone_input, :email_input, :street1_input, :street2_input, :city_input, :zip_input)

-- Update patient information
UPDATE Patients
SET
    first_name = :first_name_input,
    last_name = :last_name_input,
    birthday = :birthday_input,
    phone = :phone_input,
    email = :email_input,
    street1 = :street1_input,
    street2 = :street2_input,
    city = :city_input,
    zip = :zip_input
WHERE patient_id = :patient_id_selected     -- patient_id_selected from UI table

-- Delete patient information
DELETE FROM Patients WHERE id = :patient_id_selected

-- Test Records Page --

-- Display Test Record information
SELECT  Test_Records.record_id,
        CONCAT(Patients.first_name, ' ', Patients.last_name) as patient_name,
        Patient.patient_id,
        Tests.test_name, Test_Records.requested_date, 
        (CASE WHEN Test_Records.completed = 1 THEN 'YES' ELSE 'NO' END) AS completed,
        IFNULL(Test_Records.completed_date, '') AS completed_date, Test_Records.priority
FROM Test_Records
INNER JOIN Patients ON Test_Records.patient_id = Patients.patient_id
INNER JOIN Tests ON Test_Records.test_id = Tests.test_id
ORDER BY Test_Records.completed, Test_Records.priority, Test_Records.requested_date ASC;

-- Display Test Record by Patient
SELECT  Test_Records.record_id,
        CONCAT(Patients.first_name, ' ', Patients.last_name) as patient_name,
        Patient.patient_id,
        Tests.test_name, Test_Records.requested_date, 
        (CASE WHEN Test_Records.completed = 1 THEN 'YES' ELSE 'NO' END) AS completed,
        IFNULL(Test_Records.completed_date, '') AS completed_date, Test_Records.priority
FROM Test_Records
INNER JOIN Patients ON Test_Records.patient_id = Patients.patient_id
INNER JOIN Tests ON Test_Records.test_id = Tests.test_id
WHERE Patients.first_name = :patient_fname_input AND Patients.last_name = :patient_lname_input
ORDER BY Test_Records.completed, Test_Records.priority, Test_Records.requested_date ASC;

-- SELECT patient names for 'Patient Name' dropdown when adding new Test Record
SELECT  patient_id,
        CONCAT(last_name, ', ', first_name) as name
FROM    Patients;

-- SELECT test names for 'Test Name' dropdown when adding new Test Record
SELECT  test_id,
        test_name
FROM    Tests;

-- Add new test record
INSERT INTO Test_Records (patient_id, test_id, requested_date, completed, priority)
VALUES (:patient_id_input, :test_id_input, :requested_date_input, :priority)

-- -- Update test record
UPDATE Test_Records
SET
    test_id = :test_id_input,
    requested_date = :requested_date_input,
    completed = :completed_input,
    completed_date = :completed_date_input,
    priority = :priority_input,
WHERE record_id = :record_id_selected;

-- -- Delete patient information
DELETE FROM Test_Records WHERE test_id = :test_id_selected;

-- Tests Page

-- Display Test information
SELECT  Tests.test_id,
        Tests.test_name,
        Tests.test_desc,
        Departments.dept_name
FROM Tests
INNER JOIN Departments ON Tests.dept_id = Departments.dept_id
ORDER BY Tests.test_id ASC;

-- Display Test information for Test being edited
SELECT  Tests.test_id,
        Tests.test_name,
        Tests.test_desc,
        Departments.dept_name
FROM Tests
INNER JOIN Departments ON Tests.dept_id = Departments.dept_id
WHERE test_id = :test_id_selected;

-- SELECT department names for 'Department Name' dropdown for new test insert
SELECT  dept_id,
        dept_name
FROM Departments;

-- Add new test
INSERT INTO Tests (test_name, test_desc, dept_id)
VALUES (
    (SELECT dept_id FROM Departments WHERE dept_name = :dept_name_input),
    :test_name_input,
    :test_desc_input
);

-- Update test
UPDATE Tests
SET
    dept_id = (SELECT dept_id FROM Departments WHERE dept_name = :dept_name_selected)
    test_name = :test_name_input,
    test_desc = :test_desc_input
WHERE test_id = :test_id_selected;

-- Delete test
DELETE FROM Tests WHERE test_id = :test_id_selected;

-- Department Page --

-- Display department information
-- Total tests calculated from counting number of tests on Test_Records
SELECT  Departments.dept_id, 
        Departments.dept_name,
        SUM(CASE WHEN Test_Records.completed = 1 THEN 0 ELSE 1 END) AS total_active_tests
FROM Departments
INNER JOIN Tests ON Departments.dept_id = Tests.dept_id
INNER JOIN Test_Records ON Tests.test_id = Test_Records.test_id
GROUP BY Departments.dept_id
ORDER BY Departments.dept_id;

-- Add new department
INSERT INTO Departments (dept_name, total_tests)
VALUES  (:dept_name_input, :total_tests_input)

-- Equipment Page --
-- Display equipment information
SELECT  equip_id,
        equip_name,
        (CASE WHEN availability = 1 THEN 'Yes' ELSE 'No' END) AS availability,
        calibration_date,
        next_maintenance
FROM    Equipment
GROUP BY equip_id
ORDER BY equip_id;

-- Display selected equipment information when editing
SELECT  equip_id,
        equip_name,
        (CASE WHEN availability = 1 THEN 'Yes' ELSE 'No' END) AS availability,
        calibration_date,
        next_maintenance
FROM    Equipment
WHERE   equip_id = :equip_id_selected;

-- Add new equipment
INSERT INTO Equipment (equip_name, availability, calibration_date, next_maintenance)
VALUES  (:equip_name_input, :availability_input,  :calibration_date_input, :next_maintenance_input);

-- Updated selected equipment
UPDATE Equipment
SET
    equip_name = :equip_name_input,
    availability = :availability_input,
    calibration_date = :calibration_date_input
    next_maintenance = :next_maintenance_input,
WHERE equip_id = :equip_id_input;

-- Delete equipment
DELETE FROM Equipment WHERE equip_id = :equip_id_selected;

Tests_Equipment Page (Intersection table)

-- Display all
SELECT  Tests_Equipment.test_id,
        Tests.test_name,
        Tests_Equipment.equip_id,
        Equipment.equip_name
FROM Tests_Equipment
INNER JOIN Tests ON Tests_Equipment.test_id = Tests.test_id
INNER JOIN Equipment ON Tests_Equipment.equip_id = Equipment.equip_id
ORDER BY Tests_Equipment.test_id;

-- SELECT test ID's and names for 'Test Name' dropdown when adding new Tests_Equipment
SELECT  test_id,
        test_name
FROM    Tests;

-- SELECT equipment ID's and names for 'Equipment Name' dropdown when adding new Tests_Equipment
SELECT  equip_id,
        equip_name
FROM    Equipment;

-- Insert new test-equipment relationship
INSERT INTO Tests_Equipment (test_id, equip_id)
VALUES (:test_id_input, :equip_id_input); 

-- Update test_equipment relationship
SET
    test_id = (SELECT test_id FROM Tests WHERE test_name = :test_name_input),
    equip_id = (SELECT equip_id FROM Equipment WHERE equip_name = :equip_name_input)
WHERE test_id = :test_id_input

-- Delete test_equipment row
DELETE FROM Tests_Equipment 
WHERE   test_id = (SELECT test_id FROM Tests WHERE test_name = :test_name_input) AND 
        equip_id = (SELECT equip_id FROM Equipment WHERE equip_name = :equip_name_input);