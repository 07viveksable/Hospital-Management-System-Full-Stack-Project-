CREATE DATABASE hospital1_db;

USE hospital1_db;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    blood_group VARCHAR(10),
    admitted_date DATE,
    discharge_date DATE DEFAULT NULL,
    last_appointment DATETIME,
    diagnosis TEXT,
    payment_history TEXT,
    photo VARCHAR(255)
);
USE hospital_db;

INSERT INTO patients (name, age, blood_group, admitted_date, discharge_date, last_appointment, diagnosis, payment_history, photo,)
VALUES
('Aarav Sharma', 32, 'A+', '2025-09-10', '2025-09-20', '2025-10-10 10:30:00', 'Typhoid Fever', 'Paid ₹12,000 on discharge', 'images/aarav.jpg'),
('Priya Mehta', 28, 'B+', '2025-09-15', '2025-09-25', '2025-10-05 15:00:00', 'Migraine', 'Paid ₹8,500 via UPI', 'images/priya.jpg'),
('Rohit Verma', 45, 'O-', '2025-08-20', '2025-09-05', '2025-09-30 11:00:00', 'Diabetes Type 2', 'Pending ₹2,000', 'images/rohit.jpg'),
('Sneha Patel', 37, 'AB+', '2025-09-01', '2025-09-12', '2025-10-01 09:00:00', 'Hypertension', 'Paid ₹10,000 (cash)', 'images/sneha.jpg'),
('Vikram Singh', 50, 'A-', '2025-07-22', '2025-08-01', '2025-09-20 13:45:00', 'Heart Disease', 'Paid ₹30,000 via card', 'images/vikram.jpg'),
('Neha Kapoor', 26, 'B-', '2025-10-02', NULL, '2025-10-12 14:00:00', 'Viral Fever', 'Advance ₹3,000 paid', 'images/neha.jpg'),
('Ramesh Gupta', 60, 'O+', '2025-09-18', '2025-09-28', '2025-10-08 10:15:00', 'Arthritis', 'Paid ₹15,000 via cheque', 'images/ramesh.jpg'),
('Divya Joshi', 34, 'A+', '2025-08-25', '2025-09-05', '2025-09-25 16:30:00', 'Asthma', 'Paid ₹9,200 (online)', 'images/divya.jpg'),
('Manoj Tiwari', 41, 'B+', '2025-09-10', '2025-09-20', '2025-10-10 11:45:00', 'Kidney Stones', 'Paid ₹20,000 (card)', 'images/manoj.jpg'),
('Kavita Nair', 29, 'AB-', '2025-10-01', NULL, '2025-10-14 17:00:00', 'Allergic Rhinitis', 'Paid ₹5,000 (pending lab test)', 'images/kavita.jpg');


ALTER TABLE patients

ADD COLUMN address VARCHAR(255) AFTER mobile_no;

UPDATE patients SET mobile_no = '9876543210', address = '123 MG Road, Mumbai' WHERE id = 1;
UPDATE patients SET mobile_no = '9123456780', address = '45 Nehru Nagar, Delhi' WHERE id = 2;
UPDATE patients SET mobile_no = '9823014567', address = '56 Park Street, Kolkata' WHERE id = 3;
UPDATE patients SET mobile_no = '9988776655', address = '78 Gandhi Road, Chennai' WHERE id = 4;
UPDATE patients SET mobile_no = '9090909090', address = '21 Civil Lines, Lucknow' WHERE id = 5;
UPDATE patients SET mobile_no = '9812345678', address = '15 Brigade Road, Bengaluru' WHERE id = 6;
UPDATE patients SET mobile_no = '9977554433', address = '67 Residency Area, Indore' WHERE id = 7;
UPDATE patients SET mobile_no = '9765432109', address = '12 Model Town, Chandigarh' WHERE id = 8;
UPDATE patients SET mobile_no = '9356789012', address = '89 FC Road, Pune' WHERE id = 9;
UPDATE patients SET mobile_no = '9001122334', address = '34 Banjara Hills, Hyderabad' WHERE id = 10;

SELECT id, name, mobile_no, address FROM patients;
ALTER TABLE patients DROP COLUMN mobile_no;
ALTER TABLE patients DROP COLUMN address;
SHOW COLUMNS FROM patients;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
INSERT INTO users (username, password) VALUES
('vivek01', 'pass123'),
('ishwar', 'secure456'),
('shlokh', 'mypassword'),
('sneha04', 'abc12345'),
('kiran05', 'password1'),
('rohan06', 'qwerty123'),
('meera07', 'hello2025'),
('arjun08', 'pass9876'),
('tina09', 'welcome09'),
('raj10', 'admin2025');

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);
INSERT INTO users (username, password, role) VALUES
('vivek', 'pass123', 'owner'),
('ishwar', 'pass123', 'doctor'),
('shlok', 'pass123', 'doctor'),
('pradnya', 'pass123', 'doctor'),
('pragati', 'pass123', 'doctor'),
('shital', 'pass123', 'doctor'),
('vaishnavi', 'pass123', 'doctor'),
('kunal', 'pass123', 'doctor'),
('abhi', 'pass123', 'doctor'),
('harshad', 'pass123', 'doctor');

DROP TABLE IF EXISTS appointments;
select * from appointments;

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);
-- Insert 5 sample appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES
(1, 1, '2025-10-16 10:00:00', 'Routine checkup'),
(2, 2, '2025-10-17 14:00:00', 'Allergy follow-up'),
(3, 3, '2025-10-18 09:30:00', 'Follow-up for lab results'),
(4, 4, '2025-10-19 11:00:00', 'General consultation'),
(1, 5, '2025-10-20 15:00:00', 'Vaccination schedule review');

);
INSERT INTO prescriptions (patient_id, date, prescription_details) VALUES
(1, '2025-10-16', 'Paracetamol 500mg twice a day for 5 days'),
(2, '2025-10-17', 'Cetirizine 10mg once daily for 7 days'),
(1, '2025-10-18', 'Amoxicillin 500mg three times daily for 7 days'),
(2, '2025-10-19', 'Salbutamol inhaler as needed for wheezing'),
(1, '2025-10-20', 'Vitamin D 1000 IU daily for 30 days');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes)
VALUES (1, 2, '2025-10-20 10:00:00', 'Follow-up visit');

ALTER TABLE prescriptions MODIFY COLUMN doctor_id INT NULL;

ALTER TABLE prescriptions MODIFY COLUMN doctor_id INT NULL;
ALTER TABLE prescriptions
ADD COLUMN doctor_id INT AFTER patient_id;
DROP TABLE IF EXISTS prescriptions ;
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,  -- new column for the prescribing doctor
    date DATE NOT NULL,
    prescription_details TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)  -- link to doctors table
);




CREATE TABLE IF NOT EXISTS discharge_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    discharge_date DATE NOT NULL,
    total_bill DECIMAL(10,2) NOT NULL,
    summary_notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
CREATE TABLE IF NOT EXISTS discharge_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    discharge_date DATE NOT NULL,
    total_bill DECIMAL(10,2) NOT NULL,
    summary_notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);


