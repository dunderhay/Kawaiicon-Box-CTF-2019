# Web App Challenge

Raspberry Pi running a flask web-server. Used to control a servo that can unlock one of the doors to a level.

## Running the webserver

The web-server can be run using the following command: `python open.py`

However, the RPi is configured to start the web-server as the following system service:

Name: `/lib/systemd/system/box.service`

Content:

```
[Unit]
Description=Web Server Opener
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/web-server/open.py

[Install]
WantedBy=multi-user.target
```

## Setting up raspberry pi

_requires pigpio and pygames_

Install it: `sudo apt install pigpio`

Start dameon with: `sudo pigpiod`

`sudo apt-get install python-pygame`


## Firewall config

Open ssh for management
Open web admin port 8080

`ufw disallow`

`ufw enable ssh`

...


## Database Config

`sudo apt install sqlite3`

Create database in `/static/` dir and insert admin

`sqlite3 user.db`

`CREATE TABLE USERS(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL);`

`INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('admin', '3109ae030933b596b162e4717fc65bae94e11112109ba8b0d2990ed6fca941a2');`

(admin:matryoshka)


## Wifi Config

The RPi will broadcast a WiFi AP for participants to connect to. We need WiFi at boot so the `wpa_supplicant.conf` should have:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="📦"
    psk="oops"
    key_mgmt=WPA-PSK
}
```

## Challenges
### Challenge \#1
A login page with weak admin credentials. Participants should be able to guess the credentials to gain access to the admin page, which allows the attacker to unlock a door via the GPIO pins on the RPi.

### Challenge \#2
Participants will be able to interact with GPIO pins on the RPi once authenticated to the website. An IDOR vulnerability exists within the function that controls GPIO pins.

### Challenge \#3
Cracking WPA2 for those who do not pick lock:
https://null-byte.wonderhowto.com/how-to/hack-wi-fi-cracking-wpa2-passwords-using-new-pmkid-hashcat-attack-0189379/
