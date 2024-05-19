# michaellee1019:mpu6050_orientation:mpu6050_orientation
A Viam module that provides an orientation vector using a Kalman filter. The source code was derived from [Kalman-Filter-Python-for-mpu6050 by rocheparadox](https://github.com/rocheparadox/Kalman-Filter-Python-for-mpu6050) and wrapped in a viam module to provide movement sensor readings through Viam.

# Attributes
Specifying an `i2c_bus` attribute is required. `i2c_address` is optional and defaults to the standard address `0x68` for mpu6050 chips.

```json
{
  "i2c_bus": 1,
  "i2c_address": "0x68"
}
```

# GetOrientation
The MovementSensor.GetOrientation response will return a standard Orientation vector. This model returns only X and Y vectors. Z and Theta are returned as 0.


# GetReadings
The GetReadings response will return a standard Orientation vector with key `orientation`. For example using the Python SDK the return value is :

```json
	{"_type":"orientation_vector_degrees","ox":29,"oy":17,"oz":0,"theta":0}
```