"""Serve /add and /subtract using the num_add and num_sub Python packages."""
from num_add import add
from num_sub import subtract
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.service_introspection import ServiceIntrospectionState

from num_interfaces.srv import Compute


class CalcServer(Node):
    def __init__(self):
        super().__init__('calc_server')
        # Publish request/response events so rosbag2 can record the service calls.
        introspection = self.declare_parameter('introspection', True).value
        state = ServiceIntrospectionState.CONTENTS if introspection else ServiceIntrospectionState.OFF
        for name, op in (('add', add), ('subtract', subtract)):
            srv = self.create_service(Compute, name, self._handler(op))
            srv.configure_introspection(self.get_clock(), qos_profile_system_default, state)

    @staticmethod
    def _handler(op):
        def handle(request, response):
            response.result = float(op(request.a, request.b))
            return response
        return handle


def main():
    rclpy.init()
    try:
        rclpy.spin(CalcServer())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
