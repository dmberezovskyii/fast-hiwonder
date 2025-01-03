import time

from fast_sdk.line_sdk import InfraredSensors

sensor = InfraredSensors()
while True:
	data = sensor.read_sensor_data()
	print(
			"Sensor1:",
			data[0],
			" Sensor2:",
			data[1],
			" Sensor3:",
			data[2],
			" Sensor4:",
			data[3],
	)
	time.sleep(0.5)
