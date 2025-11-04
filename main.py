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


while True:
    print("\n --- CRM MENU ---")
    print("1. Add a contact")
    print("2. Record a visit")
    print("3. View 10 most recent visits")
    print("4. View Number of Visits for Client")
    print("5. View Number of Least Visited Clients ")
    print("6. Email Reachout Suggestion")
    print("7. Exit")

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
        break
    else:
        print("Invalid choice, try again")
