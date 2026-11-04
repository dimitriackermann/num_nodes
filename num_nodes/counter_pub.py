"""Publish an increasing counter on /counter."""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int64


class CounterPub(Node):
    def __init__(self):
        super().__init__('counter_pub')
        rate = self.declare_parameter('rate_hz', 1.0).value
        self._pub = self.create_publisher(Int64, 'counter', 10)
        self._count = 0
        self.create_timer(1.0 / rate, self._tick)

    def _tick(self):
        self._count += 1
        self._pub.publish(Int64(data=self._count))


def main():
    rclpy.init()
    try:
        rclpy.spin(CounterPub())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
