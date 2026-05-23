# AI Notes Manager Backend 🚀

A Flask-based backend project for managing notes with JWT authentication, MongoDB integration, PDF upload & extraction, AI tags generation, and smart search functionality.

## Features

* User Registration & Login
* JWT Authentication
* Protected APIs
* Add / Update / Delete Notes
* MongoDB Database Integration
* PDF Upload
* PDF Text Extraction
* AI Tags Generation
* Smart Search using TF-IDF
* Frontend Integration using HTML, CSS, JavaScript

## Technologies Used

* Python
* Flask
* MongoDB
* Flask-JWT-Extended
* PyPDF2
* Scikit-learn
* HTML
* CSS
* JavaScript

## Project Structure

ai-notes-manager-backend/
│
├── app.py
├── routes.py
├── db.py
├── requirements.txt
├── .env
│
├── templates/
│ ├── index.html
│ ├── login.html
│ └── register.html
│
├── static/
│ ├── css/
│ └── js/
│
└── uploads/

## Installation

1. Clone repository

git clone https://github.com/PathanAfrin20/ai-notes-manager-backend.git

2. Create virtual environment

python -m venv venv

3. Activate virtual environment

Windows:
venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run project

python app.py

## API Testing

All APIs were tested using Postman.

## Future Improvements

* AI summarization
* User dashboard improvements
* Better frontend UI
* Deploy on Render

