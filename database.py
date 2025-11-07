#creating the database to connect the app to, obviously need sqlite3
import sqlite3
from datetime import datetime

#below function creates the connection, it does not have a paramter
def create_connection():
    connection = sqlite3.connect('crm.db')
    return connection

#now we need to create a function to make our tables where we store the data we want to collect

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    #this is how python sends commands to the database the cursor.execute
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT NOT NULL
        )
    ''')
    #create visits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   contact_id INTEGER NOT NULL,
                   appointment_date TEXT NOT NULL,
                   comment TEXT,
                   FOREIGN KEY (contact_id) REFERENCES contacts(id)
                   
        )
    ''')
    connection.commit()
    connection.close()

def insert_contact (name, email, company):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO contacts (name, email, company)
        VALUES (?, ?, ?)
    ''', (name, email, company))

    connection.commit()
    contact_id = cursor.lastrowid
    connection.close()

    return contact_id

def get_contact_by_name(name):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT id FROM contacts WHERE name = ?                   
    ''', (name,))

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]
    else:
        return None
    

def insert_visit (contact_id, appointment_date, comment):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO visits (contact_id, appointment_date, comment)
        VALUES (?, ?, ?)
    ''', (contact_id, appointment_date, comment))

    connection.commit()
    contact_id = cursor.lastrowid
    connection.close()

    return contact_id

def get_recent_visits(limit=10):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT c.name, v.appointment_date, v.comment
                   FROM visits v 
                   JOIN contacts c ON v.contact_id = c.id
                   ORDER BY v.appointment_date DESC
                   LIMIT ?
    ''', (limit,))

    results = cursor.fetchall()
    connection.close()

    return results

def get_visits_for_contact(contact_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT appointment_date, comment
        FROM visits
        WHERE contact_id = ?
        ORDER BY appointment_date DESC
    ''', (contact_id,))

    results = cursor.fetchall()
    connection.close()

    return results

def get_least_visited_contacts(limit=10):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT c.id, c.name, c.email, c.company, COUNT(v.id) as visit_count
        FROM contacts c
        LEFT JOIN visits v ON c.id = v.contact_id
        GROUP BY c.id
        ORDER BY visit_count ASC
        LIMIT ?
    ''', (limit,))

    results = cursor.fetchall()
    connection.close()

    return results


def get_email_suggestion():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT c.id, c.name, c.email, c.company, COUNT(v.id) as visit_count, MAX(v.appointment_date) as last_visit
        FROM contacts c
        LEFT JOIN visits v ON c.id = v.contact_id
        GROUP BY c.id
        ORDER BY visit_count ASC, last_visit ASC
        LIMIT 1           
    ''')

    result = cursor.fetchone()
    connection.close()

    return result

def delete_contact(contact_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM visits WHERE contact_id  = ?', (contact_id,))

    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))

    connection.commit()
    connection.close()

def edit_contact(contact_id, name, email, company):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
                   UPDATE contacts
                   SET name = ?, email = ?, company = ?
                   WHERE id = ?
    ''', (name, email, company, contact_id))

    connection.commit()
    connection.close()

def search_contacts(search_term, search_by):
    connection = create_connection()
    cursor = connection.cursor()

    if search_by == "name":
        cursor.execute('''
                SELECT id, name, email, company
                FROM contacts
                WHERE name LIKE?
                ORDER BY name
            ''',(f'%{search_term}%',))
    elif search_by == "email":
        cursor.execute('''
                SELECT id, name, email, company
                FROM contacts
                WHERE email LIKE?
                ORDER BY name
            ''',(f'%{search_term}%',))
    elif search_by == "company":
        cursor.execute('''
                SELECT id, name, email, company
                FROM contacts
                WHERE company LIKE?
                ORDER BY name
            ''',(f'%{search_term}%',))

    results = cursor.fetchall()
    connection.close()

    return results


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%m/%d/%y")
        return True
    except ValueError:
        return False