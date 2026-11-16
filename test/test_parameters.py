from contextlib import contextmanager

import pytest
import rclpy
from std_msgs.msg import Int64

from num_nodes.calc_client import CalcClient
from num_nodes.calc_server import CalcServer
from num_nodes.counter_pub import CounterPub
from num_nodes.counter_sub import CounterSub


@contextmanager
def make_node(node_class, *params):
    """Create node_class with `name:=value` parameter overrides, as `--ros-args -p` would."""
    args = ['--ros-args'] + [a for p in params for a in ('-p', p)] if params else None
    rclpy.init(args=args)
    node = node_class()
    try:
        yield node
    finally:
        node.destroy_node()
        rclpy.shutdown()


@pytest.mark.parametrize('node_class, name, default', [
    (CounterPub, 'rate_hz', 1.0),
    (CounterSub, 'log_every', 1),
    (CalcServer, 'introspection', True),
    (CalcClient, 'operand', 1.0),
])
def test_parameter_defaults(node_class, name, default):
    with make_node(node_class) as node:
        assert node.get_parameter(name).value == default


def test_calc_client_uses_operand():
    with make_node(CalcClient, 'operand:=2.5') as node:
        assert node._operand == 2.5


def test_counter_sub_logs_every_nth(monkeypatch):
    with make_node(CounterSub, 'log_every:=3') as node:
        logged = []
        monkeypatch.setattr(node, 'get_logger', lambda: type('Log', (), {'info': logged.append})())
        for i in range(1, 8):
            node._on_counter(Int64(data=i))
        assert logged == ['counter = 3', 'counter = 6']


def test_calc_server_introspection_can_be_disabled():
    with make_node(CalcServer, 'introspection:=false') as node:
        assert node.get_parameter('introspection').value is False
