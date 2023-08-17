#!/usr/bin/env python3
import argparse
import sys
import socket
import random
import struct

from time import sleep
from scapy.all import Packet, bind_layers, XByteField, FieldLenField, BitField, ShortField, IntField, PacketListField, Ether, IP, UDP, sendp, get_if_hwaddr, sniff


class priority_header(Packet):
    fields_desc = [ BitField("priority", 0, 3),
                    BitField("qid", 0, 5),
                    BitField("swid", 0, 8),
                  ]
    """any thing after this packet is extracted is padding"""
    def extract_padding(self, p):
                return "", p

class nodeCount(Packet):
  name = "nodeCount"
  fields_desc = [ ShortField("count", 0),
                  PacketListField("priority_header", [], priority_header, count_from=lambda pkt:(pkt.count*1))]
  
def handle_pkt(pkt):
  pkt.show2()
  
def main():

  iface = 'eth0'
  bind_layers(IP, nodeCount, proto = 253)
  sniff(filter = "ip proto 253", iface = iface, prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()