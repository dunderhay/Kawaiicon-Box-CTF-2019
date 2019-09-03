# RPi Web App Challenge

Raspberry Pi running a flask web-server. Used to control a servo that can unlock one of the doors to a level.

## Running the webserver

The web-server can be run using the following command:
`python open.py`

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

## Challenges
### Challenge \#1
A login page with weak admin credentials. Participants should be able to guess the credentials to gain access to the admin page, which allows the attacker to unlock a door via the GPIO pins on the RPi.

### Challenge \#2
Participants will be able to interact with GPIO pins on the RPi once authenticated to the website. An IDOR vulnerability exists within the function that controls GPIO pins.
