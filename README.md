# num_nodes

| Executable | Does |
|---|---|
| `counter_pub` | publishes `std_msgs/Int64` on `/counter` (param `rate_hz`) |
| `counter_sub` | logs `/counter` |
| `calc_server` | serves `/add`, `/subtract` (`num_interfaces/srv/Compute`) via `num_add` / `num_sub` |
| `calc_client` | calls both services for every counter value, publishes `/add_result`, `/subtract_result` |

Service introspection is enabled so `ros2 bag record --all` captures the service calls.
