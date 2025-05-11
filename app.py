#import flask and other libraries
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# BMI Model
class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = ""
    
    if request.method == "POST":
        weight = float(request.form["weight"])
        height_cm = float(request.form["height"])
        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        # Save to database
        record = BMIRecord(weight=weight, height=height_cm, bmi=bmi, category=category)
        db.session.add(record)
        db.session.commit()

    # Show last 5 records
    records = BMIRecord.query.order_by(BMIRecord.date.desc()).limit(5).all()

    return render_template("index.html", bmi=bmi, category=category, records=records)

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the BMI table if it doesn't exist
    app.run(debug=True)
