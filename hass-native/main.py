import json

import websocket
from plyer import notification
from plyer.utils import platform
import argparse

token = None

if platform == "macosx":
    import objc

    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    NSObject = objc.lookUpClass('NSObject')


    class NotificationDelegator(NSObject):

        def userNotificationCenter_didActivateNotification_(self, center,
                                                            notification):
            print("user notification center")

        def userNotificationCenter_shouldPresentNotification_(self, center,
                                                              notification):
            return True


def on_message(ws, message):

    def notify(
            title, subtitle, info_text, delay=1, sound=False,
            user_info={}):
        """ Python method to show a desktop notification in MACOSX
            title: Title of notification
            subtitle: Subtitle of notification
            info_text: Informative text of notification
            delay: Delay (in seconds) before showing the notification
            sound: Play the default notification sound
            userInfo: a dictionary that can be used to handle clicks in your
                      app's applicationDidFinishLaunching:aNotification method
        """
        delegator = NotificationDelegator.alloc().init()
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setSubtitle_(subtitle)
        notification.setInformativeText_(info_text)
        notification.setUserInfo_(user_info)
        if sound:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")
        center = NSUserNotificationCenter.defaultUserNotificationCenter()
        center.setDelegate_(delegator)
        center.deliverNotification_(notification)
    data = json.loads(message)
    if data['type'] == 'event':
        if platform == "macosx":
            notify(
                "Hass", data['event']['data']['service_data']['message'],
                "")
        else:
            notification.notify(
                "Hass", data['event']['data']['service_data']['message'])
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"auth","access_token":"%s"}' % token)
    ws.send(
        '{"id": 18,"type": "subscribe_events","event_type": "call_service"}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hass notifications')
    parser.add_argument('--host', '-H', dest='host',
                        help='The websocket adress for hass')
    parser.add_argument('--token', '-t', dest='token',
                        help='Token for your user.')
    websocket.enableTrace(True)
    host = parser.parse_args().host
    token = parser.parse_args().token
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
