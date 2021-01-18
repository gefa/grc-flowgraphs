#!/usr/bin/env python3
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
from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot

# from zig_sens import \
#     zig_sens as flowgraph
from gnuradio import gr

IP_TX_MACHINE = "127.0.0.1"
PORT_TX_MACHINE_VAR = 57000


@conf.commands.register
def gnuradio_set_vars(gr_host=IP_TX_MACHINE, gr_port=PORT_TX_MACHINE_VAR, **kwargs):
    try:
        from xmlrpc.client import Server
        from xmlrpc.client import Fault
    except ImportError:
        print("xmlrpc is needed to call 'gnuradio_set_vars'")
    else:
        s = Server("http://{}:{}".format(gr_host, gr_port))
        for k, v in kwargs.items():
            try:
                getattr(s, "set_{}".format(k))(v)
            except Fault:
                print("Unknown variable '{}'".format(k))
        s = None


@conf.commands.register
def gnuradio_get_vars(*args, **kwargs):
    if "gr_host" not in kwargs:
        kwargs["gr_host"] = IP_TX_MACHINE
    if "gr_port" not in kwargs:
        kwargs["gr_port"] = PORT_TX_MACHINE_VAR
    rv = {}
    try:
        from xmlrpc.client import Server
        from xmlrpc.client import Fault
    except ImportError:
        print("xmlrpc is needed to call 'gnuradio_get_vars'")
    else:
        s = Server(
            "http://{}:{}".format(kwargs["gr_host"], kwargs["gr_port"]))
        for v in args:
            try:
                res = getattr(s, "get_{}".format(v))()
                rv[v] = res
            except Fault:
                print("Unknown variable '{}'".format(v))
        s = None
    if len(args) == 1:
        return rv[args[0]]
    return rv

global name, exp

if __name__ == '__main__':

    channel = 11
    START=11
    STEP=1
    STOP=26
    STEPS = [x for x in range(START,STOP+STEP,STEP)]

    print(STEPS)
    print("channel "+str(channel))
    subp = Popen(['python3','uhd_msg_tune.py']) #, stdout=PIPE, stderr=PIPE)
    time.sleep(6)
    for vary in STEPS:
        print("CURRENT STEP "+str(vary))
        gnuradio_set_vars(channel=vary)
        print('Freq:', gnuradio_get_vars('channel'))
        time.sleep(5)
    
    #time.sleep(10)
    print("Killing "+str(subp.pid))
    ret = os.system("kill -9 {}".format(subp.pid))
    print(ret)
