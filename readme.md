I want to make a marketing tracking CRM system where I document a meeting in the terminal of who I saw, when I met them, what company they work for and who I have not seen in the last number of days, weeks or months.

Tech:
- Python
- sqlite (?)

Functions should be:
- Enter a contact name, email and company
- Enter an appointment for a contact
    - Met in office 10/07/25 with John Smith at Marsh
    - Track the number of visist for the client
- View the 10 most recent visits and show how many days it has been since
- View the 10 lowest visited brokers
- Suggest a person to email

Breaking that down further, the data collected should be:
- contact name
- email address
- company
- appointment date entry
    - tied to the appointment comment (the above date is tied here)
- number of visits to that client
- most recent company visits by date and total number of visits
- least recent company visits by date and total number of vists
- email person suggestion based on number of visits being low



The contact entering function:
- Contact first name and last name
- Contact email
- Contact Company
