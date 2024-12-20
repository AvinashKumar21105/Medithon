import os
import requests
import datadecryption
from decryption import Decryption
import google.generativeai as genai
import PyPDF2
from requests.auth import HTTPBasicAuth
from flask import Flask,  render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (RegisterForm, LoginForm)
from fpdf import FPDF
import base64
import json
from dataencryption import Encryption
from flask import Flask, jsonify
import json


en = Encryption()
aes = en.generate_aes_key()

 # ,CreatePostForm, , CommentForm)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email = "agreedeal1@gmail.com"
# password = "zcvt pwvg bhgx qflt"
# subject = "Successful Bid Confirmation"




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)






class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    _tablename_ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))

class user_profile(db.Model):
    __tablename__ = "user_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    phoneNumber: Mapped[str] = mapped_column(String(250), nullable=False)
    gender: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    dob : Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    city: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    state: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    reports : Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/doctor_login', methods=["GET", "POST"])
def doctor_login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('doctor_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('doctor_login'))
        else:
            login_user(user)
            return redirect(url_for('doctor_home'))

    return render_template("doc_login.html", form=form, current_user=current_user)

@app.route("/doctor_register", methods=["GET", "POST"])
def doctor_register():
    form=RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('doctor_login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            role="doctor"
        )
        db.session.add(new_user)
        db.session.commit()
        print(form.email.data)
        login_user(new_user)

        return redirect(url_for("doctor_home"))

    return render_template("doc_signup.html",form=form)

@app.route('/user_login', methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('user_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('user_login'))
        else:
            login_user(user)
            return redirect(url_for('user_home'))

    return render_template("user_login.html", form=form, current_user=current_user)


@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    form=RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('user_login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            role="user"
        )
        db.session.add(new_user)
        db.session.commit()
        print(form.email.data)
        login_user(new_user)

        return redirect(url_for("user_profile_setup"))

    return render_template("user_signup.html",form=form)
global json_str
json_str = json.dumps({})
@app.route("/addprofile/user", methods=["GET", "POST"])
def user_profile_setup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        phone_number = request.form['phoneNumber']
        gender = request.form['gender']
        dob= request.form['dob']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        email=request.form['email']

        print(first_name)
        print(gender)
        new_profile = user_profile(
            firstName=first_name,
            phoneNumber=phone_number, gender=gender,dob=dob,address=address, city=city, state=state,email=email)
        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for('user_home'))
    return  render_template("user_reg.html")



# @app.route("/booking")
# def booking():
#     return render_template("booking.html")
#
# @app.route("/booked")
# def booked():
#     return render_template("booked.html")

@app.route("/doctor_home")
def doctor_home():
    return render_template("about.html")

@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

@app.route("/book_appointment")
def book_appointment():
    return render_template("booking.html")

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def pdf_to_text(pdf_path, output_path=None):
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Extract text from each page
            for page in reader.pages:
                text += page.extract_text()

            # Save to a text file if output_path is provided
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                print(f"Text extracted and saved to {output_path}")
            else:
                print("Extracted Text:")
                print(text)

            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

UPLOAD_FOLDER ="UPLOAD_FOLDER"

@app.route('/submit', methods=['POST','GET'])
def submit():
    """Handle form submission."""
    # Retrieve form data
    name = request.form.get('name')
    dob = request.form.get('dob')
    patient_info = request.form.get('patient')
    appointment_day_time = request.form.get('appointment_day_time')
    doctor_name = request.form.get('doctor_name')

    # Validate required fields


    # Handle file upload if present

    report = request.files.get('report')
    if report and allowed_file(report.filename):
        # Read the PDF file content
        pdf_content = report.read()

        # Save the PDF file temporarily
        pdf_path = 'Patient-1.pdf'  # Temporary path for the PDF file
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)

        # Define the output path for the text file
        output_path = 'output.txt'

        # Pass the paths to your pdf_to_text function
        pdf_to_text(pdf_path, output_path)
        with open(output_path, 'r') as file:
            data_str = file.read()
            genai.configure(api_key="AIzaSyA-UjYFpBvXHa7EEXPgVTKB5DuQF8h9wWs")
            model = genai.GenerativeModel("gemini-1.5-flash")
            data_list = ["personalDetails", "medicalHistory",
                        "examinationDetails",
                        "diagnosticTests",
                        "dateOfTestReports",
                        "diagnosis",
                        "treatmentPlan",
                        "doctorDetails"]

            data = {
                "personalDetails": "",
                "medicalHistory": "",
                "examinationDetails": "",
                "diagnosticTests": "",
                "dateOfTestReports": "",
                "diagnosis": "",
                "treatmentPlan": "",
                "doctorDetails": "",
            }

            for x in data_list:
                response = model.generate_content(
                    f"{data_str}: from the data find the {x} and give it as a single line text")
                content = response.text
                data[x] = content;
            print(data)
            for key in data:
                encrypted_data = en.encrypt_data(data[key], aes)
                data[key] = encrypted_data
            encrypted_aes_key = en.encrypt_aes_key(aes)
            data["aes"] = encrypted_aes_key
            print("\nData is successfully encrypted and posted as an api on the server.\n ")
            print("api url : http://127.0.0.1:5000/your_acces_token\n")
            api = data
            global json_str

            encoded_dict = {key: base64.b64encode(value).decode('utf-8') for key, value in api.items()}

            # Convert the dictionary to a JSON string

            json_str = json.dumps(encoded_dict)





    elif report and not allowed_file(report.filename):
        flash('Invalid file type. Allowed types are: PDF', 'error')
        return redirect(url_for('user_home'))
    return redirect(url_for('api_set'))


@app.route("/api", methods=["GET"])
def api_set():
        return jsonify(json_str)

@app.route("/get_req")
def get_req():
    data_out={}
    data_out=datadecryption.dec_data()
    return data_out
@app.route("/booked_appointment")
def booked_appointment():
    return render_template("booked.html")




if __name__ == "__main__":
    app.run(port=3000,debug=True)