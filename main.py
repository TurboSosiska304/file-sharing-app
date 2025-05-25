from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your-secret-key'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'mp3', 'wav', 'ogg', 'mp4', 'avi', 'mkv', 'doc'}

# Простая база пользователей (для примера, в продакшене используйте БД)
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_category(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext in {'jpg', 'jpeg', 'png', 'gif'}:
        return 'Photos'
    elif ext in {'mp4', 'avi', 'mkv'}:
        return 'Videos'
    elif ext in {'mp3', 'wav', 'ogg'}:
        return 'Audio'
    elif ext in {'pdf', 'doc', 'docx', 'txt'}:
        return 'Documents'
    else:
        return 'Other'

# Проверка авторизации
def require_login(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@require_login
def index():
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    files = os.listdir(user_folder)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
@require_login
def upload_file():
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    files = request.files.getlist('file')
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))
            uploaded_files.append(filename)
        else:
            return jsonify({'success': False, 'message': f'File {file.filename} not allowed'}), 400
    
    return jsonify({'success': True, 'message': 'Files uploaded successfully', 'files': uploaded_files})

@app.route('/files')
@require_login
def list_files():
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    files = os.listdir(user_folder) if os.path.exists(user_folder) else []
    categorized_files = {
        'Photos': [],
        'Videos': [],
        'Audio': [],
        'Documents': [],
        'Other': []
    }
    for file in files:
        category = get_file_category(file)
        categorized_files[category].append(file)
    return render_template('files.html', categorized_files=categorized_files)

@app.route('/delete/<filename>', methods=['POST'])
@require_login
def delete_file(filename):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    file_path = os.path.join(user_folder, filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': f'File {filename} deleted'})
        else:
            return jsonify({'success': False, 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<filename>')
@require_login
def download_file(filename):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    try:
        return send_file(os.path.join(user_folder, filename), as_attachment=True)
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)