# Importing necessary modules
from machine import Pin, PWM, ADC, UART, time_pulse_us
from time import sleep, sleep_us, ticks_ms, ticks_diff
from dht import DHT22
from network import WLAN, STA_IF
import BlynkLib

# Important variables
dist_threshold = 30
gas_threshold = 3628
distance_limit = 30000
sound_speed = 0.0343
servo_max_duty = 127 # When servo reaches 180 degrees
time_to_send_data = 250
TRIG_PIN = 12
ECHO_PIN = 13
DHT22_PIN = 32
GAS_DIGITAL = 33
LOCK_SERVO = 23
DOOR_SERVO = 22
SERVO_FREQ = 50
ANGLE_OPEN = 180
ANGLE_CLOSED = 0
LED_PIN = 27
TX, RX = 17, 16
BAUDRATE = 9600
temp = 0
hum = 0
near = None
door_status = None
gas_alert = None

# Ultrasonic sensor setup (Distance)
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# DHT22 setup (Temperature and Humidity)
dht22 = DHT22(Pin(DHT22_PIN))

# MQ2 setup (Gas)
mq2_digital = Pin(GAS_DIGITAL, Pin.IN)

# Servos setup
lock = PWM(Pin(LOCK_SERVO), freq=SERVO_FREQ)
door = PWM(Pin(DOOR_SERVO), freq=SERVO_FREQ)

# LED setup (This will be used to alert people that there is a gas leak)
led = Pin(LED_PIN, Pin.OUT)

# UART communication setup
uart = UART(2, baudrate=BAUDRATE, tx=Pin(TX), rx=Pin(RX))

# Wi-Fi setup
ssid = "Wokwi-GUEST"
password = "" # No password needed for a free acess point
wifi = WLAN(STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Connecting to WIFI")

while not wifi.isconnected():
  print("Connecting")
  sleep(1)
print("Connected sucessfully")

# Blynk setup (DON'T SHARE AUTH TOKEN)
TEMPLATE_ID = "TMPL27hVw279T"
TEMPLATE_NAME = "Semester 1 Project"
AUTH_TOKEN = "HUtihqrylTVrfuW8MZZ6hCugkiZDnMlL"
blynk = BlynkLib.Blynk(AUTH_TOKEN, tmpl_id=TEMPLATE_ID, insecure=True)

# Getting distance from ultrasonic function
def get_distance():
  # Setting up a 10 μs pulse from trigger pin
  trig.off()
  sleep_us(2)
  trig.on()
  sleep_us(10)
  trig.off()

  # Getting the duration of the pulse from echo pin
  duration = time_pulse_us(echo, 1, distance_limit)

  # Getting the distance in cm
  # We are dividing by 2 because the signal travels
  # back and forth
  distance = (duration * sound_speed) / 2

  # Error check (Distance can't be negative)
  if distance < 0:
    return 9999

  # returning result
  return distance

# Servo control function
def set_servo_angle(servo, angle):
  # Angle to duty equation
  duty = int((1023 * ((2 * angle / 180) + 0.5)) / 20)

  # Setting servo angle
  servo.duty(duty)

# Getting data from DHT22 function
def get_temp_and_hum():
  dht22.measure()
  temp = dht22.temperature()
  hum = dht22.humidity()

  # Returning data in a list (each one of them rounded to 1 decimal place)
  return [round(temp, 1), round(hum, 1)]

# Getting data from mq2
def get_gas():
  gas_digital = mq2_digital.value()

  # Returning data
  # 0 means dangerous
  # 1 means safe
  return gas_digital

# Blynk important functions
@blynk.on("connected")
def blynk_connected():
  print("Blynk is connected")

def update():
  # Get all data
  gas = get_gas()
  distance = get_distance()
  dht = get_temp_and_hum()
  temp = dht[0]
  hum = dht[1]

  # Writing safe or dangerous to V1 in blynk
  blynk.virtual_write(1, 1 if not gas else 0)

  # Writing temperature and humidity levels
  blynk.virtual_write(3, temp)
  blynk.virtual_write(4, hum)

  # door configuration
  if distance <= 30 or not gas:
    set_servo_angle(lock, ANGLE_OPEN)
    sleep(0.5)
    set_servo_angle(door, ANGLE_OPEN)
    blynk.virtual_write(0, "Open")
    door_status = True
    near = True
  else:
    set_servo_angle(door, ANGLE_CLOSED)
    sleep(0.5)
    set_servo_angle(lock, ANGLE_CLOSED)
    blynk.virtual_write(0, "Closed")
    door_status = False
    near = False

  # Gas leakage detector (ON = 1, OFF = 0)
  if not gas:
    led.on()
    blynk.virtual_write(2, 1)
    gas_alert = True
    door_status = True
  else:
    led.off()
    blynk.virtual_write(2, 0)
    gas_alert = False
    door_status = False

  # This will be used for sending data via UART to the other ESP32
  return [door_status, near, gas_alert, temp, hum]

def main():
  last_activity = 0
  last_dht_reading = 0

  while True:
    # Starting a timer
    now = ticks_ms()

    # Running blynk
    blynk.run()

    # Catching exceptions while running code
    try:
        # Setup for a non blocking timer
        if ticks_diff(now, last_activity) >= time_to_send_data:
            last_activity = now
            special_list = update()

            # Getting data
            door_status = special_list[0]
            near = special_list[1]
            gas_alert = special_list[2]
            temp = special_list[3]
            hum = special_list[4]

            # Formatting it then sending it via UART
            data = f"{temp},{hum},{near},{door_status},{gas_alert}\n"
            uart.write(data)
            print("Sent: ", data)
    # Error Detector
    except Exception as e:
        print(e)

    sleep(0.02) # Main loop delay

if __name__ == "__main__":
    main() # Code runner
