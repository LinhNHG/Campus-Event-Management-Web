import sqlite3
from pathlib import Path
from datetime import date

def get_connection():
    conn = sqlite3.connect(Path(__file__).resolve().parent / "database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_database():
    conn = get_connection()

    with open(Path(__file__).resolve().parent / "schema.sql", "r", encoding="utf-8") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

    print("Database created successfully!")

def seed_events():
    conn = get_connection()
    cursor = conn.cursor()

    events = [
        ("AI Workshop", "2026-07-20", "Hall A", 50),
        ("Python Bootcamp", "2026-07-25", "Room B201", 40),
        ("Cyber Security Seminar", "2026-08-05", "Conference Hall", 100),
        ("Music Festival", "2026-08-15", "Main Stadium", 300),
        ("Startup Pitching", "2026-08-20", "Innovation Center", 80)
    ]

    cursor.executemany("""
        INSERT INTO Events (name, date, location, capacity)
        VALUES (?, ?, ?, ?)
    """, events)

    conn.commit()
    conn.close()

    print("Sample events added successfully!")

def seed_users():
    conn = get_connection()
    cursor = conn.cursor()

    users = [
        ("admin", "Administrator", "Admin"),
        ("student1", "Nguyen Van A", "Student"),
        ("student2", "Tran Thi B", "Student")
    ]

    cursor.executemany("""
        INSERT INTO Users (user_id, name, role)
        VALUES (?, ?, ?) 
    """, users)

    conn.commit()
    conn.close()

    print("Sample users added successfully!")

def get_all_events():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Events ORDER BY date")

    events = cursor.fetchall()

    conn.close()

    return events

def search_events(keyword):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Events
        WHERE name LIKE ?
           OR location LIKE ?
        ORDER BY date
    """, (f"%{keyword}%", f"%{keyword}%"))

    events = cursor.fetchall()

    conn.close()

    return events

def get_event_by_id(event_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Events
        WHERE event_id = ?
    """, (event_id,))

    event = cursor.fetchone()

    conn.close()

    return event

def get_user(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user

def add_event(name, date, location, capacity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Events (name, date, location, capacity)
        VALUES (?, ?, ?, ?)
    """, (name, date, location, capacity))

    conn.commit()
    conn.close()

def update_event(event_id, name, date, location, capacity):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Events
        SET 
            name = ?,
            date = ?,
            location = ?,
            capacity = ?
        WHERE event_id = ?
    """,
    (
        name,
        date,
        location,
        capacity,
        event_id
    ))

    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Events
        WHERE event_id = ?
    """, (event_id,))

    conn.commit()
    conn.close()

def get_all_registrations():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Registrations.user_id,
            Events.name,
            Events.date,
            Registrations.registration_date
        FROM Registrations

        INNER JOIN Events
            ON Registrations.event_id = Events.event_id

        ORDER BY Registrations.registration_date DESC
    """)

    registrations = cursor.fetchall()

    conn.close()

    return registrations

def count_registrations(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Registrations
        WHERE event_id = ?
    """, (event_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

def count_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Events
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def total_capacity():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(capacity)
        FROM Events
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0

def upcoming_events():
    conn = get_connection()
    cursor = conn.cursor()

    today = date.today().isoformat()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Events
        WHERE date >= ?
    """, (today,))

    total = cursor.fetchone()[0]

    conn.close()

    return total

def next_event():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    today = date.today().isoformat()

    cursor.execute("""
        SELECT *
        FROM Events
        WHERE date >= ?
        ORDER BY date
        LIMIT 1
    """, (today,))

    event = cursor.fetchone()

    conn.close()

    return event

def register_event(user_id, event_id):
    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("""
        INSERT INTO Registrations (user_id, event_id)
        VALUES (?, ?)
    """, (user_id, event_id))

    conn.commit()
    conn.close()

def is_registered(user_id, event_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Registrations
        WHERE user_id = ?
        AND event_id = ?
    """, (user_id, event_id))

    registration = cursor.fetchone()

    conn.close()

    return registration is not None

def registration_exists(user_id, event_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM Registrations
        WHERE user_id = ?
          AND event_id = ?
    """, (user_id, event_id))

    exists = cursor.fetchone() is not None

    conn.close()

    return exists

def add_user(user_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Users (user_id, name, role)
        VALUES (?, ?, ?)
    """, (
        user_id,
        name,
        "Student"
    ))

    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM Users
        WHERE user_id = ?
    """, (user_id,))

    exists = cursor.fetchone() is not None

    conn.close()

    return exists

def get_my_events(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Events.event_id,
            Events.name,
            Events.date,
            Events.location
        FROM Registrations
        INNER JOIN Events
            ON Registrations.event_id = Events.event_id
        
        WHERE Registrations.user_id = ?
                   
        ORDER BY Events.date
    """, (user_id,))

    events = cursor.fetchall()

    conn.close()

    return events

def cancel_registration(user_id, event_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Registrations
        WHERE user_id = ?
        AND event_id = ?
    """, (user_id, event_id))

    conn.commit()

    conn.close()

def count_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Users
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def total_registrations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Registrations
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def recent_registrations(limit=5):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Users.name AS user_name,
            Events.name AS event_name,
            Events.date,
            Registrations.registration_date

        FROM Registrations

        INNER JOIN Users
            ON Registrations.user_id = Users.user_id

        INNER JOIN Events
            ON Registrations.event_id = Events.event_id

        ORDER BY Registrations.rowid DESC

        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def most_popular_event():

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Events.name,
            COUNT(Registrations.user_id) AS total

        FROM Events

        LEFT JOIN Registrations
            ON Events.event_id = Registrations.event_id

        GROUP BY Events.event_id

        ORDER BY total DESC

        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row

def least_popular_event():

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Events.name,
            COUNT(Registrations.user_id) AS total

        FROM Events

        LEFT JOIN Registrations
            ON Events.event_id = Registrations.event_id

        GROUP BY Events.event_id

        ORDER BY total ASC

        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row

def event_capacity_status():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Events.event_id,
            Events.name,
            Events.capacity,
            COUNT(Registrations.user_id) AS registered

        FROM Events

        LEFT JOIN Registrations
            ON Events.event_id = Registrations.event_id

        GROUP BY Events.event_id

        ORDER BY Events.date
    """)

    events = cursor.fetchall()

    conn.close()

    return events

def home_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Registrations")
    total_registrations = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Events
        WHERE date >= DATE('now')
    """)
    upcoming = cursor.fetchone()[0]

    conn.close()

    return (
        total_events,
        total_users,
        total_registrations,
        upcoming
    )

def upcoming_event_list():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Events
        WHERE date >= DATE('now')
        ORDER BY date
        LIMIT 5
    """)

    events = cursor.fetchall()

    conn.close()

    return events

def registration_chart_data():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Events.name,
            COUNT(Registrations.user_id) AS total
        FROM Events
        LEFT JOIN Registrations
            ON Events.event_id = Registrations.event_id
        GROUP BY Events.event_id
        ORDER BY total DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

if __name__ == "__main__":
    seed_users()