"""
=============================================================
  SMART CITY TRANSPORT SYSTEM — Flask Backend
  Connects to Oracle 11g via cx_Oracle
  All forms → Oracle DB (real INSERT/UPDATE/DELETE)
=============================================================
  HOW TO RUN:
  1. pip install flask cx_Oracle flask-cors
  2. Change DB_USER, DB_PASS, DB_DSN below to match yours
  3. python app.py
  4. Open browser: http://localhost:5000
=============================================================
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cx_Oracle
import os
from datetime import datetime, date

app = Flask(__name__, static_folder='.')
CORS(app)

# ─────────────────────────────────────────
#  DATABASE CONNECTION — CHANGE THESE
# ─────────────────────────────────────────
DB_USER = "24F-0512"          # your Oracle username (e.g. system or transport_admin)
DB_PASS = "1234"          # your Oracle password
DB_DSN  = "localhost/XE"    # host/service  (XE is default for Oracle 11g Express)
# If using port explicitly: cx_Oracle.makedsn("localhost", 1521, service_name="XE")

ADMIN_EMAIL = "admin@transport.com"
ADMIN_PASS  = "admin123"

def get_conn():
    """Get a fresh Oracle DB connection."""
    return cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)

def rows_to_dicts(cursor):
    """Convert cx_Oracle cursor rows → list of dicts."""
    cols = [col[0].lower() for col in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def serialize(obj):
    """Make Oracle types JSON-serializable."""
    if isinstance(obj, (datetime, date)):
        return str(obj)
    return obj

def clean_row(row):
    return {k: serialize(v) for k, v in row.items()}


# ═══════════════════════════════════════════
#  SERVE FRONTEND
# ═══════════════════════════════════════════
@app.route('/')
def index():
    return send_from_directory('.', 'SmartCityTransport_connected.html')


# ═══════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'passenger')

    if role == 'admin':
        if email == ADMIN_EMAIL and password == ADMIN_PASS:
            return jsonify({'success': True, 'role': 'admin', 'name': 'transport_admin', 'id': 0})
        return jsonify({'success': False, 'message': 'Invalid admin credentials'})

    # Passenger login — check email + phone as password (or stored pass field)
    try:
        conn = get_conn()
        cur = conn.cursor()
        # Using phoneNumber as password for simplicity (matches your DB)
        cur.execute("""
            SELECT passengerID, passengerName, passengerEmail, phoneNumber, age
            FROM Passenger
            WHERE passengerEmail = :email AND phoneNumber = :phone
        """, email=email, phone=password)
        row = cur.fetchone()
        cur.close(); conn.close()
        if row:
            return jsonify({'success': True, 'role': 'passenger',
                            'id': row[0], 'name': row[1], 'email': row[2]})
        return jsonify({'success': False, 'message': 'Invalid email or phone number'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/signup', methods=['POST'])
def signup():
    """Calls Add_Passenger procedure + trg_auto_calc_age trigger fires automatically."""
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Get next ID
        cur.execute("SELECT NVL(MAX(passengerID),0)+1 FROM Passenger")
        new_id = cur.fetchone()[0]

        # Call stored procedure — trg_auto_calc_age trigger will auto-calculate age
        cur.callproc('Add_Passenger', [
            new_id,
            data['name'],
            data['email'],
            data['phone'],
            datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            0  # age=0, trigger will override it automatically
        ])
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Account created! Login with your phone number as password.',
                        'id': new_id})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  PASSENGERS
# ═══════════════════════════════════════════
@app.route('/api/passengers', methods=['GET'])
def get_passengers():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT passengerID, passengerName, passengerEmail, phoneNumber, DOB, age FROM Passenger ORDER BY passengerID")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/passengers', methods=['POST'])
def add_passenger():
    """Admin: INSERT passenger via stored procedure."""
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT NVL(MAX(passengerID),0)+1 FROM Passenger")
        new_id = cur.fetchone()[0]

        cur.callproc('Add_Passenger', [
            new_id, data['name'], data['email'], data['phone'],
            datetime.strptime(data['dob'], '%Y-%m-%d').date(), 0
        ])
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': f'Passenger #{new_id} added successfully', 'id': new_id})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/passengers/<int:pid>', methods=['PUT'])
def update_passenger(pid):
    """Admin: UPDATE passenger record."""
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Passenger SET
                passengerName  = :name,
                passengerEmail = :email,
                phoneNumber    = :phone,
                DOB            = :dob
            WHERE passengerID = :pid
        """, name=data['name'], email=data['email'], phone=data['phone'],
             dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(), pid=pid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Passenger updated (trigger recalculates age)'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})

