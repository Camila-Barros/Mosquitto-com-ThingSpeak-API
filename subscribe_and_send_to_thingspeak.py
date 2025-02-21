import paho.mqtt.client as mqtt
import requests

# Configurações do Mosquitto
MQTT_BROKER = "localhost"  # Endereço do broker Mosquitto
MQTT_PORT = 1883           # Porta padrão do MQTT
MQTT_TOPIC_1 = "random/number1"  # Tópico para o primeiro número
MQTT_TOPIC_2 = "random/number2"  # Tópico para o segundo número

# Configurações do ThingSpeak
THINGSPEAK_API_KEY = "6X4ZC0BSBVBRKOD3"  # Substitua pela sua chave WRITE_API
THINGSPEAK_URL = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"

# Variáveis para armazenar os valores dos campos
field1_value = None
field2_value = None

# Função para enviar dados para o ThingSpeak
def send_to_thingspeak(field1=None, field2=None):
    global field1_value, field2_value
    if field1_value is not None and field2_value is not None:
        url = f"{THINGSPEAK_URL}&field1={field1_value}&field2={field2_value}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Dados enviados com sucesso: Dispositivo1={field1_value}, Dispositivo2={field2_value}")
        else:
            print(f"Erro ao enviar dados: {response.status_code}")
        # Resetar os valores após o envio
        field1_value = None
        field2_value = None

# Callback quando uma mensagem é recebida
def on_message(client, userdata, message):
    global field1_value, field2_value
    topic = message.topic
    payload = message.payload.decode()  # Decodificar a mensagem

    if topic == MQTT_TOPIC_1:
        print(f"Dado 1 recebido: {payload}")
        field1_value = payload  # Armazenar o valor do Field 1
    elif topic == MQTT_TOPIC_2:
        print(f"Dado 2 recebido: {payload}")
        field2_value = payload  # Armazenar o valor do Field 2
    
    # Enviar dados para o ThingSpeak quando ambos os valores estiverem disponíveis
    if field1_value is not None and field2_value is not None:
        send_to_thingspeak()


# Configurar o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # Isso informa ao paho-mqtt que você está usando a versão 2 da API de callback.
client.on_message = on_message

# Conectar ao broker Mosquitto
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscrever ao tópico
client.subscribe(MQTT_TOPIC_1)
client.subscribe(MQTT_TOPIC_2)

# Manter a conexão e processar mensagens
print("Aguardando mensagens...")
client.loop_forever()