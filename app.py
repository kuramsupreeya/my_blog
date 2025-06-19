from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flashing messages

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',         # Replace with your MySQL username if different
            password='',         # Replace with your MySQL password
            database='resume_portfolio'
        )
        return conn
    except Error as e:
        print("❌ Database connection error:", e)
        return None

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Skills page
@app.route('/skills')
def skills():
    skills = [
        {"name": "DSA", "link": "https://example.com/dsa-cert.pdf"},
        {"name": "Python Full Stack", "link": "https://example.com/python-cert.pdf"},
        {"name": "HTML", "link": "https://example.com/html-cert.pdf"},
        {"name": "CSS", "link": "https://example.com/css-cert.pdf"},
        {"name": "JavaScript", "link": "https://example.com/js-cert.pdf"}
    ]
    return render_template('skills.html', skills=skills)

# Experience page
@app.route('/experience')
def experience():
    experience = [
        {
            "role": "Web Development Intern",
            "company": "ABC Tech",
            "duration": "Jan 2024 - Mar 2024",
            "description": "Worked with HTML, CSS, Flask and Bootstrap."
        },
        {
            "role": "Freelancer",
            "company": "Self Employed",
            "duration": "Apr 2024 - Present",
            "description": "Developed portfolio websites using Flask."
        }
    ]
    return render_template('experience.html', experience=experience)

# Contact page (GET and POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contacts = {
        "GitHub": "https://github.com/kuramsupreeya",
        "LinkedIn": "https://linkedin.com/in/kuramsupreeya",
        "Email": "mailto:yourname@example.com"
    }

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO contact_messages (name, email, subject, message)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, subject, message))
                conn.commit()
                flash("✅ Message sent successfully!", "success")
            except Exception as e:
                print("❌ Error inserting message:", e)
                flash("❌ Failed to send message.", "danger")
            finally:
                cursor.close()
                conn.close()
        else:
            flash("❌ Could not connect to database.", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html', contacts=contacts)

# Test DB route
@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return "✅ Successfully connected to the database."
    else:
        return "❌ Failed to connect to the database."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
