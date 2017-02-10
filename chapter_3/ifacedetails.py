"""
This module uses the netifaces package.

To have a clearer understanding of the code,
read the documentaion at: https://pypi.python.org/pypi/netifaces
"""
import sys
try:
    import netifaces
except:
    sys.exit('[!] Install the netifaces library: pip install netifaces')

def get_interfaces():
    interfaces = netifaces.interfaces()
    return interfaces

def get_gateways():
    gateway_dict = {}
    gws = netifaces.gateways()
    for gw in gws:
        try:
            gateway_iface = gws[gw][netifaces.AF_INET]
            # first elem in the the tuple is the IP, second is the iface name
            gateway_ip, iface = gateway_iface[0], gateway_iface[1]
            gw_list = [gateway_ip, iface]
            gateway_dict[gw] = gw_list
        except:
            pass
    return gateway_dict


def get_addresses(interface):
    """
    Get addresses for an interfce. Includes: MAC addr, iface addr (typically
    IPv4), broadcast addr and network mask.
    """
    addrs = netifaces.ifaddresses(interface)
    link_addr = addrs[netifaces.AF_LINK]
    iface_addr = addrs[netifaces.AF_INET]
    # both of the subscriptions above return a list, because an interface
    # might have more than one address associated with it, so right below
    # we're just gonna grab the first of those addresses (usually there
    # will only be only one).
    iface_dict = iface_addr[0]
    link_dict = link_addr[0]

    hwaddr = link_dict.get('addr')  # MAC
    iface_addr = iface_dict.get('addr')  # iface addr
    iface_broadcast = iface_dict.get('broadcast')  # broadcast addr
    iface_netmask = iface_dict.get('netmask')  # network mask

    return hwaddr, iface_addr, iface_broadcast, iface_netmask


def get_networks(gateways):
    """
    Get full details about network interfaces.

    Args:
        gateways (dict): dictionary provided by get_gateways()
    """
    networks_dict = {}
    for key, value in gateways.items():
        gateway_ip, iface_name = value[0], value[1]  # value is "gw_list"
        hwaddr, addr, bcast, nmask = get_addresses(iface_name)
        network = {'gateway': gateway_ip, 'hwaddr': hwaddr, 'addr': addr,
                   'broadcast': bcast, 'netmask': nmask}
        networks_dict[iface_name] = network
    return networks_dict


if __name__ == '__main__':
    gateways = get_gateways()
    network_ifaces = get_networks(gateways)
    print(network_ifaces)
