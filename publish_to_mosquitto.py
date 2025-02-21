import paho.mqtt.publish as publish
import random
import time


# Configurações do Mosquitto
MQTT_BROKER = "localhost"  # Endereço do broker Mosquitto
MQTT_PORT = 1883           # Porta padrão do MQTT
MQTT_TOPIC_1 = "random/number1"  # Tópico para o primeiro número
MQTT_TOPIC_2 = "random/number2"  # Tópico para o segundo número

# Função para obter dados da API Random Data API
def generate_random_decimal():
    return round(random.uniform(0, 70), 2)  # Gera um número decimal entre 0 e 70

# Loop principal
def main():
    while True:
        # Gerar dois números decimais diferentes
        data1 = generate_random_decimal() 
        data2 = generate_random_decimal()

        # Publicar os números decimais nos tópicos MQTT
        publish.single(MQTT_TOPIC_1, str(data1), hostname=MQTT_BROKER, port=MQTT_PORT)
        publish.single(MQTT_TOPIC_2, str(data2), hostname=MQTT_BROKER, port=MQTT_PORT)

        print(f"Dados publicados: {data1}, {data2}")

        time.sleep(60)  # Esperar 60 segundos antes de enviar o próximo dado

if __name__ == "__main__":
    main()