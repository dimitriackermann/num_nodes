"""Call /add and /subtract with (counter, operand) and publish the results."""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.service_introspection import ServiceIntrospectionState
from std_msgs.msg import Float64, Int64

from num_interfaces.srv import Compute


class CalcClient(Node):
    def __init__(self):
        super().__init__('calc_client')
        # Second operand b of every request: add(counter, b) / subtract(counter, b)
        self._operand = float(self.declare_parameter('operand', 1.0).value)
        self._ops = []
        for name in ('add', 'subtract'):
            client = self.create_client(Compute, name)
            client.configure_introspection(
                self.get_clock(), qos_profile_system_default,
                ServiceIntrospectionState.CONTENTS)
            pub = self.create_publisher(Float64, f'{name}_result', 10)
            self._ops.append((client, pub))
        self.create_subscription(Int64, 'counter', self._on_counter, 10)

    def _on_counter(self, msg):
        for client, pub in self._ops:
            if not client.service_is_ready():
                self.get_logger().warn(f'{client.srv_name} not available', throttle_duration_sec=5.0)
                continue
            future = client.call_async(Compute.Request(a=float(msg.data), b=self._operand))
            future.add_done_callback(
                lambda f, pub=pub: pub.publish(Float64(data=f.result().result)))


def main():
    rclpy.init()
    try:
        rclpy.spin(CalcClient())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
