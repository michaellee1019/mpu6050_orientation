# mpu6050 with orientation 
A Viam module that returns sensor values from a capacitive touch sensor device with the MPR121 chip.

# Attributes
No configuration attributes are required. The module is built assuming the default I2C bus.

# GetReadings
The Sensor.GetReadings response will look like the following. A touchpads array contains the status of each pad/input to the device. True means that it is being touched, false means untouched. In the below example, input 0 is touched and 1-11 is untouched.

```json
	
{
  "touchpads": [
    true,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false,
    false
  ]
}

```