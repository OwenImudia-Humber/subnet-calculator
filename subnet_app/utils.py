import ipaddress

def calculate_subnet(ip, subnet):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)

        hosts = list(network.hosts())

        return {
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "first_host": str(hosts[0]) if hosts else "N/A",
            "last_host": str(hosts[-1]) if hosts else "N/A",
            "total_hosts": len(hosts),
            "subnet_mask": str(network.netmask),
            "cidr": network.prefixlen
        }

    except:
        return {"error": "Invalid input"}