# app/utils/config/example_data.py
"""
Example data for demonstration and testing.
"""

# Example device context JSON as a string
EXAMPLE_DEVICE_CONTEXT = '''
{
    "name": "rack1_001_leaf1",
    "hostname": "rack1-001-leaf1",
    "reference_architecture": "two_stage_l3clos",
    "hcl": "leaf_dp",
    "slots": [
        0
    ],
    "ecmp_limit": 64,
    "deploy_mode": "deploy",
    "port_count": 10,
    "role": "leaf",
    "configured_role": "leaf",
    "model": "Juniper_leaf_dp",
    "lo0_ipv4_address": "172.16.0.0/32",
    "os": "Junos",
    "device_capabilities": {
        "copp_strict": false,
        "breakout_capable": {},
        "as_seq_num_supported": true
    },
    "dual_re": false,
    "os_selector": ".*",
    "asic": "T2",
    "system_tags": [],
    "device_sn": "rack1_001_leaf1_sn",
    "node_id": "9v5Z8FJ4My49knTZog",
    "blueprint_has_esi": false,
    "dhcp_servers": {
        "default": {
            "dhcp_servers": [],
            "dhcpv6_servers": [],
            "dhcp_source_ip": "",
            "dhcp_source_interface": "",
            "dhcp_source_ipv6": "",
            "vrf_name": "default"
        }
    },
    "interface": {
        "IF-et-0/0/1": {
            "name": "IF-et-0/0/1",
            "description": "facing_spine1:et-0/0/1",
            "role": "spine_leaf",
            "part_of": "",
            "composed_of": [],
            "switch_port_mode": "trunk",
            "native_vlan": "",
            "allowed_vlans": [],
            "mlag_id": "",
            "vrf_name": "default",
            "dhcp_servers": [],
            "dhcpv6_servers": [],
            "operation_state": "up",
            "ipv4_access_group_in": "",
            "ipv4_access_group_out": "",
            "ipv6_access_group_in": "",
            "ipv6_access_group_out": "",
            "dot1x_port_control": "force_authorized",
            "dot1x_auth_mode": "multi_host",
            "dot1x_mac_auth_bypass": false,
            "dot1x_reauthentication_timeout": null,
            "dot1x_fallback_vlan_id": null,
            "ospf_area": null,
            "ospf_process_id": null,
            "ospf_hello_timer": null,
            "ospf_dead_timer": null,
            "ospf_bfd": null,
            "ospf_mtu_ignore": null,
            "ospf_md5_key_id": null,
            "ospf_md5_key": null,
            "ospf_network_type": null,
            "lag_mode": null,
            "evpn_esi": null,
            "lacp_system_id": null,
            "subinterfaces": [],
            "mtu": 9170,
            "link_local_enable": false,
            "tags": [],
            "is_port_channel": false,
            "is_port_channel_member": false,
            "is_subinterface": false,
            "is_subinterface_portchannel": false,
            "is_subinterface_standalone": false,
            "has_subinterfaces": false,
            "is_standalone": true,
            "is_rail": false,
            "intf_tags": [],
            "rail_index": null,
            "rail_label": null,
            "intfName": "et-0/0/1",
            "type": "Interface",
            "port_setting": "",
            "index": 0
        },
        "IF-et-0/0/2": {
            "name": "IF-et-0/0/2",
            "description": "facing_spine2:et-0/0/1",
            "role": "spine_leaf",
            "part_of": "",
            "composed_of": [],
            "switch_port_mode": "trunk",
            "native_vlan": "",
            "allowed_vlans": [],
            "mlag_id": "",
            "vrf_name": "default",
            "dhcp_servers": [],
            "dhcpv6_servers": [],
            "operation_state": "up",
            "ipv4_access_group_in": "",
            "ipv4_access_group_out": "",
            "ipv6_access_group_in": "",
            "ipv6_access_group_out": "",
            "dot1x_port_control": "force_authorized",
            "dot1x_auth_mode": "multi_host",
            "dot1x_mac_auth_bypass": false,
            "dot1x_reauthentication_timeout": null,
            "dot1x_fallback_vlan_id": null,
            "ospf_area": null,
            "ospf_process_id": null,
            "ospf_hello_timer": null,
            "ospf_dead_timer": null,
            "ospf_bfd": null,
            "ospf_mtu_ignore": null,
            "ospf_md5_key_id": null,
            "ospf_md5_key": null,
            "ospf_network_type": null,
            "lag_mode": null,
            "evpn_esi": null,
            "lacp_system_id": null,
            "subinterfaces": [],
            "mtu": 9170,
            "link_local_enable": false,
            "tags": [],
            "is_port_channel": false,
            "is_port_channel_member": false,
            "is_subinterface": false,
            "is_subinterface_portchannel": false,
            "is_subinterface_standalone": false,
            "has_subinterfaces": false,
            "is_standalone": true,
            "is_rail": false,
            "intf_tags": [],
            "rail_index": null,
            "rail_label": null,
            "intfName": "et-0/0/2",
            "type": "Interface",
            "port_setting": "",
            "index": 1
        }
    },
    "ip": {
        "IP-et-0/0/1": {
            "name": "IP-et-0/0/1",
            "type": "IP",
            "intfName": "et-0/0/1",
            "description": "facing_spine1:et-0/0/1",
            "interface": {
                "name": "IF-et-0/0/1",
                "description": "facing_spine1:et-0/0/1",
                "role": "spine_leaf",
                "part_of": "",
                "composed_of": [],
                "switch_port_mode": "trunk",
                "native_vlan": "",
                "allowed_vlans": [],
                "mlag_id": "",
                "vrf_name": "default",
                "dhcp_servers": [],
                "dhcpv6_servers": [],
                "operation_state": "up",
                "ipv4_access_group_in": "",
                "ipv4_access_group_out": "",
                "ipv6_access_group_in": "",
                "ipv6_access_group_out": "",
                "dot1x_port_control": "force_authorized",
                "dot1x_auth_mode": "multi_host",
                "dot1x_mac_auth_bypass": false,
                "dot1x_reauthentication_timeout": null,
                "dot1x_fallback_vlan_id": null,
                "ospf_area": null,
                "ospf_process_id": null,
                "ospf_hello_timer": null,
                "ospf_dead_timer": null,
                "ospf_bfd": null,
                "ospf_mtu_ignore": null,
                "ospf_md5_key_id": null,
                "ospf_md5_key": null,
                "ospf_network_type": null,
                "lag_mode": null,
                "evpn_esi": null,
                "lacp_system_id": null,
                "subinterfaces": [],
                "mtu": 9170,
                "link_local_enable": false,
                "tags": [],
                "is_port_channel": false,
                "is_port_channel_member": false,
                "is_subinterface": false,
                "is_subinterface_portchannel": false,
                "is_subinterface_standalone": false,
                "has_subinterfaces": false,
                "is_standalone": true,
                "is_rail": false,
                "intf_tags": [],
                "rail_index": null,
                "rail_label": null,
                "intfName": "et-0/0/1",
                "type": "Interface",
                "port_setting": "",
                "index": 0
            },
            "ipv4_address": "172.16.0.19",
            "ipv4_prefixlen": 31,
            "ipv6_address": "",
            "ipv6_prefixlen": "",
            "vrf_name": "default",
            "subinterfaces": [],
            "link_local_enable": false,
            "dhcp_servers": [],
            "dhcpv6_servers": [],
            "ospf_area": null,
            "ospf_process_id": null,
            "ospf_hello_timer": null,
            "ospf_dead_timer": null,
            "ospf_bfd": null,
            "ospf_mtu_ignore": null,
            "ospf_md5_key_id": null,
            "ospf_md5_key": null,
            "ospf_network_type": null
        },
        "IP-et-0/0/2": {
            "name": "IP-et-0/0/2",
            "type": "IP",
            "intfName": "et-0/0/2",
            "description": "facing_spine2:et-0/0/1",
            "interface": {
                "name": "IF-et-0/0/2",
                "description": "facing_spine2:et-0/0/1",
                "role": "spine_leaf",
                "part_of": "",
                "composed_of": [],
                "switch_port_mode": "trunk",
                "native_vlan": "",
                "allowed_vlans": [],
                "mlag_id": "",
                "vrf_name": "default",
                "dhcp_servers": [],
                "dhcpv6_servers": [],
                "operation_state": "up",
                "ipv4_access_group_in": "",
                "ipv4_access_group_out": "",
                "ipv6_access_group_in": "",
                "ipv6_access_group_out": "",
                "dot1x_port_control": "force_authorized",
                "dot1x_auth_mode": "multi_host",
                "dot1x_mac_auth_bypass": false,
                "dot1x_reauthentication_timeout": null,
                "dot1x_fallback_vlan_id": null,
                "ospf_area": null,
                "ospf_process_id": null,
                "ospf_hello_timer": null,
                "ospf_dead_timer": null,
                "ospf_bfd": null,
                "ospf_mtu_ignore": null,
                "ospf_md5_key_id": null,
                "ospf_md5_key": null,
                "ospf_network_type": null,
                "lag_mode": null,
                "evpn_esi": null,
                "lacp_system_id": null,
                "subinterfaces": [],
                "mtu": 9170,
                "link_local_enable": false,
                "tags": [],
                "is_port_channel": false,
                "is_port_channel_member": false,
                "is_subinterface": false,
                "is_subinterface_portchannel": false,
                "is_subinterface_standalone": false,
                "has_subinterfaces": false,
                "is_standalone": true,
                "is_rail": false,
                "intf_tags": [],
                "rail_index": null,
                "rail_label": null,
                "intfName": "et-0/0/2",
                "type": "Interface",
                "port_setting": "",
                "index": 1
            },
            "ipv4_address": "172.16.0.51",
            "ipv4_prefixlen": 31,
            "ipv6_address": "",
            "ipv6_prefixlen": "",
            "vrf_name": "default",
            "subinterfaces": [],
            "link_local_enable": false,
            "dhcp_servers": [],
            "dhcpv6_servers": [],
            "ospf_area": null,
            "ospf_process_id": null,
            "ospf_hello_timer": null,
            "ospf_dead_timer": null,
            "ospf_bfd": null,
            "ospf_mtu_ignore": null,
            "ospf_md5_key_id": null,
            "ospf_md5_key": null,
            "ospf_network_type": null
        }
    },
    "portSetting": {},
    "bgpService": {
        "asn": "3",
        "router_id": "172.16.0.0",
        "overlay_protocol": null,
        "ipv6_support": false,
        "max_evpn_routes": 0,
        "max_mlag_routes": 0,
        "max_external_routes": 0,
        "max_fabric_routes": 0,
        "evpn_uses_mac_vrf": false,
        "evpn_reject_asymmetric_vni": false,
        "name": "bgp",
        "type": "Service",
        "default_fabric_evi_route_target": null,
        "evpn_generate_type5_host_routes": "disabled"
    },
    "ospf_services": {},
    "bgp_sessions": {
        "172.16.0.19_3->172.16.0.18_1_default": {
            "name": "172.16.0.19_3->172.16.0.18_1_default",
            "description": "facing_spine1",
            "role": "leaf_spine",
            "source_asn": "3",
            "source_ip": "172.16.0.19",
            "dest_asn": "1",
            "dest_ip": "172.16.0.18",
            "address_families": {
                "ipv4": true,
                "ipv6": false,
                "evpn": false
            },
            "vrf_name": "default",
            "source_interface": "",
            "route_map_out": "LEAF_TO_SPINE_FABRIC_OUT",
            "route_map_in": "",
            "route_map_v6_out": "",
            "route_map_v6_in": "",
            "route_map_evpn_out": "",
            "route_map_evpn_in": "",
            "password": "",
            "ttl": "",
            "keepalive_timer": "",
            "holdtime_timer": "",
            "bfd": false,
            "session_type": "addressed",
            "local_asn": null
        },
        "172.16.0.51_3->172.16.0.50_2_default": {
            "name": "172.16.0.51_3->172.16.0.50_2_default",
            "description": "facing_spine2",
            "role": "leaf_spine",
            "source_asn": "3",
            "source_ip": "172.16.0.51",
            "dest_asn": "2",
            "dest_ip": "172.16.0.50",
            "address_families": {
                "ipv4": true,
                "ipv6": false,
                "evpn": false
            },
            "vrf_name": "default",
            "source_interface": "",
            "route_map_out": "LEAF_TO_SPINE_FABRIC_OUT",
            "route_map_in": "",
            "route_map_v6_out": "",
            "route_map_v6_in": "",
            "route_map_evpn_out": "",
            "route_map_evpn_in": "",
            "password": "",
            "ttl": "",
            "keepalive_timer": "",
            "holdtime_timer": "",
            "bfd": false,
            "session_type": "addressed",
            "local_asn": null
        }
    },
    "routing": {
        "has_l3edge": false,
        "prefix_lists": {},
        "ipv6_prefix_lists": {},
        "aspath_lists": {},
        "route_maps": {
            "LEAF_TO_SPINE_FABRIC_OUT": [
                {
                    "name": "LEAF_TO_SPINE_FABRIC_OUT",
                    "policies": [
                        "community FROM_SPINE_FABRIC_TIER",
                        "protocol bgp"
                    ],
                    "sequence": 10,
                    "action": "deny",
                    "vrf_name": "default",
                    "custom_actions": []
                },
                {
                    "name": "LEAF_TO_SPINE_FABRIC_OUT",
                    "policies": [],
                    "sequence": 20,
                    "action": "permit",
                    "vrf_name": "default",
                    "custom_actions": []
                }
            ],
            "AllPodNetworks": [
                {
                    "name": "AllPodNetworks",
                    "policies": [
                        "family inet",
                        "protocol direct"
                    ],
                    "sequence": 10,
                    "action": "custom",
                    "vrf_name": "default",
                    "custom_actions": [
                        "community add DEFAULT_DIRECT_V4",
                        "accept"
                    ]
                },
                {
                    "name": "AllPodNetworks",
                    "policies": [],
                    "sequence": 100,
                    "action": "deny",
                    "vrf_name": "default",
                    "custom_actions": []
                }
            ],
            "BGP-AOS-Policy": [
                {
                    "name": "BGP-AOS-Policy",
                    "policies": [
                        "policy AllPodNetworks"
                    ],
                    "sequence": 10,
                    "action": "permit",
                    "vrf_name": "default",
                    "custom_actions": []
                },
                {
                    "name": "BGP-AOS-Policy",
                    "policies": [],
                    "sequence": 100,
                    "action": "deny",
                    "vrf_name": "default",
                    "custom_actions": []
                }
            ]
        },
        "community_lists": {
            "DEFAULT_DIRECT_V4": [
                {
                    "name": "DEFAULT_DIRECT_V4",
                    "sequence": 5,
                    "action": "permit",
                    "community": "3:20007 21001:26000"
                }
            ],
            "FROM_SPINE_FABRIC_TIER": [
                {
                    "name": "FROM_SPINE_FABRIC_TIER",
                    "sequence": 5,
                    "action": "permit",
                    "community": "0:15"
                }
            ]
        },
        "static_routes": {},
        "bgp_aggregates": {},
        "route_map_index": {
            "aspath_lists": {},
            "prefix_lists": {},
            "ipv6_prefix_lists": {}
        },
        "has_evpn_gw": false,
        "has_dynamic_bgp_neighbor": false,
        "has_any_link_local_interface": false
    },
    "vlan": {},
    "configlets": {},
    "vxlan": {},
    "security_zones": {
        "default": {
            "vrf_name": "default",
            "vlan_id": null,
            "vni_id": null,
            "sz_type": "l3_fabric",
            "import_targets": [],
            "export_targets": [],
            "rd": null,
            "loopback_intf": "lo0.0",
            "loopback_ip": "172.16.0.0",
            "loopback_ipv6": null,
            "ipv6_support": false,
            "has_static_routes": false,
            "has_link_local_interface": false,
            "junos_evpn_irb_mode": null,
            "tags": [],
            "vrf_description": null
        }
    },
    "loopbacks": {},
    "access_lists": {},
    "ipv6_support": false,
    "dot1x_config": {},
    "aaa_servers": {},
    "mac_msb": 2,
    "fabric_policy": {
        "id": "VIeWRiijBOBC2Er1Qw",
        "mode": "dlb",
        "label": "Default Policy",
        "dlb_options": {
            "dlb_mode": "flowlet",
            "egress_quantization": null,
            "flowlet_options": {
                "flowset_table_size": null,
                "inactivity_interval": 128,
                "reassignment": null
            },
            "glb_options": null,
            "sampling_rate": null
        },
        "policy_type": "default"
    },
    "evpn_interconnect": {},
    "use_granular_mtu_rendering": true,
    "load_balancing_policy": {
        "id": "VIeWRiijBOBC2Er1Qw",
        "mode": "dlb",
        "label": "Default Policy",
        "dlb_options": {
            "dlb_mode": "flowlet",
            "egress_quantization": null,
            "flowlet_options": {
                "flowset_table_size": null,
                "inactivity_interval": 128,
                "reassignment": null
            },
            "glb_options": null,
            "sampling_rate": null
        },
        "policy_type": "default"
    },
    "aos_version": "6.0.0"
}
'''

# Example property set JSON as a string
EXAMPLE_PROPERTY_SET = '''
{
  "gbp_info": [
    {
      "10": [
        {
          "10": "accept"
        },
        {
          "20": "accept"
        },
        {
          "30": "discard"
        }
      ]
    },
    {
      "20": [
        {
          "20": "accept"
        },
        {
          "10": "accept"
        },
        {
          "30": "discard"
        }
      ]
    },
    {
      "30": [
        {
          "10": "discard"
        },
        {
          "20": "discard"
        },
        {
          "30": "accept"
        }
      ]
    }
  ]
}
'''