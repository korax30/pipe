#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

#define RTC_ADDR 0x51
#define LUX_ADDR 0x23

#define SDA_PIN 21
#define SCL_PIN 22

const char* ssid = "Felipee";
const char* password = "semeolvido";

const char* mqtt_server = "f4df993babc3449d8632c18cafa5c65d.s2.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_username = "FelipeMqtt";
const char* mqtt_password = "Sanpipe03.";

static const char* root_ca PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
)EOF";

WiFiClientSecure espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];

String cadena_rtc="";
const int ledPin = 19;
const int enc_1=18;
const int enc_2=5;
const int led=2;
int per_adentro=0;
int band=0;
int var_enc=0;
int luz_anterior=0;
int personas_anterior=0;
int vl=0;
int vlant=0;
void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(enc_1, INPUT);
  pinMode(led, OUTPUT);
  setup_wifi();
  espClient.setCACert(root_ca);
  client.setServer(mqtt_server, mqtt_port);


  Wire.begin(); // Iniciar comunicación I2C
  Wire.beginTransmission(SDA_PIN);
  Wire.beginTransmission(SCL_PIN);
 
}

void loop() {
  int e1=digitalRead(enc_1);
  int e2=digitalRead(enc_2);
  int luz_cadena = sensor_luz();
  //String rtc_cadena = sensor_RTC();
  if (luz_cadena<15)
  {
    var_enc=encoder(e1,e2);
    if(var_enc>0)
    {
      vl=encender_luz();
    }else{vl=apagar_luz();}
  }
  else if (luz_cadena>=15)
  {
    var_enc=encoder(e1,e2);
    vl=apagar_luz();
  }  
 
 if (!client.connected()) reconnect();
  client.loop();

  if (luz_cadena != luz_anterior) {
    client.publish("Luz", String(luz_cadena).c_str(), true);
    luz_anterior = luz_cadena;
  }
  if (var_enc != personas_anterior) {
    client.publish("Personas", String(var_enc).c_str(), true);
    personas_anterior = var_enc;
  }
  if (vl != vlant) {
    Serial.print("enviado");
    client.publish("valorluz", String(vl).c_str(), true);
    vlant = vl;
  }
 
}

int encoder(int e1, int e2)
{

  if(e1==1 and e2==0)
  {
    while (e2==0 and band==0)
    {
      e2=digitalRead(enc_2);
      if(e2==1)
      {
        while(e2==1){e2=digitalRead(enc_2);}
        per_adentro=per_adentro+1;
        band=1;
        while (e1==1){e1=digitalRead(enc_1);}
      }
    }
    Serial.println(per_adentro);
    band=0;
    delay(1000);
  }
 
  else if(e2==1 and e1==0)
  {
    while (e1==0 and band==0)
    {
      e1=digitalRead(enc_1);
      if(e1==1)
      {
        while(e1==1){e1=digitalRead(enc_1);}
        if (per_adentro>0)
        {
          per_adentro=per_adentro-1;
        }  
        else{per_adentro=per_adentro;}
        //Serial.println(per_adentro);
        band=1;
        while (e2==1){e2=digitalRead(enc_2);}
      }
    }
    Serial.println(per_adentro);
    band=0;
    delay(1000);
  }
  return per_adentro;
}

int encender_luz()
{
  digitalWrite(ledPin, HIGH);
  return 1;
}
int apagar_luz()
{
  digitalWrite(ledPin, LOW);
  return 0;
}

int sensor_luz()
{
  Wire.beginTransmission(LUX_ADDR);
  Wire.write(0x10);
  Wire.endTransmission();
  Wire.requestFrom(0x23, 2);
  uint16_t lux = (Wire.read() << 8) | Wire.read();
  delay(150);
  return lux;
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(ledPin, HIGH);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  digitalWrite(ledPin, LOW);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}