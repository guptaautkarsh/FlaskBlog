# FlaskBlog

FlaskBlog is a simple blogging application designed to demonstrate **Flask development best practices**, including 
blueprints, authentication, templates, and database integration. It is suitable both as a personal blogging site 
and as a learning project for understanding Flask-based web development.

---

## Features

- 🔐 **User Authentication** – Secure registration, login, and logout  
- 📝 **Create, Edit, Delete Posts** – Full CRUD functionality for blogs  
- 📂 **User Accounts** – Each user manages their own posts  
- 🎨 **Responsive UI** – Styled using Bootstrap for a clean, modern look   
- 🗄️ **Database Support** – SQLite (development), easy migration to other RDBMS
<br></br>
![Pdf Summarizer](https://drive.google.com/file/d/1BYkbymjEk6yzShLEhIrDDtLpcgUsHj3O/view?usp=sharing)

---

## Tech Stack

- **Frontend**: HTML, CSS, Jinja2, Bootstrap  
- **Backend**: Flask (Python)  
- **Database**: SQLite (default)   

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/guptaautkarsh/FlaskBlog.git
   ```
2. **Go inside the FlaskBlog folder**  
   ```bash
   cd FlaskBlog
   ```
3. **Create a virtual environment and activate it**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```
4. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a .env file inside FlaskBlog and paste this in it**  
   ```bash
   SECRET_KEY = 'your_secret_key'
   MAIL_USERNAME = 'your_email_address'
   APP_PASSWORD = 'your_app_password'
   ```
6. **Create a profile_pic folder inside static folder**  
   ```bash
   cd blog/static
   mkdir profile_pic
   ```
7. **Start the development server with**  
   ```bash
   python3 run.py
   ```
You should be able to interact with our app on localhost:5000

