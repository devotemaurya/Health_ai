from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
import json
import sqlite3
from io import BytesIO
from xhtml2pdf import pisa
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load JSON data
with open("data/symptoms.json") as f:
    symptom_data = json.load(f)

with open("data/firstaid.json") as f:
    firstaid_data = json.load(f)

# Landing Page
@app.route("/landing")
def landing():
    return render_template("landing.html")

# Redirect root "/" to landing
@app.route("/")
def home_redirect():
    return redirect("/landing")

# Symptom Checker Route (moved to /checker)
@app.route("/checker", methods=["GET", "POST"])
def index():
    if 'user' not in session:
        return redirect("/login")

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        matched_conditions = []

        for condition, symptoms in symptom_data.items():
            if any(symptom in selected_symptoms for symptom in symptoms):
                matched_conditions.append(condition)

        suggestions = {cond: firstaid_data.get(cond, "No info available") for cond in matched_conditions}

        # Save history
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (username, symptoms, conditions) VALUES (?, ?, ?)",
                  (session['user'], ', '.join(selected_symptoms), ', '.join(matched_conditions)))
        conn.commit()
        conn.close()

        return render_template("result.html", selected=selected_symptoms, result=suggestions, user=session['user'])

    all_symptoms = sorted({sym for lst in symptom_data.values() for sym in lst})
    return render_template("index.html", symptoms=all_symptoms, user=session['user'])

# ✅ PDF Export Route
@app.route("/download-report", methods=["POST"])
def download_report():
    selected = request.form.get("selected")
    result = request.form.get("result")

    selected_list = selected.split(", ")
    result_dict = json.loads(result)

    rendered = render_template("pdf_template.html", selected=selected_list, result=result_dict, user=session.get('user', 'User'))

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)

    if pisa_status.err:
        return "Error generating PDF"

    pdf.seek(0)
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=health_report.pdf'
    return response

# ✅ Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "⚠️ Email already registered."
        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")

# ✅ Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email = ? AND password = ?", (email, password))
        result = c.fetchone()
        conn.close()

        if result:
            session['user'] = result[0]
            return redirect("/checker")
        else:
            return "❌ Invalid credentials."

    return render_template("login.html")

#  Logout
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")

#  History
@app.route("/history")
def history():
    if 'user' not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT symptoms, conditions, timestamp FROM history WHERE username = ? ORDER BY timestamp DESC", (session['user'],))
    rows = c.fetchall()
    conn.close()

    return render_template("history.html", history=rows, user=session['user'])

#  AI Chatbot with Together API
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    prompt = data.get("prompt", "")
    api_key = os.getenv("TOGETHER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a helpful health assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        output = response.json()
        reply = output["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print("Chatbot error:", e)
        return jsonify({"reply": "Sorry, I'm having trouble reaching the chatbot."}), 500

# #  Run the app
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=8000)
