import database
from datetime import datetime

database.create_tables()

'''
The contact entering function:
- Contact first name and last name
- Contact email
- Contact Company
'''
def contactCardCreate():
    name = input("Please enter the contact name: ")
    email = input("What is their email address? ")
    company = input("What company are they associated with? ")

    contact_id = database.insert_contact(name, email, company)
    print(f"Contact saved! ID: {contact_id}")



def insertVisit():
    visitName = input("Who did you visit? ")
    visitDate = input("On what day? ")
    visitDescription = input("Describe the meeting: ")
    
    contact_id = database.get_contact_by_name(visitName)

    if contact_id is None:
        print("Contact not found! Make sure you entered the exact name.")
        return
    
    database.insert_visit(contact_id, visitDate, visitDescription)
    print(f"Visit recorded!")

def viewRecentVisits():
    visits = database.get_recent_visits()

    if not visits:
        print("No visits recorded yet!")
        return
    
    print("\n --- 10 Most Recent Visits --- ")
    for name, date, comment in visits:
        try:
            visit_date = datetime.strptime(date, "%m/%d/%y")
            today = datetime.today()
            days_ago = (today - visit_date).days
            print(f"{name} | {date} | {days_ago} days ago | {comment}")
        except:
            print(f"{name} | {date} | {comment}")

def viewVisitsForContact():
    contact_name = input("Enter contact name: ")
    contact_id = database.get_contact_by_name(contact_name)

    if contact_id is None:
        print("Contact not found!")
        return
    
    visits = database.get_visits_for_contact(contact_id)

    if not visits:
        print(f"No visits recorded for {contact_name}")
        return
    
    print(f"\n --- Visits for {contact_name}")
    print(f"Total visits: {len(visits)}")
    for date, comment in visits:
        try:
            visit_date = datetime.strptime(date, "%m/%d/%y")
            today = datetime.today()
            days_ago = (today - visit_date).days
            print(f"{date} ({days_ago} days ago | {comment})")
        except:
            print(f"{date} | {comment}")

def viewLeastVisitedContacts():
    contacts = database.get_least_visited_contacts()

    if not contacts:
        print("No contacts found!")
        return
    
    print("\n --- 10 Least Visited Contacts --- ")
    for contact_id, name, email, company, visit_count in contacts:
        print(f"{name} | {email} | {company} | {visit_count} visits")

def getEmailSuggestion():
    suggestion = database.get_email_suggestion()

    if suggestion is None:
        print("No contacts found!")
        return
    
    contact_ud, name, email, company, visit_count, last_visit = suggestion

    print("\n --- Email Suggestion ---")
    print(f"You should reach out to: {name}")
    print(f"Email: {email}")
    print(f"Company: {company}")
    print(f"Total Visits: {visit_count}")
    print(f"Last Visit: {last_visit if last_visit else 'Never'}")

def deleteContact():
    contact_name = input("Enter contact name to delete: ")
    contact_id = database.get_contact_by_name(contact_name)

    if contact_id is None:
        print("Contact not found!")
        return
    
    confirm = input(f"Are you sure you want to delete {contact_name}? (yes/no): ")

    if confirm.lower() == "yes":
        database.delete_contact(contact_id)
        print(f"{contact_name} has been deleted")
    else:
        print("Delete Cancelled")
def editContact():
    contact_name = input("Enter contact name to edit: ")
    contact_id = database.get_contact_by_name(contact_name)

    if contact_id is None:
        print("Contact not found")
        return
    
    print(f"\nEditing {contact_name}. Leave blank to keep current value.")

    new_name = input("New name (or press Enter to skip): ") or contact_name
    new_email = input("New email (or press Enter to skip): ")
    new_company = input("New company (or press Enter to skip): ")

    if not new_email or not new_company:
        connection = database.create_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT email, company FROM contacts where id = ?', (contact_id))
        current = cursor.fetchone()
        connection.close()

        new_email = new_email or current[0]
        new_company = new_company or current[1]
    
    database.edit_contact(contact_id, new_name, new_email, new_company)
    print(f"Contact updated!")

def searchContacts():
    print("\nSearch by:")
    print("1. Name")
    print("2. Email")
    print("3. Company")

    search_choice = input("Choose search type (1-3): ")

    if search_choice == "1":
        search_by = "name"
    elif search_choice == "2":
        search_by = "email"
    elif search_choice == "3":
        search_by = "company"
    else:
        print("Invalid choice!")
        return 
    
    search_term = input(f"Enter {search_by} to search: ")
    results = database.search_contacts(search_term, search_by)

    if not results:
        print(f"No contacts found matching '{search_term}'")
        return
    
    print(f"\n --- Search Results ({len(results)}) found) ---")
    for contact_id, name, email, company in results:
        print(f"ID: {contact_id} | {name} | {email} | {company}")


while True:
    print("\n --- CRM MENU ---")
    print("1. Add a contact")
    print("2. Record a visit")
    print("3. View 10 most recent visits")
    print("4. View Number of Visits for Client")
    print("5. View Number of Least Visited Clients ")
    print("6. Email Reachout Suggestion")
    print("7. Delete a contact")
    print("8. Edit a contact")
    print("9. Search")
    print("10. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        contactCardCreate()
    elif choice == "2":
        insertVisit()
    elif choice == "3":
        viewRecentVisits()
    elif choice == "4":
        viewVisitsForContact()
    elif choice =="5":
        viewLeastVisitedContacts()
    elif choice == "6":
        getEmailSuggestion()
    elif choice == "7":
        deleteContact()
    elif choice == "8":
        editContact()
    elif choice == "9":
        searchContacts()
    elif choice == "10":
        break
    else:
        print("Invalid choice, try again")
