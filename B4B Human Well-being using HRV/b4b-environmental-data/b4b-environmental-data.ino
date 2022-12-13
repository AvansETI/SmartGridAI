#include <SPI.h>
#include <SD.h>
#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include "Adafruit_CCS811.h"
#include "RTClib.h"

#define LED_PIN_RED 7
#define LED_PIN_BLUE 8

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

Adafruit_CCS811 ccs;
RTC_DS1307 rtc;
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);
File file;
String location;
String errorLocation = "error.txt";

void setup() {

  pinMode(LED_PIN_BLUE, OUTPUT);
  pinMode(LED_PIN_RED, OUTPUT);

  dht.begin();

  #ifndef ESP8266
    while (!Serial); // wait for serial port to connect. Needed for native USB
  #endif

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  if (!SD.begin(4)) {
    digitalWrite(LED_PIN_RED, HIGH);
    while (1);
  }

  file = SD.open("test.txt", FILE_WRITE);
  if (file) {
    file.close();
  } else {
    // if the file didn't open, print an error:
    digitalWrite(LED_PIN_RED, HIGH);
    writeToSD(errorLocation, "Can't open file.");
  }

  if(!ccs.begin()){
    digitalWrite(LED_PIN_RED, HIGH);
    writeToSD(errorLocation, "Failed to start sensor! Please check your wiring.");
  }

  // Wait for the sensor to be ready
  while(!ccs.available());

  if (!rtc.begin()) {
    digitalWrite(LED_PIN_RED, HIGH);
    writeToSD(errorLocation, "Couldn't find RTC.");
    
    Serial.flush();
    while (1) delay(10);
  }

  if (!rtc.isrunning()) {
    
    // When time needs to be set on a new device, or after a power loss, the
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }

  setFileLocationToNow();

  //use tsl.begin() to default to Wire, 
  //tsl.begin(&Wire2) directs api to use Wire2, etc.
  if(!tsl.begin())
  {
    digitalWrite(LED_PIN_RED, HIGH);
    writeToSD(errorLocation, "There was a problem detecting the TSL2561 ... Check your wiring or I2C ADDR!");
  }
  
  /* Setup the sensor gain and integration time */
  configureSensor();
}

void loop() {
  digitalWrite(LED_PIN_BLUE, HIGH);
  delay(1000);
  digitalWrite(LED_PIN_BLUE, LOW);
  
  // Wait a minute between measurements.
  delay(59000);
  
  /* Get a new sensor event */ 
  sensors_event_t event;
  tsl.getEvent(&event);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    digitalWrite(LED_PIN_RED, HIGH);
    writeToSD(errorLocation, "Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  String light = "";
  if (event.light){
    light = event.light;
  }

  String co2 = "";
  String TVOC = "";
  if(ccs.available()){
    if(!ccs.readData()){
      co2 = ccs.geteCO2();
      TVOC = ccs.getTVOC();
    }
    else{
      digitalWrite(LED_PIN_RED, HIGH);
      writeToSD(errorLocation, "Failed to read from CO2 sensor!");
    }
  }

  DateTime time = rtc.now();

  // if the file opened okay, write to it:
  writeToSD(location, String(h) + "," + String(t) + "," + String(f) + "," + String(light) + "," + String(co2) + "," + String(TVOC) + "," + String(time.timestamp(DateTime::TIMESTAMP_FULL)));
  // Serial.println("Humidity: "+ String(h) + ", temp: " + String(t) + ", fahr:" + String(f) + ", light: " + String(light) + ", co2: " + String(co2) + ", TVOC: " + String(TVOC) + ",Time: " + String(time.timestamp(DateTime::TIMESTAMP_FULL)));
  // Serial.println(String(h) + "," + String(t) + "," + String(f) + "," + "," + String(co2) + "," + String(TVOC) + "," + String(time.timestamp(DateTime::TIMESTAMP_FULL)));

}

void writeToSD(String fileLocation, String line) {
  file = SD.open(fileLocation, FILE_WRITE);
  if (file) {

    file.println(line);
    // close the file:
    file.close();
  } else {
    // if the file didn't open, print an error:
    digitalWrite(LED_PIN_RED, HIGH);
  }
}

void configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  // tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  tsl.enableAutoRange(true);            /* Auto-gain ... switches automatically between 1x and 16x */
  
  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */
}

void setFileLocationToNow(void) {
  DateTime time = rtc.now();
  
  String timestamp = String(time.timestamp(DateTime::TIMESTAMP_FULL));
  timestamp.replace(':', '-');
  timestamp.replace("-", "");
  timestamp.remove(timestamp.length()-2, 2);
  timestamp.remove(0, 4);
  timestamp.remove(4, 1);
  location = String(timestamp) + ".txt";
}


