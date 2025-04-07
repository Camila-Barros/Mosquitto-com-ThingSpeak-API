# Mosquitto-com-ThingSpeak-API
Projeto testando o consumo de dados de uma API pelo Mosquitto e enviado a plataforma ThingSpeak, SEM autenticação de usuário e senha.

## Ferramentas

- [Eclipse Mosquitto](https://mosquitto.org/download/)
- [ThingSpeak](https://thingspeak.mathworks.com/)
- [Python](https://www.python.org/)


## Preparar o ThingSpeak:

<b>Criar um Canal:</b>
1. No painel do Thingspeak, clique em New Channel.
2. Preencha os campos:
    - <i>Name:</i> Nome do canal, que será o tópico assinado pelo Mosquitto.
    - <i>Description:</i> Descrição do canal (opcional).
    - <i>Field 1:</i> Dispositivo IoT 1.
    - <i>Field 2:</i> Dispositivo IoT 2.
3. Clique em Save Channel.
4. Anote a sua "<i>Write API Key </i>".



## Script de Publicação:

1. Crie um arquivo chamado publish_to_mosquitto.py.

2. Cole o seguinte código no arquivo:

  ```bash
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
    
            time.sleep(30)  # Esperar 30 segundos antes de enviar o próximo dado
    
    if __name__ == "__main__":
        main()
  ```

3. Salve o arquivo.



## Script de Subscrição e envio ao ThingSpeak:

1. Crie um arquivo chamado subscribe_and_send_to_thingspeak.py.

2. Cole o seguinte código no arquivo:

  ```bash
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
  ```

3. Substitua "SUA_WRITE_API_KEY" pela chave de API do canal criado.

4. Salve o arquivo.



## Executar os Scripts

<b>Mosquitto</b> 

1. Abra um Prompt de Comando ou PowerShell.
  
2. Reinicie o Mosquitto para aplicar as mudanças:

  ```bash
    net stop mosquitto
    net start mosquitto
  ```

<b>Publicação</b>

1. Abra um Prompt de Comando ou PowerShell.
 
2. Navegue até o diretório onde você salvou <i>publish_to_mosquitto.py</i>.

3. Execute o script:
  ```bash
    python publish_to_mosquitto.py
  ```

<b>Subscrição</b>

1. Abra um Prompt de Comando ou PowerShell.
 
2. Navegue até o diretório onde você salvou subscribe_and_send_to_thingspeak.py.

3. Execute o script:
  ```bash
    python subscribe_and_send_to_thingspeak.py
  ```

## Verificar os Dados no ThingSpeak

1. Acesse o seu canal no ThingSpeak.

2. Na aba "Private View", você verá um gráfico sendo atualizado com os números decimais enviados pelo script.

![image](https://github.com/Camila-Barros/Mosquitto-com-ThingSpeak-API/blob/main/ImgGraficos.png)






## Autora

Eng. Camila Cabral de Barros

Mestranda em Inovação Tecnológica pela UNIFESP

[Lattes](http://lattes.cnpq.br/2066462797590469)

