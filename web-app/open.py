import RPi.GPIO as GPIO
import os
import signal
from flask import Flask, render_template, redirect, url_for, request, session, abort, url_for

app = Flask(__name__)

redPin   = 37
servoPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)

def end(signal,frame):
    print ("\n[*] Cleaning up...\nBye!")
    servo.stop()
    GPIO.cleanup()
    exit(1)

signal.signal(signal.SIGINT, end)

pins = {
        37 : {'name' : 'GPIO 37', 'state' : GPIO.LOW}
}

spins = {
        11 : {'name' : 'GPIO 11', 'state' : servo.ChangeDutyCycle(12)}
}

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
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        templateData = {
            'pins' : pins
        }
        return render_template('home.html', **templateData)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
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
@app.route("/<changePin>/<action>")
def action(changePin, action):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        changePin = int(changePin)
        if changePin == 37 and action == "on":
            GPIO.output(redPin, GPIO.HIGH)
        elif changePin == 11 and action == "on":
            servo.ChangeDutyCycle(5)
        elif changePin == 37 and action == "off":
            GPIO.output(redPin, GPIO.LOW)
        elif changePin == 11 and action == "off":
            servo.ChangeDutyCycle(12)
        for spin in spins:
            spins[spin]['state'] = GPIO.input(spin)
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        templateData = {
            'pins' : pins
        }
        return render_template('home.html', **templateData)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=False)
