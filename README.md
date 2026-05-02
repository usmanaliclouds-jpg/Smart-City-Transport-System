# 🚆 Smart City Transport System

This repository contains the Database Systems semester project developed by **Taheer Bin Hussain** (24F-0567) and **Usman Ali** (24F-0512). 

It is a full-stack transport management system designed for the Faisalabad region[cite: 73]. [cite_start]The core of this project is a robust **Oracle 11g** database, designed from the ground up to handle passenger ticketing, route management, vehicle scheduling, and administrative reporting[cite: 74].

## 🛠️ Tech Stack
* [cite_start]**Database:** Oracle 11g [cite: 60]
* **Backend API:** Python / Flask
* **Frontend:** Custom HTML, CSS, and JavaScript

## 📊 Database Concepts Implemented
[cite_start]To ensure strict data integrity and efficient querying, this system heavily utilizes advanced SQL and PL/SQL components as per our project requirements[cite: 140, 147]:
* [cite_start]**Complex Joins:** Used extensively to fetch interconnected data (e.g., linking passengers, tickets, routes, and schedules)[cite: 147].
* [cite_start]**Subqueries:** Implemented for advanced data filtering and validation[cite: 147].
* [cite_start]**Views:** Created (e.g., `ActiveRoutes_VW`) to simplify complex frontend reporting queries.
* [cite_start]**Automated Triggers:** Designed to handle background calculations automatically (e.g., calculating passenger age based on DOB).
* [cite_start]**Stored Procedures:** Used to securely handle data insertions (e.g., adding new passengers or schedules).

## 🗂️ Repository Contents
* `SmartCityTransport_connected.html`: The main frontend user interface.
* `app.py`: The Python/Flask API that connects the HTML frontend to the Oracle Database.
* `Database_Scripts.sql`: Contains all DDL and DML scripts, including table creation, views, triggers, and procedures.
* `24F-0567_24F-0512_EERD.pdf`: The Enhanced Entity-Relationship Diagram mapping out our database architecture.

## 🚀 How to Run Locally
*Note: Because this system relies on a local Oracle database, the frontend cannot be hosted purely on GitHub Pages. You must run the backend locally.*

1. **Set up the Database:**
   * Ensure Oracle 11g is installed and running on your machine.
   * Run the provided `.sql` scripts to generate the tables, triggers, and stored procedures.
2. **Start the API:**
   * Ensure Python and Flask are installed.
   * Update the database connection credentials inside `app.py`.
   * Run `python app.py` in your terminal. The server will start on `http://localhost:5000`.
3. **Launch the Application:**
   * Simply double-click `SmartCityTransport_connected.html` to open it in your web browser. 
   * The UI will now successfully communicate with your local Oracle Database.

## 👨‍💻 Authors
* **Taheer Bin Hussain** - [GitHub Profile](https://github.com/TaheerBinHussain) | [LinkedIn Profile](#)
* **Usman Ali** - [GitHub Profile](https://github.com/usmanaliclouds-jpg) | [LinkedIn Profile](#)

---
*Developed for the Database Lab Semester Project — May 2026*
