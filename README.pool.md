# Ansible role cetinhu.f5.pool

Create a pool in F5 (and nodes in it if wanted to) 

## Task: main.yaml

### Parameters

| Parameter | Type | Flags | Default | Description |
| --- | --- | --- | --- | --- |
| f5_cred.f5_user | string | mandatory | | F5 provider user |
| f5_cred.f5_password | string | mandatory | | F5 provider password |
| f5_cred.f5_hosts | string | mandatory | | F5 provider hosts (comma separated list, 2 items) |
| pool_name | string | mandatory | | The name of the pool, full name convention: <pool_name>_<pool_protocol><pool_port>_pool, e.g.: mypool_tcp443_pool |
| provider_server_port | int | optional | 443 | The port the hosts are accessible on |
| provider_omit_telemetry | bool | optional | true | Whether to use telemetry |
| provider_transport | string | optional | rest | The transport connection to use |
| provider_validate_certs | bool | optional | false | If false, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates. |
| slow_ramp_time | int | optional | 120 | Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members. |
| lb_algo | string | optional | round-robin | The load balancing method to use in the pool |
| partition | string | optional | Common | The partition in which the resources should be created |
| pool_port | string | optional | 443 | The service port the nodes are accessible on. (can be a number or the name of the port) |
| pool_protocol | string | optional | tcp | The network protocol the load balancer uses |
| pool_health_monitor | string | optional | [] | Comma separated list of what health monitors the pools should use |
| nodes_to_create | string | optional | [] | If wanted to, nodes can be created and added to the pool as members. List of objects with fields: address, name |

**Load balancer algorith choices:**

- dynamic-ratio-member
- dynamic-ratio-node
- fastest-app-response
- fastest-node
- least-connections-member
- least-connections-node
- least-sessions
- observed-member
- observed-node
- predictive-member
- predictive-node
- ratio-least-connections-member
- ratio-least-connections-node
- ratio-member
- ratio-node
- ratio-session
- round-robin
- weighted-least-connections-member
- weighted-least-connections-node

### Functionality

Steps:

1. Validate presence of mandatory provider credentials

2. From the provided 2 hosts, select the active one and use it in later steps

3. If 'nodes_to_create' parameter is (correctly) provided, create those nodes
    Example of input parameter:
        nodes_to_create:
            - address: 192.168.10.10
              name: 192.168.10.10
            - address: 192.168.10.11
              name: mynode

4. Create the pool with the provided parameters

5. If there were nodes successfully created in step 3, add those nodes to the pool created in step 4

### Examples

```yaml
- name: Create pool
  ansible.builtin.include_role:
    name: cetinhu.f5.pool
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    pool_name: my_pool
    partition: My_partition
    pool_health_monitor: tcp
```

```yaml
- name: Create pool with nodes
  ansible.builtin.include_role:
    name: cetinhu.f5.pool
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    pool_name: my_pool
    partition: My_partition
    pool_health_monitor: tcp
    nodes_to_create:
        - address: 192.168.10.10
          name: 192.168.10.10
        - address: 192.168.10.11
          name: mynode
```
