#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pigpio
import time
import signal
from mfrc522 import SimpleMFRC522

redPin   = 26
greenPin = 19
bluePin  = 13
servoPin = 17
pi = pigpio.pi()
reader = SimpleMFRC522()
magicUID = "9dfdcc73df"
magicWord = "wootwoot"
continue_reading = True

def end(signal,frame):
    print ("\n[*] Cleaning up...\nBye!")
    global continue_reading
    continue_reading = False
    pi.write(bluePin, 0)
    close_door()
    GPIO.cleanup()
    exit(1)

signal.signal(signal.SIGINT, end)

def open_door():
    pi.set_servo_pulsewidth(servoPin, 1000)

def close_door():
    pi.set_servo_pulsewidth(servoPin, 2500)

def grant_access():
    print("[+] Access Granted!")
    pi.write(bluePin, 0)
    pi.write(greenPin, 1)
    open_door()
    time.sleep(6)
    close_door()
    time.sleep(1)
    pi.write(greenPin, 0)
    pi.write(bluePin, 1)
    return

def deny_access():
    print("[-] Access Denied - Try Harder!")
    pi.write(bluePin, 0)
    pi.write(redPin, 1)
    time.sleep(2)
    pi.write(redPin, 0)
    pi.write(bluePin, 1)
    return

close_door()
print("[*] Place Card on Reader...\n[*] Ctrl+C to stop")
pi.write(bluePin, 1)

while continue_reading:
    cardUID, text = reader.read()
    pi.write(bluePin, 1)
    if format(cardUID, "02x") == magicUID or text.find(magicWord) != -1:
      grant_access()
    else:
      deny_access()
