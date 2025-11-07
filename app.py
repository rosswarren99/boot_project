from flask import Flask, render_template, request, redirect
import database
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')

        database.insert_contact(name, email, company)

        return redirect('/')
    
    return render_template('add_contact.html')

@app.route('/add-visit', methods=['GET','POST'])
def add_visit():
    if request.method =='POST':
        visit_name = request.form.get('visit_name')
        visit_date = request.form.get('visit_date')
        visit_description = request.form.get('visit_description')

        contact_id = database.get_contact_by_name(visit_name)

        if contact_id is None:
            return render_template('add_visit.html' , error="Contact not found!")
        
        database.insert_visit(contact_id, visit_date, visit_description)

        return redirect('/')
    return render_template('add_visit.html')


@app.route('/view-recent-visits')
def view_recent_visits():
    visits = database.get_recent_visits()

    visits_with_days = []
    for name, date, comment in visits:
        try:
            visit_date = datetime.strptime(date, "%m/%d/%y")
            today = datetime.today()
            days_ago = (today - visit_date).days
            visits_with_days.append((name, date, days_ago, comment))
        except:
            visits_with_days.append((name, date, "N/A", comment))

    return render_template('view_recent_visits.html', visits=visits_with_days)

@app.route('/view-least-visited')
def view_least_visited():
    contacts = database.get_least_visited_contacts()
    return render_template('view_least_visited.html', contacts=contacts)

@app.route('/search-contacts', methods=['GET', 'POST'])
def search_contacts():
    results = []
    search_term = None
    search_by = None
    error = None

    if request.method == 'POST':
        search_term = request.form.get('search_term')
        search_by = request.form.get('search_by')

        if not search_term:
            error = "Please enter a search term"
        elif not search_by: 
            error = "Please select what to search by"
        else:
            results = database.search_contacts(search_term, search_by)
    
    return render_template('search_contacts.html', results=results, search_term=search_term, search_by=search_by, error=error)

@app.route('/email-suggestion')
def email_suggestion():
    suggestion = database.get_email_suggestion()

    if suggestion is None:
        return render_template('email_suggestion.html', suggestion = None)
    
    contact_id, name, email, company, visit_count, last_visit = suggestion
    
    return render_template('email_suggestion.html', suggestion = {
        'name': name,
        'email': email, 
        'company': company,
        'visit_count': visit_count,
        'last_visit': last_visit
    })

if __name__ == '__main__':
    database.create_tables()
    app.run(debug=True)