# add driver function newly added 
@app.route('/api/drivers', methods=['POST'])
def add_driver():
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT NVL(MAX(driverID),0)+1 FROM Driver")
        new_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO Driver (driverID, driverName, licenseNumber, experience)
            VALUES (:v_id, :v_name, :v_lic, :v_exp)
        """, v_id=new_id, v_name=data['name'], v_lic=data['license'], v_exp=data['experience'])
        
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Driver added successfully'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})
    



#newly added 


@app.route('/api/vehicles/<int:vid>', methods=['PUT'])
def update_vehicle(vid):
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Vehicle SET model = :v_mod, capacity = :v_cap
            WHERE vehicleID = :v_id
        """, v_mod=data['model'], v_cap=data['capacity'], v_id=vid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Vehicle updated'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/vehicles/<int:vid>', methods=['DELETE'])
def delete_vehicle(vid):
    try:
        conn = get_conn()
        cur = conn.cursor()
        # Note: You may need to delete linked schedules first if they exist
        cur.execute("DELETE FROM Vehicle WHERE vehicleID = :v_id", v_id=vid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Vehicle deleted'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})




@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():  # Fixed: Removed the character "积极"
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Get next available ID
        cur.execute("SELECT NVL(MAX(vehicleID),0)+1 FROM Vehicle")
        new_id = cur.fetchone()[0]
        
        # Use v_ prefixes for bind variables to avoid Oracle reserved word conflicts
        cur.execute("""
            INSERT INTO Vehicle (vehicleID, model, capacity) 
            VALUES (:v_id, :v_mod, :v_cap)
        """, v_id=new_id, v_mod=data['model'], v_cap=data['capacity'])
        
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Vehicle added successfully'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})
    
    
# newly added 

@app.route('/api/schedules', methods=['POST'])
def add_schedule():
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT NVL(MAX(scheduleID),0)+1 FROM Schedule")
        new_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO Schedule (scheduleID, routeID, vehicleID, driverID, departureTime, arrivalTime, frequency)
            VALUES (:v_id, :v_rid, :v_vid, :v_did, 
                    TO_DATE(:v_dep, 'YYYY-MM-DD HH24:MI'), 
                    TO_DATE(:v_arr, 'YYYY-MM-DD HH24:MI'), :v_freq)
        """, v_id=new_id, v_rid=data['routeID'], v_vid=data['vehicleID'], 
             v_did=data['driverID'], v_dep=data['departure'], v_arr=data['arrival'], v_freq=data['frequency'])
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Schedule created'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})




@app.route('/api/schedules/<int:sid>', methods=['PUT'])
def update_schedule(sid):
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Schedule SET
                routeID       = :v_rid,
                vehicleID     = :v_vid,
                driverID      = :v_did,
                departureTime = TO_DATE(:v_dep, 'YYYY-MM-DD HH24:MI'),
                arrivalTime   = TO_DATE(:v_arr, 'YYYY-MM-DD HH24:MI'),
                frequency     = :v_freq
            WHERE scheduleID = :v_id
        """, v_rid=data['routeID'], v_vid=data['vehicleID'], v_did=data['driverID'],
             v_dep=data['departure'], v_arr=data['arrival'], v_freq=data['frequency'],
             v_id=sid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Schedule updated'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/schedules/<int:sid>', methods=['DELETE'])
def delete_schedule(sid):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Schedule WHERE scheduleID = :v_id", v_id=sid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Schedule removed'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})



@app.route('/api/passengers/<int:pid>', methods=['DELETE'])
def delete_passenger(pid):
    """Admin: DELETE passenger (cascade delete tickets first)."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Ticket WHERE passengerID = :pid", pid=pid)
        cur.execute("DELETE FROM Passenger WHERE passengerID = :pid", pid=pid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': f'Passenger #{pid} and their tickets deleted'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  STATIONS
# ═══════════════════════════════════════════
@app.route('/api/stations', methods=['GET'])
def get_stations():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT stationID, stationName, location, platform FROM Station ORDER BY stationID")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════
@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Uses JOIN to get station names — matches your Queries.sql Join #1."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.routeID, r.routeName, r.distance,
                   s1.stationName AS startstation,
                   s2.stationName AS endstation,
                   r.startStationID, r.endStationID
            FROM Route r
            JOIN Station s1 ON r.startStationID = s1.stationID
            JOIN Station s2 ON r.endStationID   = s2.stationID
            ORDER BY r.routeID
        """)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/routes', methods=['POST'])
