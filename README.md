# Module michaellee1019:mpu6050_orientation
Is an extension of the Viam movement sensor model that provides an orientation vector using a Kalman filter.

## Model michaellee1019:mpu6050_orientation:mpu6050_orientation
A Viam sensor that provides an orientation vector using a Kalman filter. The source code was derived from [Kalman-Filter-Python-for-mpu6050 by rocheparadox](https://github.com/rocheparadox/Kalman-Filter-Python-for-mpu6050) and wrapped in a viam module to provide movement sensor readings through Viam.

### Configuration
```json
{
  "i2c_bus": <int>,
  "i2c_address": "<hex_address>"
}
```

### Attributes
The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `i2c_bus`     | int    | Required  | The I2C bus number to communicate with the MPU6050 chip. |
| `i2c_address` | string | Required  | The I2C address of the MPU6050 chip in hexadecimal format. Usually `"0x68"` for this sensor. |

### Configuration Example
```json
{
  "i2c_bus": 1,
  "i2c_address": "0x68"
}
```

### GetOrientation
The MovementSensor.GetOrientation response will return an Orientation vector that is a heading relative to its reset point. This reading is a bit different from the standard [Orientation vector of Viam](https://docs.viam.com/operate/reference/orientation-vector/). This model returns only X and Y vectors. Z and Theta are returned as 0.


### GetReadings
The GetReadings response will return a standard Orientation vector with key `orientation`. For example using the Python SDK the return value is :

```json
	{
		"_type": "orientation_vector_degrees",
		"ox": 29,
		"oy": 17,
		"oz": 0,
		"theta": 0
	}
```

### DoCommand
Due to gyro drift the orientation can become skewed over time. The model will internally start and keep track of angles even when GetOrientation/GetReadings are not called. To reset all internal measurements and calculations, call reset through DoCommand in the following way. All values will zero for a few seconds and then return new calculated angles.

```json
{
  "reset": true
}
```