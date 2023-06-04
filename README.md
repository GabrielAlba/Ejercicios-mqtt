# Ejercicios-mqtt \n
En este repositorio podemos encontrar las soluciones a los ejercicios propuesto sobre el protocolo mqtt:

1. Broker: En el script 01_broker, los usuarios que se conectan pueden establecer una conexión MQTT 
con un broker y realizar algunas operaciones básicas de publicación y suscripción.

2. Numbers: En el script 02_numbers un cliente mqtt lee el topic "numbers" y que realiza tareas con los
números leídos ,por ejemplo, separar los enteros y reales, y estudia propiedades (como ser o no primo) en los enteros.

3. Temperatures: En el script 03_temperatures un cliente mqtt que lee los subtopics y dado un intervalo de tiempo calcula la temperatura máxima, mínima y media para cada sensor y de todos los sensores.

4. Temperature & Humidity: En el script 04_temperature&humidity un cliente mqtt lee un
termómetro y, si su valor supera una determinada temperatura, K0, entonces pase a escuchar
también en el topic humidity. Si la temperatura baja de K0 o el valor de humidity sube de
K1 entonces el cliente dejará de escuchar en el topic humidity.

5. Timer: En el script 05_timer un cliente mqtt funciona como temporizador. El cliente leerá
mensajes en un topic dado y tendrá que encargarse de esperar el tiempo adecuado y luego publicar el 
mensaje en dicho topic.

6. Chain: En el script 06_chain diferentes clientes mqtt encadenan sus comportamientos.