def add_route():
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT NVL(MAX(routeID),0)+1 FROM Route")
        new_id = cur.fetchone()[0]
        
        # Change the variable names here to avoid Oracle reserved word conflicts
        cur.execute("""
            INSERT INTO Route (routeID, routeName, distance, startStationID, endStationID)
            VALUES (:v_id, :v_name, :v_dist, :v_start, :v_end)
        """, v_id=new_id, 
             v_name=data['name'], 
             v_dist=data['distance'],
             v_start=data['startStationID'], 
             v_end=data['endStationID'])
             
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': f'Route #{new_id} added'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/routes/<int:rid>', methods=['DELETE'])
def delete_route(rid):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Route WHERE routeID = :rid", rid=rid)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': f'Route #{rid} deleted'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  VEHICLES
# ═══════════════════════════════════════════
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """LEFT JOIN Bus — matches your Queries.sql Join #4."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT v.vehicleID, v.model, v.capacity,
                   b.busNumber, b.busType,
                   t.trainNumber, t.numberOfCoaches,
                   CASE WHEN b.vehicleID IS NOT NULL THEN 'Bus'
                        WHEN t.vehicleID IS NOT NULL THEN 'Train'
                        ELSE 'Unknown' END AS vehicletype
            FROM Vehicle v
            LEFT JOIN Bus b   ON v.vehicleID = b.vehicleID
            LEFT JOIN Train t ON v.vehicleID = t.vehicleID
            ORDER BY v.vehicleID
        """)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  DRIVERS
# ═══════════════════════════════════════════
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT driverID, driverName, licenseNumber, experience FROM Driver ORDER BY driverID")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/drivers/<int:did>', methods=['PUT'])
def update_driver(did):
    data = request.json
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Driver SET driverName = :v_name, licenseNumber = :v_lic, experience = :v_exp
            WHERE driverID = :v_id
        """, v_name=data['name'], v_lic=data['license'], v_exp=data['experience'], v_id=did)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Driver updated'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/drivers/<int:did>', methods=['DELETE'])
def delete_driver(did):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Driver WHERE driverID = :v_id", v_id=did)
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': 'Driver deleted'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  SCHEDULES
# ═══════════════════════════════════════════
@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    """JOIN with Driver + Vehicle + Route — matches Join #3, #7."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.scheduleID, r.routeName,
                   TO_CHAR(s.departureTime,'YYYY-MM-DD HH24:MI') AS departuretime,
                   TO_CHAR(s.arrivalTime,  'YYYY-MM-DD HH24:MI') AS arrivaltime,
                   s.frequency, d.driverName, v.model AS vehiclemodel,
                   s.routeID, s.vehicleID, s.driverID
            FROM Schedule s
            JOIN Route   r ON s.routeID   = r.routeID
            JOIN Driver  d ON s.driverID  = d.driverID
            JOIN Vehicle v ON s.vehicleID = v.vehicleID
            ORDER BY s.scheduleID
        """)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/schedules/by-route/<int:rid>', methods=['GET'])
def schedules_by_route(rid):
    """Get schedules for a specific route (for booking wizard)."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.scheduleID, v.model AS vehiclemodel, v.capacity,
                   TO_CHAR(s.departureTime,'YYYY-MM-DD HH24:MI') AS departuretime,
                   s.frequency, s.vehicleID,
                   CASE WHEN b.vehicleID IS NOT NULL THEN 'Bus'
                        WHEN t.vehicleID IS NOT NULL THEN 'Train'
                        ELSE 'Vehicle' END AS vehicletype,
                   NVL(b.busNumber, t.trainNumber) AS vehiclenumber
            FROM Schedule s
            JOIN Vehicle v  ON s.vehicleID = v.vehicleID
            LEFT JOIN Bus b   ON v.vehicleID = b.vehicleID
            LEFT JOIN Train t ON v.vehicleID = t.vehicleID
            WHERE s.routeID = :rid
        """, rid=rid)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  TICKETS
# ═══════════════════════════════════════════
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Admin: all tickets with passenger + route (Join #2, #5)."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.ticketNumber, p.passengerName, r.routeName,
                   t.price, t.type,
                   TO_CHAR(t.issueDate,'YYYY-MM-DD') AS issuedate,
                   t.passengerID, t.scheduleID
            FROM Ticket t
            JOIN Passenger p ON t.passengerID = p.passengerID
            JOIN Schedule  s ON t.scheduleID  = s.scheduleID
            JOIN Route     r ON s.routeID     = r.routeID
            ORDER BY t.ticketNumber
        """)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/tickets/my/<int:pid>', methods=['GET'])
