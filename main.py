from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL URI with your credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql12743492:Kzbjb57YFM@sql12.freesqldatabase.com:3306/sql12743492'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Contact_form model with the message field
class Contact_form(db.Model):
    __tablename__ = 'contact_form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(15))
    city = db.Column(db.String(100))

# Define Project model with img, name, and description
class Project(db.Model):
    __tablename__ = 'ourproject'  # Corrected table name to 'ourproject'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255))
    name = db.Column(db.String(100))
    discription = db.Column(db.String(255))  # Corrected column name from 'description' to 'discription'

class HappyClient(db.Model):
        __tablename__ = 'happy_client'  # Name of the table in the database
        id = db.Column(db.Integer, primary_key=True)
        img = db.Column(db.String(255))
        name = db.Column(db.String(100))
        discription = db.Column(db.String(255))
        designation = db.Column(db.String(100))



class Subscription(db.Model):
    __tablename__ = 'subcriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

@app.route("/", methods=['GET', 'POST'])
def landing_page():
    projects = Project.query.all()  # Fetch all projects from the database
    clients = HappyClient.query.all()  # Fetch all clients from the database

    if request.method == 'POST':
        if 'name' in request.form:  # Handle the contact form submission
            try:
                # Retrieve form data
                name = request.form.get('name')
                email = request.form.get('email')
                mobile = request.form.get('mobile')
                city = request.form.get('city')

                # Create a new entry with form data
                entry = Contact_form(name=name, email=email, mobile=mobile, city=city)
                db.session.add(entry)
                db.session.commit()

                return jsonify({"message": "Contact form submitted successfully"}), 201
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                return jsonify({"message": "An error occurred"}), 500

        elif 'email' in request.form:  # Handle subscription form submission (for non-AJAX)
            try:
                email = request.form.get('email')

                # Check if the email is already subscribed
                existing_subscription = Subscription.query.filter_by(email=email).first()
                if existing_subscription:
                    return jsonify({"message": "This email is already subscribed"}), 400

                # Create a new subscription
                new_subscription = Subscription(email=email)
                db.session.add(new_subscription)
                db.session.commit()

                return jsonify({"message": "Subscribed successfully"}), 201
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                return jsonify({"message": "An error occurred while subscribing"}), 500

        elif request.is_json:  # Handle subscription via AJAX (JSON data)
            try:
                data = request.get_json()  # Get the JSON data from the request
                email = data.get('email')

                # Check if the email is already subscribed
                existing_subscription = Subscription.query.filter_by(email=email).first()
                if existing_subscription:
                    return jsonify({"message": "This email is already subscribed"}), 400

                # Create a new subscription
                new_subscription = Subscription(email=email)
                db.session.add(new_subscription)
                db.session.commit()

                return jsonify({"message": "Subscribed successfully"}), 201
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                return jsonify({"message": "An error occurred while subscribing"}), 500

    return render_template('landing.html', projects=projects, clients=clients)



# Admin Page
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    # Fetch contact forms and subscriptions from the database
    contact_forms = Contact_form.query.all()
    subscriptions = Subscription.query.all()
    projects = Project.query.all()
    clients = HappyClient.query.all()

    if request.method == 'POST':
        # Add new project
        if 'add_project' in request.form:
            try:
                project_image = request.form.get('project_image')
                project_name = request.form.get('project_name')
                project_description = request.form.get('project_description')

                # Create a new project entry
                new_project = Project(img=project_image, name=project_name, discription=project_description)
                db.session.add(new_project)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error adding project: {e}")

        # Add new client
        elif 'add_client' in request.form:
            try:
                client_image = request.form.get('client_image')
                client_name = request.form.get('client_name')
                client_description = request.form.get('client_description')
                client_designation = request.form.get('client_designation')

                # Create a new client entry
                new_client = HappyClient(img=client_image, name=client_name, discription=client_description, designation=client_designation)
                db.session.add(new_client)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error adding client: {e}")

    return render_template('admin.html', contact_forms=contact_forms, subscriptions=subscriptions, projects=projects, clients=clients)


if __name__ == '__main__':
    app.run(debug=True)
