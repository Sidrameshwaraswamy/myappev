from flask import Flask, request, redirect, url_for, flash, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load ML Model (with error handling)
model_path = "ev_model.pkl"
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
else:
    model = None  # Prevent crashes if model file is missing

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "login_username" in request.form:
            username = request.form["login_username"]
            password = request.form["login_password"]
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("predict"))
            else:
                flash("Invalid username or password", "danger")

        elif "signup_username" in request.form:
            username = request.form["signup_username"]
            password = request.form["signup_password"]
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists!", "danger")
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Signup successful! Please log in.", "success")

    # Read index.html manually and return it
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    prediction = None
    if request.method == "POST":
        if model is None:
            prediction = "Model not found! Please check ev_model.pkl"
        else:
            try:
                hour = int(request.form["hour"])
                dayofweek = int(request.form["dayofweek"])
                temperature = float(request.form["temperature"])
                station_id = int(request.form["station_id"])

                input_data = np.array([[hour, dayofweek, temperature, station_id]])
                prediction = model.predict(input_data)[0]
            except:
                prediction = "Invalid input"

    # Read predict.html manually and replace the placeholder with the prediction
    with open("predict.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content.replace("{{ prediction }}", str(prediction))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

# Serve static files (CSS)
@app.route('/styles.css')
def serve_css():
    return send_file("styles.css")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(host="127.0.0.1", port=5000, debug=True)
