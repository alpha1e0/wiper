

from plugin.lib.dnsresolve import DnsResolver

dns = DnsResolver()

#response = dns.getRecords("ns","www.baidu.com")
#response = dns.getRecords("ns","baidu.com")
response = dns.resolveAll("baidu.com")
#response = dns.getZoneRecords("thinksns.com")
print response