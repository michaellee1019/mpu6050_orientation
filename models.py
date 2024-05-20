import sys

sys.path.append("..")

from UninterruptedAngleMeter.AngleMeterAlpha import AngleMeterAlpha
import viam_wrap
from viam.components.movement_sensor import MovementSensor
from viam.proto.app.robot import ComponentConfig
from typing import Any, Dict, Mapping, Optional, Self, Tuple
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.gen.common.v1.common_pb2 import Orientation, Vector3, GeoPoint
from viam.utils import ValueTypes


class MPU6050(MovementSensor):
    MODEL = "michaellee1019:mpu6050_orientation:mpu6050_orientation"
    angleMeter = None
    i2c_address = None
    i2c_bus: int = None

    @classmethod
    def new(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        output = self(config.name)
        output.reconfigure(config, dependencies)
        return output

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        self.i2c_bus = int(config.attributes.fields["i2c_bus"].number_value)
        if "i2c_address" in config.attributes.fields:
            self.i2c_address = int(config.attributes.fields["i2c_address"].string_value, base=16)
        self.reset()
        
    def reset(self):
        self.angleMeter = AngleMeterAlpha(i2c_bus=self.i2c_bus, address=self.i2c_address)
        self.angleMeter.measure()

    async def get_position(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Tuple[GeoPoint, float]:
        raise NotImplementedError

    async def get_linear_velocity(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Vector3:
        raise NotImplementedError

    async def get_angular_velocity(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Vector3:

        # w_x, w_y, w_z = self.angleMeter.getAngularVelocity()
        # return Vector3(x=w_x, y=w_y, z=w_z)
        raise NotImplementedError

    async def get_linear_acceleration(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Vector3:
        # v_x, v_y, v_z = self.angleMeter.getLinearVelocity()
        # return Vector3(x=v_x, y=v_y, z=v_z)
        raise NotImplementedError

    async def get_compass_heading(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> float:
        raise NotImplementedError

    async def get_orientation(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Orientation:
        return self.orientation()

    def orientation(self):
        roll = self.angleMeter.get_kalman_roll()
        pitch = self.angleMeter.get_kalman_pitch()
        return Orientation(o_x=roll, o_y=pitch, o_z=None, theta=None)

    async def get_properties(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> MovementSensor.Properties:
        return MovementSensor.Properties(
            linear_velocity_supported=False,
            angular_velocity_supported=False,
            orientation_supported=True,
            position_supported=False,
            compass_heading_supported=False,
            linear_acceleration_supported=False,
        )

    async def get_accuracy(
        self,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, float]:
        raise NotImplementedError


    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'reset':
                self.reset()
                result[name] = True
        return result

    async def get_readings(self, **kwargs):
        return {"orientation": self.orientation()}

if __name__ == "__main__":
    # necessary for pyinstaller to see it
    # build this with:
    # pyinstaller --onefile --hidden-import viam-wrap --paths $VIRTUAL_ENV/lib/python3.10/site-packages installable.py
    # `--paths` arg may no longer be necessary once viam-wrap is published somewhere
    # todo: utility to append this stanza automatically at build time
    viam_wrap.main(sys.modules.get(__name__))