def my_tickets(pid):
    """Passenger: their own tickets — Subquery #3 pattern."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.ticketNumber, r.routeName,
                   s1.stationName AS fromstation, s2.stationName AS tostation,
                   t.price, t.type,
                   TO_CHAR(t.issueDate,'YYYY-MM-DD') AS issuedate,
                   TO_CHAR(sch.departureTime,'YYYY-MM-DD HH24:MI') AS departuretime,
                   v.model AS vehiclemodel
            FROM Ticket t
            JOIN Schedule  sch ON t.scheduleID      = sch.scheduleID
            JOIN Route       r ON sch.routeID        = r.routeID
            JOIN Station    s1 ON r.startStationID   = s1.stationID
            JOIN Station    s2 ON r.endStationID     = s2.stationID
            JOIN Vehicle     v ON sch.vehicleID      = v.vehicleID
            WHERE t.passengerID = :pid
            ORDER BY t.ticketNumber DESC
        """, pid=pid)
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/tickets/book', methods=['POST'])
def book_ticket():
    """
    Passenger books a ticket.
    trg_default_ticket_type  → auto sets type if null
    trg_enforce_min_price    → rejects price < 50
    ticket_seq               → used for ID
    """
    data = request.json
    prices = {'Economy': 500, 'Standard': 350, 'Business': 1200, 'VIP': 3500}
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Get next ticket number
        cur.execute("SELECT NVL(MAX(ticketNumber),0)+1 FROM Ticket")
        new_id = cur.fetchone()[0]

        price = prices.get(data.get('type', 'Standard'), 350)

        cur.execute("""
            INSERT INTO Ticket (ticketNumber, price, type, issueDate, passengerID, scheduleID)
            VALUES (:tnum, :price, :ttype, SYSDATE, :pid, :sid)
        """, tnum=new_id, price=price,
             ttype=data.get('type', 'Standard'),
             pid=data['passengerID'],
             sid=data['scheduleID'])
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'success': True,
                        'message': f'Ticket #{new_id} booked successfully!',
                        'ticketNumber': new_id, 'price': price})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/tickets/<int:tnum>', methods=['DELETE'])
def cancel_ticket(tnum):
    """Calls Cancel_Passenger_Ticket procedure."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.callproc('Cancel_Passenger_Ticket', [tnum])
        cur.close(); conn.close()
        return jsonify({'success': True, 'message': f'Ticket #{tnum} cancelled via stored procedure'})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  VIEWS (read from Oracle Views)
# ═══════════════════════════════════════════
@app.route('/api/views/active-routes', methods=['GET'])
def view_active_routes():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ActiveRoutes_VW WHERE distance > 100")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/views/senior-drivers', methods=['GET'])
def view_senior_drivers():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SeniorDrivers_VW WHERE experience >= 10 ORDER BY experience DESC")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/views/ticket-history', methods=['GET'])
def view_ticket_history():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM TicketHistory_VW ORDER BY issueDate DESC")
        rows = [clean_row(r) for r in rows_to_dicts(cur)]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': rows})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


# ═══════════════════════════════════════════
#  STATS (for dashboard)
# ═══════════════════════════════════════════
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_conn()
        cur = conn.cursor()
        stats = {}
        for key, sql in [
            ('passengers', "SELECT COUNT(*) FROM Passenger"),
            ('tickets',    "SELECT COUNT(*) FROM Ticket"),
            ('routes',     "SELECT COUNT(*) FROM Route"),
            ('vehicles',   "SELECT COUNT(*) FROM Vehicle"),
            ('drivers',    "SELECT COUNT(*) FROM Driver"),
            ('stations',   "SELECT COUNT(*) FROM Station"),
            ('revenue',    "SELECT NVL(SUM(price),0) FROM Ticket"),
        ]:
            cur.execute(sql)
            stats[key] = cur.fetchone()[0]
        cur.close(); conn.close()
        return jsonify({'success': True, 'data': stats})
    except cx_Oracle.Error as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    print("=" * 55)
    print("  Smart City Transport System — Flask Server")
    print("  Connecting to Oracle 11g...")
    print(f"  DSN: {DB_DSN}  USER: {DB_USER}")
    print("=" * 55)
    app.run(debug=True, port=5000)