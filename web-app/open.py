import RPi.GPIO as GPIO
import pigpio
import os
import signal
import time
from flask import Flask, render_template, redirect, url_for, request, session, abort, url_for

app = Flask(__name__)

redPin   = 26
buzzerPin = 22
servoPin = 17
pi = pigpio.pi()

def end(signal,frame):
    print ("\n[*] Cleaning up...\nBye!")
    pi.write(redPin, 0)
    pi.write(buzzerPin, 0)
    pi.set_servo_pulsewidth(servoPin, 2500)
    GPIO.cleanup()
    exit(1)

signal.signal(signal.SIGINT, end)

pi.set_servo_pulsewidth(servoPin, 2500)
pi.write(redPin, 0)
pi.write(buzzerPin, 0)

def triggerLights():
    pi.write(redPin, 1)
    time.sleep(6)
    pi.write(redPin, 0)

def triggerBuzzer():
    pi.write(buzzerPin, 1)
    time.sleep(3)
    pi.write(buzzerPin, 0)

def triggerDoor():
    pi.set_servo_pulsewidth(servoPin, 1000)
    time.sleep(6)
    pi.set_servo_pulsewidth(servoPin, 2500)

## Routing
# Route for handling index page
@app.route("/")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

# Route for handling home page
@app.route("/home")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in'):
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials!'
            else:
                session['logged_in'] = True
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

# Route for handling the logout page logic
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# Route for handling GPIO / setting pins on and off
# Missing auth check as one of the bugs, failure to call `if not session.get('logged_in')`
@app.route("/trigger/<changePin>/on")
def action(changePin):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        changePin = int(changePin)
        if changePin == 1:
            triggerLights()
        elif changePin == 2:
            triggerBuzzer()
        elif changePin == 3:
            triggerDoor()
        return render_template('home.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=False)
