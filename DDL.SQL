SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

----- Create Tables -----

-- Patients table
CREATE OR REPLACE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    phone CHAR(12) NOT NULL,
    email VARCHAR(100) NOT NULL,
    street1 VARCHAR(100) NOT NULL,
    street2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    zip CHAR(5)
);

-- Departments table
CREATE OR REPLACE TABLE Departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    total_tests INT NOT NULL DEFAULT 0
);

-- Tests table
CREATE OR REPLACE TABLE Tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(50) NOT NULL,
    test_desc VARCHAR(255) NOT NULL,
    dept_id INT,
    CONSTRAINT Tests_ibfk_1
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Test_Records table
CREATE OR REPLACE TABLE Test_Records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    test_id INT,
    requested_date DATE NOT NULL,
    completed BOOLEAN DEFAULT 0,
    completed_date DATE,
    priority INT NOT NULL,
    CONSTRAINT Test_Records_ibfk_1
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT Test_Records_ibfk_2
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Equipment table
CREATE OR REPLACE TABLE Equipment (
    equip_id INT AUTO_INCREMENT PRIMARY KEY,
    equip_name VARCHAR(50) NOT NULL,
    availability BOOLEAN DEFAULT 1,
    calibration_date DATE,
    next_maintenance DATE
);

-- Tests_Equipment intersection table
CREATE OR REPLACE TABLE Tests_Equipment (
    test_equip_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    equip_id INT,
    CONSTRAINT Tests_Equipment_ibfk_1
    FOREIGN KEY (test_id) REFERENCES Tests(test_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Tests_Equipment_ibfk_2
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

----- Insert data -----

-- Patients table
INSERT INTO Patients (patient_id, first_name, last_name, birthday, phone, email, street1, street2, city, zip)
VALUES  (1, 'Elon', 'Musk', '1971-09-28', '415-222-9670', 'E.Musk@twitter.com', '1355 Market St', 'Suite 900', 'San Francisco', 94103),
        (2, 'Jeff', 'Bezos', '1964-01-12', '206-266-1000', 'J.Bezos@amazon.com', '440 Terry Ave N', NULL, 'Seattle', 98109),
        (3, 'Mark', 'Zuckerberg', '1984-05-14', '650-853-1300', 'M.Zuckerberg@meta.com', '1 Hacker Way', NULL, 'Palo Alto', 94025),
        (4, 'Susan', 'Wojcicki', '1968-07-15', '650-253-0000', 'S.Wojcicki@youtube.com', '901 Cherry Ave', NULL, 'San Bruno', 94066),
        (5, 'Safra', 'Catz', '1961-12-01', '800-392-2999', 'S.Catz@oracle.com', '2300 Oracle Wy', NULL, 'Austin', 78741);

-- Test_Records table
INSERT INTO Test_Records (patient_id, test_id, requested_date, completed, completed_date, priority)
VALUES  (3, 4, '2023-01-30', 1, '2023-01-31', 1),
        (1, 5, '2023-01-30', 1, '2023-02-01', 2),
        (2, 1, '2023-02-01', 1, '2023-02-03', 3),
        (5, 3, '2023-02-05', 1, '2023-02-07', 4),
        (4, 2, '2023-05-01', 0, NULL, 1);

-- Tests table
INSERT INTO Tests (dept_id, test_name, test_desc)
VALUES  (1, 'X-Ray', 'x-ray image'),
        (1, 'MRI', 'mri image'),
        (1, 'Ultrasound', 'ultrasound image'),
        (2, 'Blood-Metabolic', 'Metabolic panel'),
        (3, 'Urine', 'Dipstick, microscopy'),
        (3, 'Culture', 'cell growth, counting');

-- Departments table
-- NOTE: possible query to count total number of tests in Test_Records table to use to update 'total_tests'
INSERT INTO Departments (dept_name, total_tests)
VALUES  ('Radiology', 3),
        ('Immunology', 3),
        ('Microbiology', 2);

-- Equipment table
INSERT INTO Equipment (equip_name, availability, calibration_date, next_maintenance)
VALUES  ('Philips all-in-1 imager', 1, '2024-01-15', '2025-05-03'),
        ('B/U analyzer', 0, '2023-05-10', '2024-03-17'),
        ('cell counter', 0, '2023-07-27', '2023-09-05'),
        ('GE wonder tester 5000', 1, '2023-10-24', '2023-12-21');

-- Tests_Equipment
INSERT INTO Tests_Equipment (test_id, equip_id)
VALUES  (1, 1),
        (1, 2),
        (3, 3),
        (3, 4),
        (2, 4);

-- Check tables
DESCRIBE Patients;
DESCRIBE Departments;
DESCRIBE Test_Records;
DESCRIBE Tests;
DESCRIBE Equipment;
DESCRIBE Tests_Equipment;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;