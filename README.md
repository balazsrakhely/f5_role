# Ansible role cetinhu.f5.pool

Create a pool in F5 (and nodes in it if wanted to) 

## Task: main.yaml

### Parameters

| Parameter | Type | Flags | Default | Description |
| --- | --- | --- | --- | --- |
| f5_cred.f5_user | string | mandatory | | F5 provider user |
| f5_cred.f5_password | string | mandatory | | F5 provider password |
| f5_cred.f5_hosts | string | mandatory | | F5 provider hosts (comma separated list, 2 items) |
| pool_name | string | mandatory | | The name of the pool |
| pool_operation | string | mandatory | | Specifies what pool operation to do. Can be 'create', 'update' or 'remove' | 
| provider_server_port | int | optional | 443 | The port the hosts are accessible on |
| provider_validate_certs | bool | optional | true | If false, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates. |
| slow_ramp_time | int | optional | 120 | Sets the ramp-up time (in seconds) to gradually ramp up the load on newly added or freshly detected up pool members. |
| lb_algo | string | optional | round-robin | The load balancing method to use in the pool |
| partition | string | optional | Common | The partition in which the resources should be created |
| pool_port | string | optional | 443 | The service port the nodes are accessible on. (can be a number or the name of the port) |
| pool_health_monitor | string | optional | [] | Comma separated list of what health monitors the pools should use |
| node_list | string | optional | [] | This list of nodes will be created and added to the pool, or removed from the pool, based on the 'node_operation' parameter (add, remove) |
| node_operation | string | optional | 'add' | Specifies what operation to do with the list of nodes provided in the 'node_list' parameter. Can be 'add' or 'remove' |

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

Pre-Steps:

1. Validate presence of mandatory provider credentials

2. From the provided 2 hosts, select the active one and use it in later steps

Steps:

If 'pool_operation' equals 'create':

1. Create the pool with the provided parameters

2. If 'node_list' parameter is (correctly) provided, create those nodes

3. Add the 'node_list' nodes to the pool

If 'pool_operation' equals 'update' and 'node_operation' equals 'add':

1. If 'node_list' parameter is (correctly) provided, create those nodes

2. Add the 'node_list' nodes to the pool

If 'pool_operation' equals 'update' and 'node_operation' equals 'remove':

1. Remove 'node_list' nodes from the pool

If 'pool_operation' equals 'remove':

1. Remove pool

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
    pool_operation: create
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
    pool_operation: create
    partition: My_partition
    pool_health_monitor: tcp
    node_list:
        - address: 192.168.10.10
          description: "My 'xy' node"
        - address: 192.168.10.11
```

```yaml
- name: Remove pool
  ansible.builtin.include_role:
    name: cetinhu.f5.pool
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    pool_name: my_pool
    pool_operation: remove
    partition: My_partition
```

```yaml
- name: Add nodes to pool
  ansible.builtin.include_role:
    name: cetinhu.f5.pool
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    pool_name: my_pool
    pool_operation: update
    partition: My_partition
    pool_port: 443
    node_list:
        - address: 192.168.10.10
```

```yaml
- name: Remove nodes to pool
  ansible.builtin.include_role:
    name: cetinhu.f5.pool
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    pool_name: my_pool
    pool_operation: update
    partition: My_partition
    pool_port: 443
    node_operation: remove
    node_list:
        - address: 192.168.10.10
```
