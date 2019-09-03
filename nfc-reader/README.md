# NFC Reader Challenge

## Setup
`python3 -m venv ./nf-venv`

`pip install -r requirements.txt`

`source nf-venv/bin/activate`

`python3 opensesame.py`


## Enabling Raspberry Pi SPI

To enable SPI for the Pi go to the configuration settings by executing:

`raspi-config`
Now select interface options and then SPI. Confirm with yes when prompted and reboot your Pi with:
