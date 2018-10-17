# Hass notifications
This will trigger notifications from Hass websocket in OSX / Winndows (and soon android)

## Installation
```bash
pip3 install -r requirements.txt
```
(Optional)
```bash
pip3 install -r requirements_osx.txt
```

## Example:
```bash
$ python3 hass-native/main.py -h ws://localhost:8123/api/websocket -t api_token
```

## Warning
This is just a proof of concept, it will display ALL notifications atm. and that might not suit everyone.

## Plans
The goal is to create a cross-plattform "native"-application for kiosk-mode, just notifications or both.