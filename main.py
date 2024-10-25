from flask import Flask, request, render_template_string, redirect, url_for, session, flash
import requests
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Login credentials
ADMIN_USERNAME = "JACK 3:)"
ADMIN_PASSWORD = "THE FAIZU"

# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JACK X3 FAIZU- Login</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #8B0000; /* Deep Red Background */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: white; /* White text color */
        }
        .login-container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            text-align: center;
            width: 300px;
        }
        h1 {
            color: white;
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
            color: white;
            font-size: 1rem;
        }
        button {
            background-color: #FF4500; /* Bright red button */
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
        }
        button:hover {
            background-color: #FF6347; /* Lighter red on hover */
        }
        .flash-message {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 4px;
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
            color: #FF4500; /* Contact link color */
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>FAIZU X3 JACK 3:)</h1>
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
            <a href="https://www.facebook.com/The.drugs.ft.chadwick.67">Contact Admin</a>
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
    <title>JACK x3 FAIZU - Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #8B0000; /* Deep Red Background */
            color: white; /* White text color */
            margin: 0;
            padding: 20px;
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
            background-color: #FF4500; /* Bright red button */
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #FF6347; /* Lighter red on hover */
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
        <h1>JACK DIXIT</h1>
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
        return redirect(url_for('admin_panel'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['username'] = username
        return redirect(url_for('admin_panel'))
    else:
        flash('Incorrect username or password. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template_string(ADMIN_TEMPLATE)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    txt_file = request.files['txtFile']
    access_tokens = txt_file.read().decode().splitlines()

    messages_file = request.files['messagesFile']
    messages = messages_file.read().decode().splitlines()

    num_comments = len(messages)
    max_tokens = len(access_tokens)

    # Create a folder with the Convo ID
    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    # Create files inside the folder
    with open(os.path.join(folder_name, "CONVO.txt"), "w") as f:
        f.write(thread_id)

    with open(os.path.join(folder_name, "Tokens.txt"), "w") as f:
        for token in access_tokens:
            f.write(f"{token}\n")

    with open(os.path.join(folder_name, "Messages.txt"), "w") as f:
        for message in messages:
            f.write(f"{message}\n")

    flash('Files created successfully!', 'success')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    while True:
        try:
            app.run(debug=False, host='0.0.0.0', port=5000)  # Run the app on port 5000
        except Exception as e:
            print(f"Error: {e}. Restarting the server...")
            time.sleep(5)  # Wait before restarting
    
