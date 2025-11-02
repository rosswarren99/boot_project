from database import insert_contact, create_tables, get_contact_by_name, insert_visit

create_tables()

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

    contact_id = insert_contact(name, email, company)
    print(f"Contact saved! ID: {contact_id}")



def insertVisit():
    visitName = input("Who did you visit? ")
    visitDate = input("On what day? ")
    visitDescription = input("Describe the meeting: ")
    
    contact_id = get_contact_by_name(visitName)

    if contact_id is None:
        print("Contact not found! Make sure you entered the exact name.")
        return
    
    insert_visit(contact_id, visitDate, visitDescription)
    print(f"Visit recorded!")


while True:
    print("\n --- CRM MENU ---")
    print("1. Add a contact")
    print("2. Record a visit")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        contactCardCreate()
    elif choice == "2":
        insertVisit()
    elif choice == "3":
        break
    else:
        print("Invalid choice, try again")
