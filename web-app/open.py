import pigpio
import os
import signal
from flask import Flask, render_template, redirect, url_for, request, session, abort, url_for

app = Flask(__name__)

redPin   = 26
servoPin = 17
pi = pigpio.pi()

def end(signal,frame):
    print ("\n[*] Cleaning up...\nBye!")
    pi.write(redPin, 0)
    pi.set_servo_pulsewidth(servoPin, 2500)
    exit(1)

signal.signal(signal.SIGINT, end)

pins = {
        redPin : {'name' : 'redPin', 'state' : pi.write(redPin, 0)}
}

spins = {
        servoPin : {'name' : 'servoPin', 'state' : pi.set_servo_pulsewidth(servoPin, 2500)}
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
            pins[pin]['state'] = pi.read(pin)
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
        if changePin == 26 and action == "on":
            pi.write(redPin, 1)
        elif changePin == 17 and action == "on":
            pi.set_servo_pulsewidth(servoPin, 1000)
        elif changePin == 26 and action == "off":
            pi.write(redPin, 0)
        elif changePin == 17 and action == "off":
            pi.set_servo_pulsewidth(servoPin, 2500)
        for spin in spins:
            spins[spin]['state'] = pi.read(spin)
        for pin in pins:
            pins[pin]['state'] = pi.read(pin)
        templateData = {
            'pins' : pins
        }
        return render_template('home.html', **templateData)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=False)
