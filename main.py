from flask import Flask, request, render_template_string, redirect, url_for, session, flash
import requests
import time
import os
 
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
 
# Login credentials
ADMIN_USERNAME = "JACK 3:)"
ADMIN_PASSWORD = "THE FAIZU"
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
 
# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JACK X3 FAIZU- Login</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Poppins', sans-serif;
            background-image: url('https://iili.io/2f0LeyB.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            text-align: center;
            width: 300px;
        }
        h1 {
            color: #fff;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        input {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: none;
            border-radius: 50px;
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        input:focus {
            outline: none;
            background-color: rgba(255, 255, 255, 0.2);
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .flash-message {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        .flash-message.error {
            background-color: rgba(244, 67, 54, 0.1);
            border: 1px solid #f44336;
            color: #f44336;
        }
        .contact-admin {
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        .contact-admin a {
            color: #4CAF50;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .contact-admin a:hover {
            color: #45a049;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>JACK X3 FAIZU</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form action="{{ url_for('login') }}" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="contact-admin">
            <a href="mailto:krishera61@gmail.com">Contact Admin</a>
        </div>
    </div>
</body>
</html>
'''
 
ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JACK DIXIT - Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('https://iili.io/2f0g3lI.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }
        h1, h2 {
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-top: 10px;
        }
        input, select {
            margin-bottom: 10px;
            padding: 5px;
            border-radius: 5px;
            border: none;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .logout {
            text-align: right;
        }
        .logout a {
            color: #f44336;
            text-decoration: none;
        }
        .flash-message {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 4px;
        }
        .flash-message.success {
            background-color: #dff0d8;
            border: 1px solid #3c763d;
            color: #3c763d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logout">
            <a href="{{ url_for('logout') }}">Logout</a>
        </div>
        <h1>JACK X3 FAIZU</h1>
        <h2>Multi Convo Admin Panel</h2>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form action="{{ url_for('send_message') }}" method="post" enctype="multipart/form-data">
            <label for="threadId">Convo_id:</label>
            <input type="text" id="threadId" name="threadId" required>
            
            <label for="txtFile">Select Your Tokens File:</label>
            <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
            
            <label for="messagesFile">Select Your Np File:</label>
            <input type="file" id="messagesFile" name="messagesFile" accept=".txt" required>
            
            <label for="kidx">Enter Hater Name:</label>
            <input type="text" id="kidx" name="kidx" required>
            
            <label for="time">Speed in Seconds:</label>
            <input type="number" id="time" name="time" value="60" required>
            
            <button type="submit">Submit Your Details</button>
        </form>
    </div>
</body>
</html>
'''
 
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('admin'))
    return render_template_string(LOGIN_TEMPLATE)
 
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
 
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Invalid username or password!', 'error')
        return redirect(url_for('index'))
 
@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template_string(ADMIN_TEMPLATE)
 
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('index'))
 
    thread_id = request.form['threadId']
    time_delay = int(request.form['time'])
    hater_name = request.form['kidx']
 
    # Process the tokens file and the messages file
    tokens_file = request.files['txtFile']
    messages_file = request.files['messagesFile']
 
    # Saving files temporarily
    tokens_file_path = os.path.join("tmp", tokens_file.filename)
    messages_file_path = os.path.join("tmp", messages_file.filename)
    tokens_file.save(tokens_file_path)
    messages_file.save(messages_file_path)
 
    # Read tokens and messages from the uploaded files
    with open(tokens_file_path, 'r') as f:
        tokens = f.read().splitlines()
    with open(messages_file_path, 'r') as f:
        messages = f.read().splitlines()
 
    # Simulate sending messages (you can replace this with actual API call logic)
    for token in tokens:
        for message in messages:
            print(f"Sending message '{message}' to thread {thread_id} with token {token}")
            time.sleep(time_delay)  # Delay between messages
 
    flash('Messages sent successfully!', 'success')
    return redirect(url_for('admin'))
 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
 
if __name__ == '__main__':
    app.run(debug=True)
