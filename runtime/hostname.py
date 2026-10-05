"""Optional endpoint-specific DNS mapping; URL hostnames still drive TLS checks."""
import ipaddress
import re
from pathlib import Path
from urllib.parse import urlsplit

MARKER = '# paperclip-cln-endpoint'

def apply_mapping(config, path=Path('/etc/hosts')):
    address = config.get('cln_connect_ip')
    hosts = []
    if address:
        address = str(ipaddress.ip_address(address))
    if address and config.get('cln'):
        for key in ('uri', 'hold_uri'):
            host = urlsplit(config['cln'][key]).hostname
            if not host or not re.fullmatch(r'[A-Za-z0-9.-]+', host):
                raise ValueError('CLN mapping requires a DNS hostname in both URLs')
            if host not in hosts:
                hosts.append(host)
    original = path.read_text()
    lines = [line for line in original.splitlines() if not line.endswith(MARKER)]
    if hosts:
        lines.append(address + ' ' + ' '.join(hosts) + ' ' + MARKER)
    updated = '\n'.join(lines) + '\n'
    if updated != original:
        path.write_text(updated)
