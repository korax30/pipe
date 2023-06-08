import paho.mqtt.client as mqtt
import time
import numpy as np
import redis


mqtt_broker="f4df993babc3449d8632c18cafa5c65d.s2.eu.hivemq.cloud"
mqtt_port=8883
mqtt_username="FelipeMqtt"
mqtt_password="Sanpipe03."
mqtt_topic1="Luz"
mqtt_topic2="Personas"
mqtt_topic3="valorluz"
luz=[0]
personas=[0]
valorluz=[0]
per_ant=0
luz_ant=0
valorluz_ant=0
r = redis.Redis(
    host ='redis-12293.c9.us-east-1-4.ec2.cloud.redislabs.com',
    port=12293,  
    password='vYP6uC9pgQzIQ1PpjgzbrtURZqdGD8bQ')
 
ts = r.ts()
ts.create("personas")
ts.create("luz")
ts.create("valorluz")
ts.create("media_luz")
ts.create("media_personas")
ts.create("percentil_luz25")
ts.create("percentil_luz75")

def publicar_redis_personas():
ts.add("personas", "*",int(personas[len(personas)-1]))


def publicar_redis_luz():
ts.add("luz", "*",int(luz[len(luz)-1]))



def publicar_redis_valorluz():
ts.add("valorluz", "*",int(valorluz[len(valorluz)-1]))


def ciencia_datos(var):
global media_luz,percentiles_luz,media_personas
if var==2:
luz2=list(map(int,luz))
media_luz=sum(luz2)/len(luz2)
percentiles_luz=np.percentile(luz2,[25,50,75])
ts.add("media_luz", "*",media_luz)
ts.add("percentil_luz25", "*",percentiles_luz[0])
ts.add("percentil_luz75", "*",percentiles_luz[2])
if var==1:
personas2=list(map(int,personas))
media_personas=sum(personas2)/len(personas2)
ts.add("media_personas", "*",media_personas)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Conexión exitosa al broker MQTT')
        # Suscribirse al topic
        client.subscribe(mqtt_topic1)
        client.subscribe(mqtt_topic2)
        client.subscribe(mqtt_topic3)
    else:
        print('No se pudo conectar al broker MQTT')

def on_message(client, userdata, msg):
    # Obtener los datos del mensaje recibido
global luz,personas,per_ant,luz_ant,valorluz,valorluz_ant
data = msg.payload.decode('utf-8')
topic=msg.topic
    # Hacer algo con los datos obtenidos
#time.sleep(1)
if topic == mqtt_topic1:
luz.append(data)
#print(data)
elif topic == mqtt_topic2:
personas.append(data)

elif topic == mqtt_topic3:
valorluz.append(data)

if not personas[len(personas)-1] == per_ant:
publicar_redis_personas()
per_ant=personas[len(personas)-1]
ciencia_datos(1)
if not luz[len(luz)-1] == luz_ant:
publicar_redis_luz()
luz_ant=luz[len(luz)-1]
ciencia_datos(2)
if not valorluz[len(valorluz)-1] == valorluz_ant:
publicar_redis_valorluz()
valorluz_ant=valorluz[len(valorluz)-1]
#print(personas[len(personas)-1])
   

# Crear un cliente MQTT
client = mqtt.Client()

# Configurar el cliente MQTT
client.username_pw_set(mqtt_username, mqtt_password)
client.tls_set()

# Asignar los callbacks de conexión y recepción de mensajes
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker, mqtt_port)


# Mantener la conexión MQTT en ejecución
client.loop_forever()