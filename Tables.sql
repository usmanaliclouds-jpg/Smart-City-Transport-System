 -- 1. Station
CREATE TABLE Station (
    stationID NUMBER PRIMARY KEY,
    stationName VARCHAR2(100),
    location VARCHAR2(100),
    platform VARCHAR2(50)
);
--2 Passenger
CREATE TABLE Passenger (
    passengerID NUMBER PRIMARY KEY,
    passengerName VARCHAR2(100),
    passengerEmail VARCHAR2(100),
    phoneNumber VARCHAR2(20),
    DOB DATE,
    age NUMBER
);

-- 3. Route
CREATE TABLE Route (
    routeID NUMBER PRIMARY KEY,
    routeName VARCHAR2(100),
    distance NUMBER,
    startStationID NUMBER REFERENCES Station(stationID),
    endStationID NUMBER REFERENCES Station(stationID)
);

-- 4. Vehicle (Superclass)
CREATE TABLE Vehicle (
    vehicleID NUMBER PRIMARY KEY,
    capacity NUMBER,
    model VARCHAR2(50)
);

-- 5. Bus (Subclass of Vehicle)
CREATE TABLE Bus (
    vehicleID NUMBER PRIMARY KEY REFERENCES Vehicle(vehicleID),
    busNumber VARCHAR2(50),
    busType VARCHAR2(50)
);

-- 6. Train (Subclass of Vehicle)
CREATE TABLE Train (
    vehicleID NUMBER PRIMARY KEY REFERENCES Vehicle(vehicleID),
    trainNumber VARCHAR2(50),
    numberOfCoaches NUMBER
);

-- 7. Driver
CREATE TABLE Driver (
    driverID NUMBER PRIMARY KEY,
    driverName VARCHAR2(100),
    licenseNumber VARCHAR2(50) UNIQUE,
    experience NUMBER
);

-- 8. Schedule
CREATE TABLE Schedule (
    scheduleID NUMBER PRIMARY KEY,
    arrivalTime TIMESTAMP,
    departureTime TIMESTAMP,
    frequency VARCHAR2(50),
    routeID NUMBER REFERENCES Route(routeID),
    vehicleID NUMBER REFERENCES Vehicle(vehicleID),
    driverID NUMBER REFERENCES Driver(driverID)
);

-- 9. Ticket
CREATE TABLE Ticket (
    ticketNumber NUMBER PRIMARY KEY,
    price NUMBER(10, 2),
    type VARCHAR2(50),
    issueDate DATE,
    passengerID NUMBER REFERENCES Passenger(passengerID),
    scheduleID NUMBER REFERENCES Schedule(scheduleID)
);





INSERT ALL
    INTO Station VALUES (1, 'Faisalabad Central', 'City Center', 'Platform 1')
    INTO Station VALUES (2, 'Lahore Junction', 'Main Boulevard', 'Platform 2')
    INTO Station VALUES (3, 'Islamabad Metro', 'Blue Area', 'Platform 3')
    INTO Station VALUES (4, 'Karachi Terminal', 'Saddar', 'Platform 1')
    INTO Station VALUES (5, 'Multan Station', 'Cantt Area', 'Platform 2')
    INTO Station VALUES (6, 'Rawalpindi Hub', 'Committee Chowk', 'Platform 1')
    INTO Station VALUES (7, 'Sialkot Stop', 'Civil Lines', 'Platform 3')
    INTO Station VALUES (8, 'Gujranwala Point', 'GT Road', 'Platform 2')
    INTO Station VALUES (9, 'Peshawar Central', 'University Road', 'Platform 1')
    INTO Station VALUES (10, 'Quetta Station', 'Jinnah Road', 'Platform 2')
SELECT * FROM dual;




-- 1. Station (10 records)
INSERT ALL
    INTO Station VALUES (1, 'Faisalabad Central', 'City Center', 'Platform 1')
    INTO Station VALUES (2, 'Lahore Junction', 'Main Boulevard', 'Platform 2')
    INTO Station VALUES (3, 'Islamabad Metro', 'Blue Area', 'Platform 3')
    INTO Station VALUES (4, 'Karachi Terminal', 'Saddar', 'Platform 1')
    INTO Station VALUES (5, 'Multan Station', 'Cantt Area', 'Platform 2')
    INTO Station VALUES (6, 'Rawalpindi Hub', 'Committee Chowk', 'Platform 1')
    INTO Station VALUES (7, 'Sialkot Stop', 'Civil Lines', 'Platform 3')
    INTO Station VALUES (8, 'Gujranwala Point', 'GT Road', 'Platform 2')
    INTO Station VALUES (9, 'Peshawar Central', 'University Road', 'Platform 1')
    INTO Station VALUES (10, 'Quetta Station', 'Jinnah Road', 'Platform 2')
SELECT * FROM dual;



