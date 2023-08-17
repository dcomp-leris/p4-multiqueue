#!/usr/bin/env python3

import argparse
import sys
import socket
import random
import struct

from time import sleep
from scapy.all import Packet, bind_layers, BitField, ShortField, IntField, XByteField, PacketListField, FieldLenField, Raw, Ether, IP, UDP, sendp, get_if_hwaddr, sniff


class priority_header(Packet):
    fields_desc = [ BitField("priority", 0, 3),
                    BitField("qid", 0, 5),
                    BitField("swid", 0, 8),
                  ]
    def extract_padding(self, p):
                return "", p

class nodeCount(Packet):
  name = "nodeCount"
  fields_desc = [ ShortField("count", 0),
                  PacketListField("priority_header", [], priority_header, count_from=lambda pkt:(pkt.count*1))]

def main():

    addr = socket.gethostbyname(sys.argv[1])
    iface = 'eth0'

    bind_layers(IP, nodeCount, proto = 253)
    pkt = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff") / IP(
        dst=addr, proto=253) / nodeCount(count = 0, priority_header=[])

    #sendp(pkt, iface=iface)
    #pkt.show2()

    while True:
        sendp(pkt, iface=iface)
        pkt.show2()
        sleep(0.2)

if __name__ == '__main__':
    main()