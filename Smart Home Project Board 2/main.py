# Importing necessary modules
from machine import Pin, UART, I2C
from time import sleep, ticks_ms, ticks_diff
from pico_i2c_lcd import I2cLcd

# Important variables
SCL_PIN = 22
SDA_PIN = 21
TX, RX = 17, 16
num_of_fields = 5
i2c_address = 0x27
UART_TIMEOUT = 50 # 50ms

# I2C OLED setup
width = 16
height = 2

i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN)) # I2C setup
device = i2c.scan() # Scanning for devices (addr = 0x27)
# 0x27(hex) = 39(decimal)

# Detecting devices
if not device:
  print("No devices found")

print(device)
# LCD setup
lcd = I2cLcd(i2c, i2c_address, height, width)

# UART communication setup
uart = UART(2, baudrate=9600, tx=Pin(TX), rx=Pin(RX), timeout=UART_TIMEOUT)

# LCD writing function
def lcd_write(x: int, y: int, msg):
    lcd.move_to(x, y)
    m = str(msg)
    lcd.putstr(m)

# This function displays the readings on the lcd
def show_readings(temp, hum, near, door_status, gas_alert): 
  if gas_alert == "True":
    lcd.clear()
    lcd_write(0, 0, "GAS LEAK!!")
    lcd_write(0, 1, "EVACUATE NOW!!")
  else:
    lcd.clear()
    lcd_write(0, 0, f"T:{temp}C,H:{hum}%")
    lcd_write(0, 1, "Door: Open" if near == "True" else "Door: Closed")
    # If someone is near the door opens else it closes

last_data_recv = 0
interval = 250
previous_data = ""

lcd.clear() # Clearing anything from the LCD

while True:
  # Setting up a timer
  now = ticks_ms()

  # Checking if any data has been sent
  line = None
  if uart.any():
    line = uart.readline()

  if not line:
    continue

  try:
    # Decoding data
    text = line.decode("utf-8").strip()

    # This if statement prevents unnecessary changes in the LCD
    if text != previous_data and ticks_diff(now, last_data_recv) >= interval:
      # Extracting the data
      # This if statement checks that the data is split to 
      # exactly 5 fields (Delimiter: ",")
      if len(text.split(",")) == num_of_fields:
        print("Recv: ", text)
        t_str, h_str, n_str, d_str, g_str = text.split(",")

        # changing the types of data so we can process it
        temp = float(t_str)
        hum = float(h_str)
        near = n_str
        door_status = d_str
        gas_alert = g_str

        # Displaying the data
        show_readings(temp, hum, near, door_status, gas_alert)

        # Resetting everything
        previous_data = text
        last_data_recv = now

  except Exception as e:
    print("Parse Error: ", e)
        
    sleep(0.02) # Main loop delay
