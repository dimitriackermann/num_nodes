# num_nodes

| Executable | Does | Parameters (default) |
|---|---|---|
| `counter_pub` | publishes `std_msgs/Int64` on `/counter` | `rate_hz` (1.0): publish rate |
| `counter_sub` | logs `/counter` | `log_every` (1): log only every n-th value |
| `calc_server` | serves `/add`, `/subtract` (`num_interfaces/srv/Compute`) via `num_add` / `num_sub` | `introspection` (true): publish service events |
| `calc_client` | calls both services for every counter value, publishes `/add_result`, `/subtract_result` | `operand` (1.0): second operand `b` |

Set them with `ros2 run num_nodes counter_sub --ros-args -p log_every:=5`.

Service introspection (`calc_server` parameter `introspection`) is on by default, so `ros2 bag record --all` captures the service calls.
