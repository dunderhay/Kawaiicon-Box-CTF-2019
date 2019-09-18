
import RPi.GPIO as GPIO
import pigpio, os, signal, time, sqlite3, hashlib, pygame
from flask import Flask, render_template, redirect, url_for, request, session, abort, url_for

app = Flask(__name__)
dir = os.path.dirname(__file__)

redPin   = 26
servoPin = 17
pi = pigpio.pi()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

def setup():
    pi.set_servo_pulsewidth(servoPin, 2500)
    pi.write(redPin, 0)
    bgmusic()

def end(signal,frame):
    print ('\n[*] Cleaning up...\nBye!')
    pi.write(redPin, 0)
    pi.set_servo_pulsewidth(servoPin, 2500)
    pygame.mixer.music.stop()
    GPIO.cleanup()
    exit(1)

signal.signal(signal.SIGINT, end)

def bgmusic():
    pygame.mixer.music.load(os.path.join(dir, 'static/bg.wav'))
    pygame.mixer.music.play(-1)

def wow():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(dir, 'static/wow.wav'))
    pygame.mixer.music.play()

def openmusic():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(dir, 'static/open.wav'))
    pygame.mixer.music.play()

def triggerLights():
    pi.write(redPin, 1)
    time.sleep(6)
    pi.write(redPin, 0)

def triggerRick():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(dir, 'static/rick.wav'))
    pygame.mixer.music.play()

def triggerDoor():
    pi.set_servo_pulsewidth(servoPin, 1000)
    time.sleep(6)
    pi.set_servo_pulsewidth(servoPin, 2500)

def hash_pass(password):
        return hashlib.sha256(password.encode()).hexdigest()

setup()

## Routing
# Route for handling index page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('home.html')

# Route for handling home page
@app.route('/home')
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
            username, password = (request.form['username'], request.form['password'])
            try:
                con = sqlite3.connect(os.path.join(dir, 'static/user.db'))
                with con:
                    cur = con.cursor()
                    cur.execute('SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"' % (username, hash_pass(password)))
                    if cur.fetchone():
                        wow()
                        time.sleep(2)
                        bgmusic()
                        session['logged_in'] = True
                        return redirect(url_for('home'))
                    else:
                        error = 'Invalid Credentials'
            except sqlite3.Error as e:
                error = e
            except Exception as e:
                error = e
            finally:
                if con:
                    con.close()
        return render_template('login.html', error=error)

# Route for handling the logout page logic
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# Route for handling GPIO / setting pins on and off
@app.route('/trigger/<changePin>/on')
def action(changePin):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        changePin = int(changePin)
        if changePin == 1:
            triggerLights()
        elif changePin == 2:
            triggerRick()
            time.sleep(4)
            bgmusic()
        elif changePin == 3:
            openmusic()
            triggerDoor()
            bgmusic()
        return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080, debug=False)
