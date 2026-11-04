from num_add import add
from num_sub import subtract

from num_interfaces.srv import Compute
from num_nodes.calc_server import CalcServer


def test_handlers_use_python_packages():
    for op, expected in ((add, 5.0), (subtract, -1.0)):
        response = CalcServer._handler(op)(Compute.Request(a=2.0, b=3.0), Compute.Response())
        assert response.result == expected
