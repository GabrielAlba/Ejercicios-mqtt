
from paho.mqtt.client import Client
from multiprocessing import Lock
import traceback
import time

def on_connect(mqttc, userdata, flags, rc):
    try:
        print("CONNECT:", userdata, flags, rc)
    except:
        traceback.print_exc()

def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload)
    lock = userdata['lock']
    lock.acquire()
    try:
        userdata['count'] += 1
        a=1
        if a/0 == 0:
            mqttc.publish(userdata['topic_p'], msg.payload)
    except:
        traceback.print_exc()
    finally:
        lock.release()


def on_publish(mqttc, userdata, mid):
    try:
        print("PUBLISH:", userdata, mid)
    except:
        traceback.print_exc()


def on_subscribe(mqttc, userdata, mid, granted_qos):
    try:
        print("SUBSCRIBED:", userdata, mid, granted_qos)
    except:
        traceback.print_exc()


def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)


def main(broker, topic_s, topic_p):
    userdata = {
        'count': 0,
        'topic_s': topic_s,
        'topic_p': topic_p,
        'lock': Lock()
    }
    mqttc = Client(userdata = userdata)
    #mqttc.enable_logger()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    #mqttc.on_log = on_log

    #mqttc.connect("localhost")
    mqttc.connect(broker)

    mqttc.subscribe(topic_s)

    mqttc.loop_start()
    i = 0
    while True:
        mqttc.publish(topic_p, i)
        print(f'counter: {userdata["count"]}')
        i += 1
        time.sleep(5)

if __name__ == "__main__":
    import sys
    if len(sys.argv)<4:
        print(f"Usage: {sys.argv[0]} broker topic_s topic_p")
        sys.exit(1)
    broker = sys.argv[1]
    topic_s = sys.argv[2]
    topic_p = sys.argv[3]
    main(broker, topic_s, topic_p)

