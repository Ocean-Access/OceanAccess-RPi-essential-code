import RPi.GPIO as IO
import time, sys

global count
count = 0
IO.setmode(IO.BCM)


FLOW_SENSOR_GPIO = 23
IO.setup(FLOW_SENSOR_GPIO,IO.IN,pull_up_down=IO.PUD_UP)

def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1
IO.add_event_detect(FLOW_SENSOR_GPIO, IO.FALLING, callback=countPulse)



while True:
    try:
        start_counter = 1
        time.sleep(10)
        start_counter = 0
        flow = (count / 367) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f Liter/min" % (flow))
        print("The count is: %s count" % (count))
        #publish.single("/Garden.Pi/WaterFlow", flow, hostname=MQTT_SERVER)
        count = 0
        time.sleep(5)
    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        IO.cleanup()
        sys.exit()
 