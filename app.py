from flask import Flask, render_template, request, redirect
import database
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

if __name__ == '__main__':
    database.create_tables()
    app.run(debug=True)