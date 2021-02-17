### !/usr/bin/env python2
import os,sys
from subprocess import Popen, PIPE
import signal,time


import socket

from scapy.data import MTU
from scapy.packet import *
from scapy.fields import *
from scapy.supersocket import SuperSocket
from scapy import sendrecv
from scapy import main
from scapy.layers.dot15d4 import * #Dot15d4FCS, Dot15d4Cmd
from scapy.modules.gnuradio import *

#from appdirs import user_data_dir
import socket
import struct
import atexit
import os
import sys
import time
from datetime import datetime
import errno

import random


import atexit
import errno
import os
import random
import signal
#from appdirs import user_data_dir
import socket
import struct
import sys
import time
from distutils.version import StrictVersion
from threading import Timer

#from PyQt4 import Qt
# from PyQt5 import Qt
# from PyQt5.QtCore import QObject, pyqtSlot

# from zig_sens import \
#     zig_sens as flowgraph
#from gnuradio import gr

IP_TX_MACHINE = "127.0.0.1"
IP_RX_MACHINE = "127.0.0.1"
PORT_TX_MACHINE_VAR = 57004
#PORT_RX_MACHINE_VAR = 57002


@conf.commands.register
def gnuradio_set_vars(host="localhost", port=8080, **kargs):
    try:
        import xmlrpclib
    except ImportError:
        print "xmlrpclib is missing to use this function."
    else:
        s = xmlrpclib.Server("http://%s:%d" % (host, port))
        for k, v in kargs.iteritems():
            try:
                getattr(s, "set_%s" % k)(v)
            except xmlrpclib.Fault:
                print "Unknown variable '%s'" % k
        s = None

# #@conf.commands.register
# def gnuradio_get_vars(*args, **kwargs):
#     if "gr_host" not in kwargs:
#         kwargs["gr_host"] = IP_TX_MACHINE
#     if "gr_port" not in kwargs:
#         kwargs["gr_port"] = PORT_TX_MACHINE_VAR
#     rv = {}
#     try:
#         # from xmlrpc.client import Server
#         # from xmlrpc.client import Fault
#         #from SimpleXMLRPCServer import Server, Fault
#         from xmlrpclib import Server, Fault
#     except ImportError:
#         print("xmlrpc is needed to call 'gnuradio_get_vars'")
#     else:
#         s = Server(
#             "http://{}:{}".format(kwargs["gr_host"], kwargs["gr_port"]))
#         print(dir(Server))
#         for v in args:
#             try:
#                 res = getattr(s, "get_{}".format(v))()
#                 rv[v] = res
#             except Fault:
#                 print("Unknown variable '{}'".format(v))
#         s = None
#     if len(args) == 1:
#         return rv[args[0]]
#     return rv

global name, exp

from collections import defaultdict
import time
if __name__ == '__main__':

    channel = 11
    START=11
    STEP=1
    STOP=26
    STEPS = [x for x in range(START,STOP+STEP,STEP)]
    REFERENCE_CNT = 100
    BEACON = Dot15d4FCS()/Dot15d4Cmd()/Dot15d4CmdAssocReq() # b'\x03\x08\xf2\xff\xff\xff\xff\x07\xcd\xe1' 
    # print(type(BEACON))
    # print(dir(BEACON))
    # print(bytes(BEACON.payload))
    #pkts = defaultdict()
    pkts = [dict() for x in range(START,STOP+STEP,STEP)]

    print(STEPS)
    #print("channel "+str(channel))
    #subp = Popen(['python3.8','uhd_msg_tune.py']) #, stdout=PIPE, stderr=PIPE)
    #pkts = sniffradio(radio="BT4LE",store=1)
    #time.sleep(6)

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock_address_first = (IP_RX_MACHINE, PORT_RX_MACHINE_VAR)
    # sock.settimeout(60)
    # sock.bind(sock_address_first)
    soctx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soctx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socrx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socrx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socrx.settimeout(1)
    wireshark = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wireshark.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    txmt_address = ('127.0.0.1', 52001)
    recv_address = ('127.0.0.1', 52002)
    wireshark_addr = ('127.0.0.1', 52003)
    socrx.bind(recv_address)
    #wireshark.bind(wireshark_addr)

    import xmlrpclib
    s = xmlrpclib.Server('http://0.0.0.0:8000')
    #s.set_freq(5000)


    for idx,vary in enumerate(STEPS):
        print("CURRENT STEP "+str(vary))

        gnuradio_stop_graph(host="localhost", port=8000)
        s.set_channel(vary)
        print('Freq:',s.get_channel())
        gnuradio_start_graph(host="localhost", port=8000)
        #s.close()

        #gnuradio_set_vars(channel=vary)
        #print('Freq:', gnuradio_get_vars('Channel'))
        #time.sleep(5)
        t_start = time.time()
        t_end = t_start + 3 * 1 # 15 min timout
        packets = 0

        while packets < REFERENCE_CNT and time.time() < t_end:
            print('\nwaiting to receive message')
            #soctx.sendto(bytes(BEACON.payload), txmt_address)
            try:
                data = socrx.recv(1000) # try to receive 100 bytes
                print(list(data))
                rx_msg = []
                for i in list(data):
                    rx_msg.append(i)
                    sys.stdout.write("\\x{:02x}".format(ord(i)))

                try:
                    #print(data[8:])
                    wireshark.sendto(data[8:], wireshark_addr)
                    print('Source address:')
                    addr = "0x{:02x}{:02x}".format(ord(rx_msg[8+14]),ord(rx_msg[8+13]))
                    # account only for packets with src.addr
                    # later we should count dest.addr too
                    print(addr)
                    try:
                        if pkts[idx][addr] >= 1:
                            pass
                    except:
                        packets += 1 # counts distinct addresses
                        pkts[idx][addr] = 1
                    finally:
                        pkts[idx][addr] += 1
                    print("packets:"+str(packets))
                    # if rx_msg[0] == 0x00 and rx_msg[1] == 0x80:
                    #     print('think i found beacon')
                    #     msg_num = msg_num + 1
                    # else:
                    #     pass
                except IndexError as e:
                    pass
            except socket.timeout: # fail after 1 second of no activity
                print("Didn't receive data! [Timeout]")
            finally:
                pass

            # add packet's address to set
            # if already discovered pass, else packets ++
    print("Found addresses: ")
    for idx,vary in enumerate(STEPS):
        print("Channel: "+str(vary))
        try:
            print(pkts[idx])
        except:
            print("No packets")
    # scan_time = time.time() - t_start
    # print("Scan time: "+str(scan_time)+" seconds")

    soctx.close()
    socrx.close()
    wireshark.close()
    #time.sleep(10)
    #print("Killing "+str(subp.pid))
    #ret = os.system("kill -9 {}".format(subp.pid))
    #print(ret)
