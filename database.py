#creating the database to connect the app to, obviously need sqlite3
import sqlite3

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