-- 2. Passenger (15 records)
INSERT ALL
    INTO Passenger VALUES (1, 'Ali Ahmed', 'ali@email.com', '03001234567', TO_DATE('1995-03-15', 'YYYY-MM-DD'), 29)
    INTO Passenger VALUES (2, 'Fatima Khan', 'fatima@email.com', '03011234568', TO_DATE('1998-07-22', 'YYYY-MM-DD'), 26)
    INTO Passenger VALUES (3, 'Hassan Raza', 'hassan@email.com', '03021234569', TO_DATE('1990-11-10', 'YYYY-MM-DD'), 34)
    INTO Passenger VALUES (4, 'Ayesha Malik', 'ayesha@email.com', '03031234570', TO_DATE('2000-05-18', 'YYYY-MM-DD'), 24)
    INTO Passenger VALUES (5, 'Bilal Sheikh', 'bilal@email.com', '03041234571', TO_DATE('1985-09-25', 'YYYY-MM-DD'), 39)
    INTO Passenger VALUES (6, 'Zainab Ali', 'zainab@email.com', '03051234572', TO_DATE('1992-01-30', 'YYYY-MM-DD'), 32)
    INTO Passenger VALUES (7, 'Usman Tariq', 'usman@email.com', '03061234573', TO_DATE('1997-12-05', 'YYYY-MM-DD'), 27)
    INTO Passenger VALUES (8, 'Maryam Saeed', 'maryam@email.com', '03071234574', TO_DATE('2001-08-14', 'YYYY-MM-DD'), 23)
    INTO Passenger VALUES (9, 'Ahmed Iqbal', 'ahmed@email.com', '03081234575', TO_DATE('1988-04-20', 'YYYY-MM-DD'), 36)
    INTO Passenger VALUES (10, 'Sara Hussain', 'sara@email.com', '03091234576', TO_DATE('1999-10-12', 'YYYY-MM-DD'), 25)
    INTO Passenger VALUES (11, 'Kamran Aslam', 'kamran@email.com', '03101234577', TO_DATE('1993-06-08', 'YYYY-MM-DD'), 31)
    INTO Passenger VALUES (12, 'Hina Butt', 'hina@email.com', '03111234578', TO_DATE('1996-02-28', 'YYYY-MM-DD'), 28)
    INTO Passenger VALUES (13, 'Fahad Malik', 'fahad@email.com', '03121234579', TO_DATE('1991-09-17', 'YYYY-MM-DD'), 33)
    INTO Passenger VALUES (14, 'Nida Abbas', 'nida@email.com', '03131234580', TO_DATE('2002-03-22', 'YYYY-MM-DD'), 22)
    INTO Passenger VALUES (15, 'Imran Shah', 'imran@email.com', '03141234581', TO_DATE('1987-11-09', 'YYYY-MM-DD'), 37)
SELECT * FROM dual;

-- 3. Route (8 records)
INSERT ALL
    INTO Route VALUES (1, 'Faisalabad-Lahore Express', 120, 1, 2)
    INTO Route VALUES (2, 'Lahore-Islamabad Highway', 375, 2, 3)
    INTO Route VALUES (3, 'Islamabad-Rawalpindi Local', 15, 3, 6)
    INTO Route VALUES (4, 'Karachi-Multan Route', 850, 4, 5)
    INTO Route VALUES (5, 'Faisalabad-Sialkot Link', 95, 1, 7)
    INTO Route VALUES (6, 'Gujranwala-Lahore Circle', 70, 8, 2)
    INTO Route VALUES (7, 'Peshawar-Islamabad Express', 180, 9, 3)
    INTO Route VALUES (8, 'Quetta-Multan Long Route', 950, 10, 5)
SELECT * FROM dual;

-- 4. Vehicle (12 records)
INSERT ALL
    INTO Vehicle VALUES (1, 50, 'Volvo 9400')
    INTO Vehicle VALUES (2, 45, 'Mercedes Benz O500')
    INTO Vehicle VALUES (3, 300, 'Metro Train M1')
    INTO Vehicle VALUES (4, 280, 'Metro Train M2')
    INTO Vehicle VALUES (5, 42, 'Isuzu Turbo')
    INTO Vehicle VALUES (6, 55, 'Hino RK')
    INTO Vehicle VALUES (7, 320, 'Siemens Metro')
    INTO Vehicle VALUES (8, 48, 'Daewoo Express')
    INTO Vehicle VALUES (9, 350, 'China Railway CRH')
    INTO Vehicle VALUES (10, 40, 'Toyota Coaster')
    INTO Vehicle VALUES (11, 290, 'Hyundai Rotem')
    INTO Vehicle VALUES (12, 52, 'Yutong ZK6127')
SELECT * FROM dual;

-- 5. Bus (7 records)
INSERT ALL
    INTO Bus VALUES (1, 'FSD-LHE-001', 'AC Deluxe')
    INTO Bus VALUES (2, 'LHE-ISB-002', 'Business Class')
    INTO Bus VALUES (5, 'FSD-SKT-005', 'Economy')
    INTO Bus VALUES (6, 'GRW-LHE-006', 'AC Standard')
    INTO Bus VALUES (8, 'ISB-PSH-008', 'VIP')
    INTO Bus VALUES (10, 'LHE-MLT-010', 'Economy')
    INTO Bus VALUES (12, 'KHI-MLT-012', 'AC Deluxe')
SELECT * FROM dual;

