from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape


app = Flask(__name__)

@app.route('/login', method=["POST", "GET"])
def login():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
  
  return render_template('login.html')