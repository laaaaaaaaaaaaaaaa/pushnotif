import pyrebase
from pusher_push_notifications import PushNotifications
import time

firebaseConfig = {
    'apiKey': "AIzaSyCluCynP5G1a_ISHYW6UXfoN81ZwGeoNb4",
    'authDomain': "falldetector-98d21.firebaseapp.com",
    'databaseURL': "https://falldetector-98d21-default-rtdb.firebaseio.com",
    'projectId': "falldetector-98d21",
    'storageBucket': "falldetector-98d21.appspot.com",
    'messagingSenderId': "976382816729",
    'appId': "1:976382816729:web:6194f4e5bb8246f210e9c8",
    'measurementId': "G-Q1HPYS1ZTB"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
beams_client = PushNotifications(
    instance_id='a4aa7582-e906-44b1-9bea-eadea0e6193d',
    secret_key='BC983486AD3B7A6998F0FDC172F4A15E0D076EB96D2B17F43A1A54736A7EDB8B',
)


def send_notif(title, body):
    response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={
            'apns': {
                'aps': {
                    'alert': title
                }
            },
            'fcm': {
                'notification': {
                 'title': title,
                'body': body
                }
            }
        }
    )
    print(response['publishId'])


def stream_handler_mpu(message):
        print(message)
        value = message['data']
        if value > 10000:
            value = db.child("/Sensor/Sensor Mpu/Value").get().val()
            send_notif('LANSIA TERDETEKS JATUH!', f'status: Bahaya {value} m')


data_path_mpu = "/Sensor/Sensor Mpu/Value"
my_stream_mpu = db.child(data_path_mpu).stream(stream_handler_mpu, None)