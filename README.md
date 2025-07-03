
# 🩺 HealthCheck AI – Your Personal Health Companion

**HealthCheck AI** is an intelligent, user-friendly web application designed to help users check symptoms, get first-aid guidance, track health history, and even chat with an AI assistant for general medical support. Built with Python Flask, HTML/CSS, and integrated with Together AI, it offers a smooth and helpful experience.

---

## 🔗 Live Demo

👉 [Visit the Live App](https://healthai-production-e0e5.up.railway.app/) 

---

## 🚀 Features

- ✅ Symptom checker with condition mapping
- ✅ AI-powered chatbot for general health queries
- ✅ First-aid suggestions based on predicted conditions
- ✅ PDF report generation of your health check
- ✅ Secure user login & registration
- ✅ Health history tracker
- 🌗 Responsive UI with dark/light mode toggle
- 📽️ Landing page with animated visuals or videos
- 🔒 Data managed securely using SQLite

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS (Dark/Light Mode), JavaScript
- **Backend:** Python Flask
- **Database:** SQLite
- **AI API:** Together AI (Mistral 7B model)
- **Hosting:** Railway / PythonAnywhere

---

## 📁 Folder Structure

```
Health/
│
├── data/                  # Contains symptom & first-aid data (JSON)
├── static/                # Images, styles, videos, chatbot.js
├── templates/             # All HTML templates (login, index, history, result, etc.)
├── .env                   # Stores your Together AI API Key
├── app.py                 # Main Flask application
├── chatbot.py             # AI response handler
├── init_db.py             # Creates initial DB schema
├── add_history_table.py   # Adds health history table to DB
├── requirements.txt       # Python dependencies
└── users.db               # SQLite database
```

---

## ⚙️ Setup Instructions (Local)

1. **Clone the Repo**
   ```bash
   git clone https://github.com/yourusername/HealthCheck-AI.git
   cd HealthCheck-AI
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add `.env` file**
   ```env
   TOGETHER_API_KEY=your_api_key_here
   ```

5. **Initialize the Database**
   ```bash
   python init_db.py
   python add_history_table.py
   ```

6. **Run the App**
   ```bash
   python app.py
   ```
 
 
---

## 🙏 Acknowledgments

- Together AI for the free API
- Open-source contributors and documentation
