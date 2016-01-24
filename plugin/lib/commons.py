#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Wiper, an assistant tool for web penetration test.
Copyright (c) 2014-2015 alpha1e0
See the file COPYING for copying detail
'''

import os
import time
from subprocess import Popen, PIPE, STDOUT

from thirdparty import requests
from thirdparty.dns import resolver, reversename, query
from thirdparty.dns.exception import DNSException
from thirdparty.BeautifulSoup import BeautifulStoneSoup, NavigableString

from config import CONF, Dict



def DictFileEnum(fileName):
    if os.path.exists(fileName):
        with open(fileName, "r") as fd:
            for line in fd:
                if line and not line.startswith("#"):
                    yield line.strip()


class Nmap(object):
    '''
    Nmap scan.
    '''
    @classmethod
    def scan(cls, cmd):
        '''
        Nmap scan.
        output:
            a list of Host
        '''
        result = list()

        if "-oX" not in cmd:
            cmd = cmd + " -oX -"
        if CONF.nmap:
            cmd.replace("namp", CONF.nmap)

        popen = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        scanResult = popen.stdout.read()

        #parse the nmap scan result     
        xmlDoc = BeautifulStoneSoup(scanResult)
        hosts = xmlDoc.findAll("host")
        for host in hosts:
            if isinstance(host, NavigableString) or host.name!="host" or host.status['state']!="up":
                continue
            ip = host.address['addr']
            #url = host.hostnames.hostname['name']
            try:
                ports = host.ports.contents
            except AttributeError:
                result.append(Dict(**{'ip':ip}))
                continue
            else:
                for port in ports:
                    if isinstance(port, NavigableString) or port.name != "port" or port.state['state']!="open": 
                        continue
                    result.append(Dict(ip=ip,port=port['portid'],protocol=port.service['name']))

        return result



class DnsResolver(object):
    '''
    Dns operation.
    The records format is [domain, value, type]
    '''
    def __init__(self, domain=None, timeout=None):
        self.domain = domain

        self.resolver = resolver.Resolver()
        self.resolver.nameservers = CONF.dns.servers
        self.resolver.timeout = timeout if timeout else CONF.dns.timeout

        self.axfr = query.xfr


    def domain2IP(self, domain=None):
        '''
        Parse domain to IP.
        '''
        domainToResolve = domain if domain else self.domain
        try:
            response = self.resolver.query(domainToResolve, "A")
        except DNSException:
            return None
        else:
            return response[0].to_text()
            #return [x.to_text for x in response]


    def IP2domain(self, ip):
        '''
        Parse IP to domain. The most dns server dose not support this operation.
        '''
        return reversename.from_address(ip)


    def getRecords(self, rtype, domain=None):
        '''
        Get dns records, records type supports "A", "CNAME", "NS", "MX", "SOA", "TXT"
        Example:
            dns.getRecords("A")
        '''
        if not rtype in ["A", "CNAME", "NS", "MX", "SOA", "TXT", "a", "cname", "ns", "mx", "soa", "txt"]:
            return []

        domainToResolve = domain if domain else self.domain
        try:
            response = self.resolver.query(domainToResolve, rtype)
        except DNSException:
            return []

        if not response:
            return []

        if rtype in ["MX","mx"]:
            return [[domainToResolve, line.to_text().rstrip(".").split()[-1], rtype] for line in response]
        return [[domainToResolve, line.to_text().rstrip("."), rtype] for line in response]


    def getZoneRecords(self, domain=None):
        '''
        Check and use dns zone transfer vulnerability. This function will traverse all the 'ns' server
        Usage:
            dnsresolver = DnsResolver('aaa.com')
            records = dnsresolver.getZoneRecords()
        '''
        domainToResolve = domain if domain else self.domain

        records = list()
        nsRecords = self.getRecords("NS", domainToResolve)
        for serverRecord in nsRecords:
            xfrHandler = self.axfr(serverRecord[1], domainToResolve)
            try:
                for response in xfrHandler:
                    topDomain = response.origin.to_text().rstrip(".")
                    for line in response.answer:
                        # A records
                        if line.rdtype == 1:
                            lineSplited = line.to_text().split()
                            if lineSplited[0] != "@":
                                subDomain = lineSplited[0] + "." + topDomain
                                ip = lineSplited[-1]
                                records.append([subDomain, ip, "A"])
                        # CNAME records
                        elif line.rdtype == 5:
                            lineSplited = line.to_text().split()
                            if lineSplited[0] != "@":
                                subDomain = lineSplited[0] + "." + topDomain
                                aliasName = lineSplited[-1]
                                records.append([subDomain, aliasName, "CNAME"])
            except:
                pass

        return records


    def getZoneRecords2(self, server, domain=None):
        '''
        Use the specified ns server, check and use dns zone transfer vulnerability.
        Usage:
            dnsresolver = DnsResolver('aaa.com')
            records = dnsresolver.getZoneRecords2()
        '''
        domainToResolve = domain if domain else self.domain

        records = list()

        xfrHandler = self.axfr(server, domainToResolve)

        try:
            for response in xfrHandler:
                topDomain = response.origin.to_text().rstrip(".")
                for line in response.answer:
                    # A records
                    if line.rdtype == 1:
                        lineSplited = line.to_text().split()
                        if lineSplited[0] != "@":
                            subDomain = lineSplited[0] + "." + topDomain
                            ip = lineSplited[-1]
                            records.append([subDomain, ip, "A"])
                    # CNAME records
                    elif line.rdtype == 5:
                        lineSplited = line.to_text().split()
                        subDomain = lineSplited[0] + "." + topDomain
                        if lineSplited[0] != "@":
                            aliasName = lineSplited[-1]
                            records.append([subDomain, aliasName, "CNAME"])
        except:
            pass

        return records


    def resolveAll(self, domain=None):
        domainToResolve = domain if domain else self.domain
        types = ["A", "CNAME", "NS", "MX", "SOA", "TXT"]
        records = list()

        for t in types:
            records += self.getRecords(t, domainToResolve)

        records += self.getZoneRecords(domainToResolve)

        return records



class DnsBrute(object):
    '''
    Use wordlist to bruteforce subdomain.
    input:
        domain: the domain to bruteforce
        dictfiles: the dict files
        bruteTopDomain: wither to check top domain
    '''
    def __init__(self, domain, dictfiles, bruteTopDomain=False):
        self.domain = domain
        self.dictfiles = dictfiles
        self.bruteTopDomain = bruteTopDomain


    def checkDomain(self, domain, dnsresolver):
        ip = dnsresolver.domain2IP(domain)
        if ip:
            return ip


    def __iter__(self):
        return self.brute()


    def brute(self):
        #partDoman示例：aaa.com partDomain为aaa，aaa.com.cn partDomain为aaa
        pos = self.domain.rfind(".com.cn")
        if pos==-1: pos = self.domain.rfind(".")
        partDomain = self.domain if pos==-1 else self.domain[0:pos]

        if self.bruteTopDomain:
            dlist = os.path.join("data","wordlist","toplevel.txt")
            for line in DictFileEnum(dlist):
                domain = partDomain + "." + line
                ip = self.checkDomain(domain, dns)
                if ip:
                    yield Dict(url=domain, ip=ip, description="Generated by dnsbrute plugin.")

        for dlist in self.dictfiles:
            for line in DictFileEnum(dlist):
                domain = line + "." + self.domain
                ip = self.checkDomain(domain, dns)
                if ip:
                    yield Dict(url=domain, ip=ip, description="Generated by dnsbrute plugin.")



class ServiceIdentify(object):
    pass




