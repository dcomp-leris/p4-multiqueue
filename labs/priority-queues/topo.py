#!/usr/bin/python2

#ajeitar todos os pritns e por aprenteses
#uma coisa: eu mudei ali em cima pra usr/bin/python2 (tava so python)
#talvez seja melhor manter o python2 pra rodar esse codigo
    #ta tendo problema nos xranges por n tarem definidos no python2
    #mas no pyhton3 se mudar pra range pode ter problema
    #pra seguran;a vou instalar o python2 nessa maquina e ver o q da
# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.link import TCIntf

#essas classes tao definidas dentro da pasta do bmv2
from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep
import os
import subprocess

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)

args = parser.parse_args()

class MyTopo(Topo):
    def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        for i in xrange(nb_switches):
            switch = self.addSwitch('s%d' % (i + 1),
                                    sw_path = sw_path,
                                    json_path = json_path,
                                    thrift_port = _THRIFT_BASE_PORT + i,
                                    pcap_dump = True,
                                    device_id = i,
                                    enable_debugger = True,
                                    log_console = True) 
            print(sw_path)       
        for h in xrange(nb_hosts):
            host = self.addHost('h%d' % (h + 1),
                                 ip = "10.0.%d.10/24" % h,
                                 mac = '00:04:00:00:00:%02x' % h)

        i = 0
        for a, b in links:
            self.addLink(a, b,
                         addr1 = '00:aa:bb:00:00:%02d' % i, 
                         addr2 = '00:aa:bb:00:00:%02d' % (i + 1))
            i += 2

def read_topo():
    nb_hosts = 0
    nb_switches = 0
    links = []
    with open("topo.txt", "r") as f:
        line = f.readline()[:-1]
        w, nb_switches = line.split()
        assert(w == "switches")
        line = f.readline()[:-1]
        w, nb_hosts = line.split()
        assert(w == "hosts")
        for line in f:
            if not f: break
            a, b = line.split()
            links.append( (a, b) )
    return int(nb_hosts), int(nb_switches), links
            

def main():
    print("topo.py file begin ---------")
    nb_hosts, nb_switches, links = read_topo()

    topo = MyTopo(args.behavioral_exe,
                  args.json,
                  nb_hosts, nb_switches, links ) #, args.priority_queues
    
    

    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  link = TCLink,
                  controller = None ) 
    net.start()
    

    sw_mac = ["00:aa:bb:00:00:%02x" % n for n in xrange(nb_hosts)]

    sw_addr = ["10.0.%d.1" % n for n in xrange(nb_hosts)]

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
        print("**********")
        print("Hostname: %s" %(h.name))
        for off in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload eth0 %s off" % off
            print(cmd)
            h.cmd(cmd)
        print("disable ipv6")
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
        h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
        h.describe()
        print("**********")


    sw_addr = ["10.0.%d.1" % n for n in xrange(nb_hosts)]

    s = net.get('s1')
    sw_mac_s1_eth1 = s.intf("s1-eth1").MAC()
    h = net.get('h1')
    h.setARP(sw_addr[0], sw_mac_s1_eth1)
    h.setDefaultRoute("dev eth0 via %s" % sw_addr[0])


    s = net.get('s1')
    sw_mac_s1_eth2 = s.intf("s1-eth2").MAC()
    h = net.get('h2')
    h.setARP(sw_addr[1], sw_mac_s1_eth2)
    h.setDefaultRoute("dev eth0 via %s" % sw_addr[1])

#    s = net.get('s3')
#    sw_mac_s3_eth1 = s.intf("s3-eth1").MAC()
#    h = net.get('h2')
#    h.setARP(sw_addr[1], sw_mac_s3_eth1)
#    h.setDefaultRoute("dev eth0 via %s" % sw_addr[1])
#
#    s = net.get('s4')
#    sw_mac_s4_eth1 = s.intf("s4-eth1").MAC()  
#    h = net.get('h3')
#    h.setARP(sw_addr[2], sw_mac_s4_eth1)
#    h.setDefaultRoute("dev eth0 via %s" % sw_addr[2])


    sleep(1)

    for i in xrange(nb_switches):
        s = net.get('s%d' % (i + 1))
        print("**********")
        print("Switch Name: %s" %(s.name))
        print("Switch DPID: %s" %(s.dpid))
        for j in s.ports:
            print("port: %s - intf: %s - mac: %s" % (
                s.ports[s.intf(j)],
                j,
                s.intf(str(j)).MAC()
                )
            )

        print("Running command_s%d.txt" % (i + 1))
        cmd = [args.cli, "--json", args.json,
               "--thrift-port", str(_THRIFT_BASE_PORT + i), ] 
        with open("command_s%d.txt" % (i + 1), "r") as f:
            print(" ".join(cmd))
            try:
                output = subprocess.check_output(cmd, stdin = f)
                #print output
            except subprocess.CalledProcessError as e:
                print(e)
                print(e.output)
        print("**********")

    sleep(1)

    print("Ready !")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
