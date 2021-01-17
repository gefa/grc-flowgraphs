#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: UHD Message Tuner
# Description: Tune a UHD source from a QT sink via messages (double-click a frequency to tune)
# GNU Radio version: 3.8.1.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from ieee802_15_4_oqpsk_phy import ieee802_15_4_oqpsk_phy  # grc-generated hier_block
try:
   import SimpleXMLRPCServer
except ModuleNotFoundError:
   import xmlrpc.server as SimpleXMLRPCServer
import threading
import foo
import ieee802_15_4


class uhd_msg_tune(gr.top_block):

    def __init__(self, ant_msg='RX2', gain_msg=0.8, lo_msg=0):
        gr.top_block.__init__(self, "UHD Message Tuner")

        ##################################################
        # Parameters
        ##################################################
        self.ant_msg = ant_msg
        self.gain_msg = gain_msg
        self.lo_msg = lo_msg

        ##################################################
        # Variables
        ##################################################
        self.channel = channel = 11
        self.freq_msg = freq_msg = 1000000 * (2400 + 5 * (channel - 10))
        self.samp_rate = samp_rate = 4e6
        self.initial_fc = initial_fc = 1000000 * (2400 + 5 * (11 - 10))
        self.gain = gain = 0.8
        self.cmd_msg = cmd_msg = pmt.to_pmt({'antenna': ant_msg, 'gain': gain_msg, 'chan': 0, 'freq': freq_msg, 'lo_offset': lo_msg})

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer.SimpleXMLRPCServer(('127.0.0.1', 57000), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(initial_fc, 0)
        self.uhd_usrp_source_0.set_rx_agc(True, 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True,0x8841,0,0x1aaa,0xffff,0x3344)
        self.foo_wireshark_connector_0 = foo.wireshark_connector(195, False)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(cmd_msg, 500)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/tmp/sensor.pcap', False)
        self.blocks_file_sink_0.set_unbuffered(True)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.foo_wireshark_connector_0, 'in'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.foo_wireshark_connector_0, 'in'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))
        self.connect((self.foo_wireshark_connector_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))


    def get_ant_msg(self):
        return self.ant_msg

    def set_ant_msg(self, ant_msg):
        self.ant_msg = ant_msg
        self.set_cmd_msg(pmt.to_pmt({'antenna': self.ant_msg, 'gain': self.gain_msg, 'chan': 0, 'freq': self.freq_msg, 'lo_offset': self.lo_msg}))

    def get_gain_msg(self):
        return self.gain_msg

    def set_gain_msg(self, gain_msg):
        self.gain_msg = gain_msg
        self.set_cmd_msg(pmt.to_pmt({'antenna': self.ant_msg, 'gain': self.gain_msg, 'chan': 0, 'freq': self.freq_msg, 'lo_offset': self.lo_msg}))

    def get_lo_msg(self):
        return self.lo_msg

    def set_lo_msg(self, lo_msg):
        self.lo_msg = lo_msg
        self.set_cmd_msg(pmt.to_pmt({'antenna': self.ant_msg, 'gain': self.gain_msg, 'chan': 0, 'freq': self.freq_msg, 'lo_offset': self.lo_msg}))

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq_msg(1000000 * (2400 + 5 * (self.channel - 10)))

    def get_freq_msg(self):
        return self.freq_msg

    def set_freq_msg(self, freq_msg):
        self.freq_msg = freq_msg
        self.set_cmd_msg(pmt.to_pmt({'antenna': self.ant_msg, 'gain': self.gain_msg, 'chan': 0, 'freq': self.freq_msg, 'lo_offset': self.lo_msg}))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_initial_fc(self):
        return self.initial_fc

    def set_initial_fc(self, initial_fc):
        self.initial_fc = initial_fc
        self.uhd_usrp_source_0.set_center_freq(self.initial_fc, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_cmd_msg(self):
        return self.cmd_msg

    def set_cmd_msg(self, cmd_msg):
        self.cmd_msg = cmd_msg
        self.blocks_message_strobe_0.set_msg(self.cmd_msg)




def argument_parser():
    description = 'Tune a UHD source from a QT sink via messages (double-click a frequency to tune)'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-a", "--ant-msg", dest="ant_msg", type=str, default='RX2',
        help="Set Antena [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain-msg", dest="gain_msg", type=eng_float, default="800.0m",
        help="Set gain_msg [default=%(default)r]")
    parser.add_argument(
        "--lo-msg", dest="lo_msg", type=eng_float, default="0.0",
        help="Set LO Offset [default=%(default)r]")
    return parser


def main(top_block_cls=uhd_msg_tune, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(ant_msg=options.ant_msg, gain_msg=options.gain_msg, lo_msg=options.lo_msg)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
