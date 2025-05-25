# File Sharing App

A simple Flask-based web application for uploading, downloading, and deleting files, with user authentication and file categorization (Photos, Videos, Audio, Documents, Other).

## Features
- User authentication (login/logout).
- File upload with progress bar, speed (MB/s), and size tracking.
- File categorization by type (Photos, Videos, Audio, Documents, Other).
- Per-user file storage (each user sees only their files).
- File download and deletion.

## Requirements
- Python 3.8+
- Flask 3.0.3
- Werkzeug 3.0.4

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/file-sharing-app.git
   cd file-sharing-app

Create and activate a virtual environment:
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
bash

pip install -r requirements.txt

Run the application:
bash

python app.py

Open http://127.0.0.1:5000/login in your browser.

Usage
Login: Use predefined credentials (e.g., user1/password1, user2/password2).

Upload: On the main page (/), upload files and see progress (percentage, speed, uploaded/total size).

View Files: Go to /files to see categorized files with download and delete options.

Logout: Click "Logout" to end the session.

Project Structure

file-sharing-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── templates/              # HTML templates
│   ├── index.html          # Upload page
│   ├── files.html          # Categorized file list
│   ├── login.html          # Login page
├── static/                 # Static files
│   ├── styles/
│   │   └── style.css       # CSS styles
│   └── scripts/
│       └── script.js       # JavaScript for upload progress and deletion
└── uploads/                # User file storage

Deployment
For production, consider:
Use a WSGI server (e.g., Gunicorn) instead of Flask's development server.

Deploy on a platform like Heroku, Render, or AWS.

Replace the in-memory user dictionary with a database (e.g., SQLite, PostgreSQL).

Add environment variables for SECRET_KEY and other sensitive data.

Set MAX_CONTENT_LENGTH to limit file sizes.

Use cloud storage (e.g., AWS S3) for files.

Enable HTTPS and CSRF protection.

Example for Heroku:
bash

heroku create
git push heroku main
heroku open

Notes
The current user authentication is basic (hardcoded dictionary). Replace with a proper database and password hashing (e.g., Flask-Bcrypt).

File uploads are stored locally in uploads/<username>/. For production, use cloud storage.

Add CSRF tokens for POST requests in production.

