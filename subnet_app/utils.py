import ipaddress


def _netmask_to_prefix(mask: ipaddress.IPv4Address) -> int:
    m = int(mask)
    if m == 0xFFFFFFFF:
        return 32
    host_bits = (~m) & 0xFFFFFFFF
    if host_bits == 0:
        return 32
    if (host_bits & (host_bits + 1)) != 0:
        raise ValueError(
            "Netmask must be a contiguous standard IPv4 subnet mask (e.g. 255.255.255.0)."
        )
    return 32 - host_bits.bit_length()


def parse_subnet_to_prefix(subnet_raw: str | None) -> int:
    if subnet_raw is None:
        raise ValueError("Subnet is required.")
    s = subnet_raw.strip()
    if not s:
        raise ValueError("Subnet is required.")
    if "." in s:
        try:
            mask = ipaddress.IPv4Address(s)
        except ValueError as e:
            raise ValueError(f"Invalid netmask: {s}.") from e
        return _netmask_to_prefix(mask)
    if s.startswith("/"):
        s = s[1:].strip()
    try:
        prefix = int(s, 10)
    except ValueError as e:
        raise ValueError(
            "Subnet must be a CIDR length (0–32), optionally with a leading slash, "
            "or a dotted-decimal netmask."
        ) from e
    if prefix < 0 or prefix > 32:
        raise ValueError("CIDR prefix must be between 0 and 32.")
    return prefix


def _usable_hosts(network: ipaddress.IPv4Network) -> tuple[str, str, int]:
    pl = network.prefixlen
    n = network.num_addresses
    net = network.network_address
    bcast = network.broadcast_address

    if pl == 32:
        s = str(net)
        return s, s, 1
    if pl == 31:
        return str(net), str(bcast), 2

    usable = n - 2
    if usable <= 0:
        return "N/A", "N/A", 0
    return str(net + 1), str(bcast - 1), usable


def calculate_subnet(ip_raw: str | None, subnet_raw: str | None) -> dict:
    if ip_raw is None or (isinstance(ip_raw, str) and not ip_raw.strip()):
        return {"error": "IP address is required."}
    if subnet_raw is None or (isinstance(subnet_raw, str) and not subnet_raw.strip()):
        return {"error": "Subnet is required."}

    ip = ip_raw.strip()
    try:
        prefix = parse_subnet_to_prefix(subnet_raw)
    except ValueError as e:
        return {"error": str(e)}

    try:
        network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
    except ValueError as e:
        return {"error": f"Invalid IPv4 network: {e}."}

    first_host, last_host, total_usable = _usable_hosts(network)

    return {
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "first_host": first_host,
        "last_host": last_host,
        "total_hosts": total_usable,
        "num_addresses": network.num_addresses,
        "subnet_mask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "cidr": network.prefixlen,
    }
