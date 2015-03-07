import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_15", GPIO.OUT)
GPIO.setup("P8_17", GPIO.OUT)
GPIO.setup("P8_19", GPIO.OUT)

GPIO.output("P8_15", GPIO.LOW)
GPIO.output("P8_17", GPIO.LOW)
GPIO.output("P8_19", GPIO.LOW)