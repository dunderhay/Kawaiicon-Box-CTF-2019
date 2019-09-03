#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import signal

redPin   = 37
greenPin = 35
bluePin  = 33
servoPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)
reader = SimpleMFRC522()
magicUID = "9dfdcc73df"
magicWord = "wootwoot"

continue_reading = True

def end(signal,frame):
    global continue_reading
    continue_reading = False
    print ("\n[*] Cleaning up...\nBye!")
    servo.stop()
    GPIO.cleanup()
    exit(1)

signal.signal(signal.SIGINT, end)

def grant_access():
    print("[+] Access Granted!")
    GPIO.output(bluePin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    servo.ChangeDutyCycle(5)
    time.sleep(6)
    servo.ChangeDutyCycle(12)
    time.sleep(1)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)
    return

def deny_access():
    print("[-] Access Denied - Try Harder!")
    GPIO.output(bluePin, GPIO.LOW)
    GPIO.output(redPin, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)
    return

print("[*] Place Card on Reader...\n[*] Ctrl+C to stop")

while continue_reading:
    cardUID, text = reader.read()
    GPIO.output(bluePin, GPIO.HIGH)

    if format(cardUID, "02x") == magicUID or text.find(magicWord) != -1:
      grant_access()

    else:
      deny_access()
