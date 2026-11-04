"""Log every value received on /counter."""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int64


class CounterSub(Node):
    def __init__(self):
        super().__init__('counter_sub')
        self.create_subscription(Int64, 'counter', self._on_counter, 10)

    def _on_counter(self, msg):
        self.get_logger().info(f'counter = {msg.data}')


def main():
    rclpy.init()
    try:
        rclpy.spin(CounterSub())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
