from paho.mqtt.client import Client
import time


def on_message(client, userdata, msg):
    # Decodifica el mensaje JSON recibido
    message = msg.payload.decode("utf-8")
    
    # Obtiene los datos del mensaje
    tiempo_espera = message["tiempo_espera"]
    topic = message["topic"]
    mensaje = message["mensaje"]
    
    # Espera el tiempo especificado
    time.sleep(tiempo_espera)
    
    # Publica el mensaje en el topic correspondiente
    client.publish(topic, mensaje)
    print(f"Mensaje publicado en el topic '{topic}': {mensaje}")
    
    
def main(broker):

    # Crear instancia del cliente MQTT
    client = Client()
    
    # Asignar funciones de callback
    client.on_message = on_message
    
    # Conectar al broker MQTT
    client.connect(broker)
    
    # Suscribirse al topic donde se recibirán los mensajes de temporización
    temporizador_topic = "temporizador"
    client.subscribe(temporizador_topic)
    
    # Mantener el cliente MQTT en ejecución
    client.loop_forever()
    
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Imprime el uso correcto del script si no se proporciona un broker
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
        
    broker = sys.argv[1]
    main(broker)