-- 6. Train (5 records)
INSERT ALL
    INTO Train VALUES (3, 'MT-001', 6)
    INTO Train VALUES (4, 'MT-002', 5)
    INTO Train VALUES (7, 'SM-001', 8)
    INTO Train VALUES (9, 'CRH-001', 10)
    INTO Train VALUES (11, 'HR-001', 7)
SELECT * FROM dual;

-- 7. Driver (10 records)
INSERT ALL
    INTO Driver VALUES (1, 'Muhammad Akram', 'LIC-2015-001', 8)
    INTO Driver VALUES (2, 'Rashid Mahmood', 'LIC-2012-002', 12)
    INTO Driver VALUES (3, 'Tariq Jameel', 'LIC-2018-003', 6)
    INTO Driver VALUES (4, 'Naveed Akhtar', 'LIC-2010-004', 14)
    INTO Driver VALUES (5, 'Sajid Ali', 'LIC-2019-005', 5)
    INTO Driver VALUES (6, 'Yasir Hussain', 'LIC-2016-006', 8)
    INTO Driver VALUES (7, 'Khalid Mehmood', 'LIC-2013-007', 11)
    INTO Driver VALUES (8, 'Asif Rauf', 'LIC-2017-008', 7)
    INTO Driver VALUES (9, 'Shahid Iqbal', 'LIC-2011-009', 13)
    INTO Driver VALUES (10, 'Zahid Abbas', 'LIC-2020-010', 4)
SELECT * FROM dual;

-- 8. Schedule (12 records)
INSERT ALL
    INTO Schedule VALUES (1, TO_TIMESTAMP('2024-01-15 08:30:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 06:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 1, 1, 1)
    INTO Schedule VALUES (2, TO_TIMESTAMP('2024-01-15 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 08:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 2, 2, 2)
    INTO Schedule VALUES (3, TO_TIMESTAMP('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 09:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'Every 30 min', 3, 3, 3)
    INTO Schedule VALUES (4, TO_TIMESTAMP('2024-01-16 20:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-16 05:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Weekly', 4, 4, 4)
    INTO Schedule VALUES (5, TO_TIMESTAMP('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 5, 5, 5)
    INTO Schedule VALUES (6, TO_TIMESTAMP('2024-01-15 13:30:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 6, 6, 6)
    INTO Schedule VALUES (7, TO_TIMESTAMP('2024-01-15 11:30:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 08:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 7, 7, 7)
    INTO Schedule VALUES (8, TO_TIMESTAMP('2024-01-15 16:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 2, 8, 8)
    INTO Schedule VALUES (9, TO_TIMESTAMP('2024-01-17 06:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-16 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Twice a week', 8, 9, 9)
    INTO Schedule VALUES (10, TO_TIMESTAMP('2024-01-15 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Hourly', 3, 11, 3)
    INTO Schedule VALUES (11, TO_TIMESTAMP('2024-01-15 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 5, 10, 10)
    INTO Schedule VALUES (12, TO_TIMESTAMP('2024-01-15 17:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-01-15 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Daily', 1, 12, 1)
SELECT * FROM dual;

-- 9. Ticket (20 records)
INSERT ALL
    INTO Ticket VALUES (1, 500.00, 'Economy', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 1, 1)
    INTO Ticket VALUES (2, 1200.00, 'Business', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 2, 2)
    INTO Ticket VALUES (3, 100.00, 'Standard', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 3, 3)
    INTO Ticket VALUES (4, 3500.00, 'VIP', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 4, 4)
    INTO Ticket VALUES (5, 400.00, 'Economy', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 5, 5)
    INTO Ticket VALUES (6, 350.00, 'Standard', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 6, 6)
    INTO Ticket VALUES (7, 800.00, 'Business', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 7, 7)
    INTO Ticket VALUES (8, 1200.00, 'Business', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 8, 8)
    INTO Ticket VALUES (9, 4000.00, 'VIP', TO_DATE('2024-01-16', 'YYYY-MM-DD'), 9, 9)
    INTO Ticket VALUES (10, 100.00, 'Standard', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 10, 10)
    INTO Ticket VALUES (11, 450.00, 'Economy', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 11, 11)
    INTO Ticket VALUES (12, 550.00, 'Economy', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 12, 12)
    INTO Ticket VALUES (13, 500.00, 'Economy', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 13, 1)
    INTO Ticket VALUES (14, 1200.00, 'Business', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 14, 2)
    INTO Ticket VALUES (15, 100.00, 'Standard', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 15, 3)
    INTO Ticket VALUES (16, 800.00, 'Business', TO_DATE('2024-01-14', 'YYYY-MM-DD'), 1, 7)
    INTO Ticket VALUES (17, 350.00, 'Standard', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 2, 6)
    INTO Ticket VALUES (18, 400.00, 'Economy', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 3, 5)
    INTO Ticket VALUES (19, 3500.00, 'VIP', TO_DATE('2024-01-16', 'YYYY-MM-DD'), 4, 4)
    INTO Ticket VALUES (20, 100.00, 'Standard', TO_DATE('2024-01-15', 'YYYY-MM-DD'), 5, 10)
SELECT * FROM dual;




