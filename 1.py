
from plugin.lib.dnsresolve import DnsResolver

dns = DnsResolver()

ip = dns.domain2IP("xiuren.aero")
print ip