from paho.mqtt.client import Client

TEMP = "temperature"
HUMIDITY = "humidity"

def on_message(mqttc, data, msg):
    # Imprime información sobre el mensaje recibido
    print(f"message:{msg.topic}:{msg.payload}:{data}")
    
    if data["status"] == 0:
        # Convierte el payload del mensaje en un entero
        temp = int(msg.payload) 
        
        if temp > data["temp_threshold"]:
            # Si la temperatura supera el umbral, se suscribe a la temperatura
            print(f"umbral superado {temp}, suscribiendo a humidity")
            mqttc.subscribe(HUMIDITY)
            data["status"] = 1
    
    elif data["status"] == 1:
        if msg.topic == HUMIDITY:
            # Si el mensaje es sobre la humedad, convierte el payload en un entero
            humidity = int(msg.payload)
            
            if humidity > data["humidity_threshold"]:
                # Si la humedad supera el umbral, cancela la suscripción a la humedad
                print(f"umbral humedad {humidity} superado, cancelando suscripción")
                mqttc.unsubscribe(HUMIDITY) 
                data["status"] = 0
        
        elif TEMP in msg.topic:
            # Si el mensaje es sobre la temperatura, convierte el payload en un entero
            temp = int(msg.payload)
            
            if temp <= data["temp_threshold"]:
                # Si la temperatura está por debajo del umbral, cancela la suscripción a la humedad
                print(f"temperatura {temp} por debajo de umbral, cancelando suscripción")
                data["status"] = 0
                mqttc.unsubscribe(HUMIDITY)
                
    
def main(broker):
    data = {
        "temp_threshold": 20,
        "humidity_threshold": 80,
        "status": 0
    }
    
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.connect(broker)
    
    # Se suscribe al topic de temperatura t1
    mqttc.subscribe(f"{TEMP}/t1")
    
    mqttc.loop_forever()
    
    
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Imprime el uso correcto del script si no se proporciona un broker
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
        
    broker = sys.argv[1]
    main(broker)
