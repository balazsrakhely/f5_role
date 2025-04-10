# Ansible role cetinhu.f5.vs

Create a virtual server in F5 

## Task: main.yaml

### Parameters

| Parameter | Type | Flags | Default | Description |
| --- | --- | --- | --- | --- |
| f5_cred.f5_user | string | mandatory | | F5 provider user |
| f5_cred.f5_password | string | mandatory | | F5 provider password |
| f5_cred.f5_hosts | string | mandatory | | F5 provider hosts (comma separated list, 2 items) |
| vs_name | string | mandatory | | The name of the virtual server, full name convention: <vs_name>_<vs_protocol><vs_port>_vs, e.g.: myvirtualserver_tcp443_vs |
| vs_address | string | mandatory | | The address of the virtual server |
| vs_vlans | string | mandatory | | Enabled VLANs for the virtual server. Comma separated list |
| provider_server_port | int | optional | 443 | The port the hosts are accessible on |
| provider_omit_telemetry | bool | optional | true | Whether to use telemetry |
| provider_transport | string | optional | rest | The transport connection to use |
| provider_validate_certs | bool | optional | false | If false, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates. |
| partition | string | optional | Common | The partition in which the resources should be created |
| vs_port | string | optional | 443 | Port of the virtual server. If 0, the virtual server listens on any port. (can be a number or the name of the port) |
| vs_protocol | string | optional | tcp | The network protocol for the traffic on the virtual server |
| vs_pool | string | optional | | The pool name the virtual server should use |

### Functionality

Steps:

1. Validate presence of mandatory provider credentials

2. From the provided 2 hosts, select the active one and use it in later steps

3. Validate the presence of mandatory virtual server parameters (name, address, vlans)

4. Create the virtual server with the provided parameters

### Examples

```yaml
- name: Create virtual server
  ansible.builtin.include_role:
    name: cetinhu.f5.vs
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    vs_name: myvirtualserver
    partition: My_partition
    vs_address: 192.168.10.10
    vs_vlans: VLAN1,VLAN2
```

```yaml
- name: Create virtual server with pool
  ansible.builtin.include_role:
    name: cetinhu.f5.vs
  vars:
    f5_cred:
        f5_user: apiuser
        f5_password: apipassword
        f5_hosts: 10.10.10.10,10.10.10.11
    vs_name: myvirtualserver
    partition: My_partition
    vs_address: 192.168.10.10
    vs_vlans: VLAN1
    pool: mypool
```
