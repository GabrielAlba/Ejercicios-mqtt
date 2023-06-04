from paho.mqtt.client import Client
import json


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        number = payload["number"]
        
        # Realizar tareas con los números leídos
        if isinstance(number, int):
            print(f"Se recibió un número entero: {number}")
            if is_prime(number):
                print(f"El número {number} es primo.")
            else:
                print(f"El número {number} no es primo.")
        elif isinstance(number, float):
            print(f"Se recibió un número real: {number}")
        else:
            print(f"Se recibió un valor inválido: {number}")
    except:
        print("Error al procesar el mensaje")

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main(broker):
    client = Client()
    client.on_message = on_message

    client.connect(broker)
    client.subscribe("numbers")

    client.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
