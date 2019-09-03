import RPi.GPIO as GPIO
import os
from flask import Flask, render_template, redirect, url_for, request, session, abort, url_for

app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Create dictionary called pins to store pin number, name and pin state
pins = {
        23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW}
}

spins = {
        24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
}

# Set each pin as an output and make it low
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for spin in spins:
    GPIO.setup(spin, GPIO.OUT)
    GPIO.output(spin, GPIO.LOW)

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
        if action == "on":
            GPIO.output(changePin, GPIO.HIGH)
        if action == "off":
            GPIO.output(changePin, GPIO.LOW)
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
