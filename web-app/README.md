# Web App Challenge

Raspberry Pi running a flask web-server. Used to control a servo that can unlock one of the doors to a level.

## Running the webserver

The web-server can be run using the following command: `python open.py`

However, the RPi is configured to start the web-server as the following system service:

Name: `/lib/systemd/system/box.service`

Content:

```
[Unit]
Description=Starts the web application
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python /home/pi/web-app/open.py

[Install]
WantedBy=multi-user.target
```

## Setting up raspberry pi

_requires pigpio and pygames_

Install it: `sudo apt install pigpio`

Start dameon with: `sudo pigpiod`

`sudo systemctl enable pigpiod`

`sudo apt install python-pygame`


## Firewall config

`sudo apt install ufw`

`sudo ufw default deny incoming`

`sudo ufw default allow outgoing`

`sudo ufw limit ssh comment "Allow SSH"`

`sudo ufw allow 8080 comment "Allow administrator web portal"`

`sudo ufw allow proto udp from 0.0.0.0/0 to 0.0.0.0/0 port 67 comment "Allow dhcp"`

`sudo ufw enable`


## Database Config

`sudo apt install sqlite3`

Create database in `/static/` dir and insert admin

`sqlite3 user.db`

`CREATE TABLE USERS(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL);`

`INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('admin', '3109ae030933b596b162e4717fc65bae94e11112109ba8b0d2990ed6fca941a2');`

(admin:matryoshka)


## Wifi Config

`sudo apt install dnsmasq`
`sudo apt install hostapd`

The RPi will broadcast a WiFi AP for participants to connect to:

`sudo vim /etc/dhcpcd.conf`

```
interface wlan0
    static ip_address=192.168.20.1/24
    nohook wpa_supplicant

denyinterfaces wlan0
```

`sudo vim /etc/dnsmasq.conf`

```
interface=wlan0
listen-address=192.168.20.1
dhcp-range=192.168.20.3,192.168.20.254,255.255.255.0,24h
```

`sudo vim /etc/hostapd/hostapd.conf`

```
interface=wlan0
driver=nl80211
ssid=📦ฅ(＾・ω・＾ฅ)
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=2
wpa_passphrase=somethingsupersecure
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

`sudo vim /etc/default/hostapd`

```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

`sudo systemctl unmask hostapd`

`sudo systemctl enable hostapd`

## Challenges
### Challenge \#1
A login page with weak admin credentials. Participants should be able to guess the credentials to gain access to the admin page, which allows the attacker to unlock a door via the GPIO pins on the RPi.

### Challenge \#2
Participants will be able to interact with GPIO pins on the RPi once authenticated to the website. An IDOR vulnerability exists within the function that controls GPIO pins.

### Challenge \#3
Cracking WPA2 for those who do not pick lock:
https://null-byte.wonderhowto.com/how-to/hack-wi-fi-cracking-wpa2-passwords-using-new-pmkid-hashcat-attack-0189379/
