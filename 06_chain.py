from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep

def work_on_message(message, broker):
    # Procesa el mensaje recibido
    print("process body", message)
    
    # Extrae el topic, tiempo de espera y texto del mensaje
    topic, timeout, text = message[2:-1].split(",")
    print("process body", timeout, topic, text)
    
    # Espera el tiempo de espera especificado
    sleep(int(timeout))
    
    # Publica el mensaje en el topic correspondiente
    publish.single(topic, payload=text, hostname=broker)
    print("end process body", message)

def on_message(mqttc, userdata, msg):
    # Se ejecuta cuando se recibe un mensaje
    print("on_message", msg.topic, msg.payload)
    
    # Crea un nuevo proceso para manejar el mensaje
    worker = Process(target=work_on_message, args=(str(msg.payload), userdata["broker"]))
    worker.start()
    print("end on_message", msg.payload)

def on_log(mqttc, userdata, level, string):
    # Se ejecuta cuando se registra un mensaje de log
    print("LOG", userdata, level, string)

def on_connect(mqttc, userdata, flags, rc):
    # Se ejecuta cuando se establece la conexión MQTT
    print("CONNECT:", userdata, flags, rc)

def main(broker):
    # Configuración inicial
    userdata = {
        "broker": broker
    }
    
    # Crea una instancia del cliente MQTT
    mqttc = Client(userdata=userdata)
    
    # Habilita el registro de log
    mqttc.enable_logger()
    
    # Asigna las funciones de callback
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    
    # Conecta al broker MQTT
    mqttc.connect(broker)
    
    # Suscribe al topic donde se recibirán los mensajes
    topic = "clients/timeout"
    mqttc.subscribe(topic)
    
    # Mantiene el cliente MQTT en ejecución
    mqttc.loop_forever()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Imprime el uso correcto del script si no se proporciona un broker
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    
    broker = sys.argv[1]
    main(broker)

