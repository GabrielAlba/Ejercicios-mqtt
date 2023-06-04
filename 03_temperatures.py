from paho.mqtt.client import Client
from statistics import mean

# Variables para almacenar los valores de temperatura
temperatures = {}

def on_message(client, userdata, msg):
    # Obtener el subtema y el valor de temperatura del mensaje
    topic = msg.topic
    temperature = float(msg.payload.decode())

    # Obtener el nombre del sensor a partir del subtema
    sensor_name = topic.split('/')[-1]

    # Actualizar los valores de temperatura para el sensor actual
    if sensor_name not in temperatures:
        temperatures[sensor_name] = [temperature]
    else:
        temperatures[sensor_name].append(temperature)

    # Calcular los valores máximo, mínimo y promedio para cada sensor
    max_temp = max(temperatures[sensor_name])
    min_temp = min(temperatures[sensor_name])
    avg_temp = mean(temperatures[sensor_name])

    # Calcular los valores máximo, mínimo y promedio para todos los sensores
    all_max_temp = max([max(temps) for temps in temperatures.values()])
    all_min_temp = min([min(temps) for temps in temperatures.values()])
    all_avg_temp = mean([mean(temps) for temps in temperatures.values()])

    # Imprimir los resultados
    print(f"Sensor: {sensor_name}")
    print(f"Temperatura máxima: {max_temp}")
    print(f"Temperatura mínima: {min_temp}")
    print(f"Temperatura promedio: {avg_temp}")
    print()
    print("Todas las temperaturas:")
    for sensor, temps in temperatures.items():
        print(f"Sensor: {sensor}")
        print(f"Temperatura máxima: {max(temps)}")
        print(f"Temperatura mínima: {min(temps)}")
        print(f"Temperatura promedio: {mean(temps)}")
        print()
    print("Todas las temperaturas (globales):")
    print(f"Temperatura máxima: {all_max_temp}")
    print(f"Temperatura mínima: {all_min_temp}")
    print(f"Temperatura promedio: {all_avg_temp}")
    print()


def main(broker):
    client = Client()
    client.on_message = on_message
    
    # Conectar al broker MQTT
    client.connect(broker)
    
    # Suscribirse a los subtemas de temperatura
    client.subscribe("temp1")
    client.subscribe("temp2")
    
    # Mantenerse conectado y procesar mensajes entrantes
    client.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
