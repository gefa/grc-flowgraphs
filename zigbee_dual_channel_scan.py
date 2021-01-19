#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: zigbee_dual_channel_scan
# GNU Radio version: 3.8.1.0

from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
try:
   import SimpleXMLRPCServer
except ModuleNotFoundError:
   import xmlrpc.server as SimpleXMLRPCServer
import threading
import foo
import ieee802_15_4


class zigbee_dual_channel_scan(gr.top_block):

    def __init__(self, ant_msg='RX2', gain_msg=0.8, lo_msg=0):
        gr.top_block.__init__(self, "zigbee_dual_channel_scan")

        ##################################################
        # Parameters
        ##################################################
        self.ant_msg = ant_msg
        self.gain_msg = gain_msg
        self.lo_msg = lo_msg

        ##################################################
        # Variables
        ##################################################
        self.channel_spacing = channel_spacing = 5e6
        self.channel = channel = 11
        self.transition_width = transition_width = 300e3
        self.sample_rate = sample_rate = 8e6
        self.freq_msg = freq_msg = 1000000 * (2400 + channel_spacing * (channel - 10))
        self.cutoff_freq = cutoff_freq = 850e3
        self.base_freq = base_freq = int(2405e6)
        self.squelch_threshold = squelch_threshold = -75
        self.lowpass_filter = lowpass_filter = firdes.low_pass(1, sample_rate, cutoff_freq, transition_width, firdes.WIN_HAMMING, 6.76)
        self.gmsk_sps = gmsk_sps = 4
        self.gmsk_omega_limit = gmsk_omega_limit = 0.035
        self.gmsk_mu = gmsk_mu = 0.5
        self.gmsk_gain_mu = gmsk_gain_mu = 0.7
        self.freq_offset = freq_offset = 2.5e6
        self.freq = freq = (base_freq+(channel_spacing*(channel-11)))
        self.decim = decim = int(sample_rate/2000000)
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
        self.uhd_usrp_source_0.set_center_freq(freq+freq_offset, 0)
        self.uhd_usrp_source_0.set_rx_agc(True, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(sample_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_ff(0.00016, 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.00016, 1)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decim,
                taps=None,
                fractional_bw=None)
        self.ieee802_15_4_packet_sink_0_0 = ieee802_15_4.packet_sink(10)
        self.ieee802_15_4_packet_sink_0 = ieee802_15_4.packet_sink(10)
        self.freq_xlating_fir_filter_xxx_0_0_0 = filter.freq_xlating_fir_filter_ccc(1, lowpass_filter, freq_offset, sample_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, lowpass_filter, -freq_offset, sample_rate)
        self.foo_wireshark_connector_0_0 = foo.wireshark_connector(195, False)
        self.foo_wireshark_connector_0 = foo.wireshark_connector(195, False)
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(sample_rate/2e6/decim, 0.000225, 0.5, 0.03, 0.0002)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sample_rate/2e6/decim, 0.000225, 0.5, 0.03, 0.0002)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_message_strobe_0 = blocks.message_strobe(cmd_msg, 1000000)
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_char*1, '/tmp/sensor12.pcap', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/tmp/sensor11.pcap', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc(squelch_threshold, 0.1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.ieee802_15_4_packet_sink_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.ieee802_15_4_packet_sink_0, 'out'), (self.foo_wireshark_connector_0, 'in'))
        self.msg_connect((self.ieee802_15_4_packet_sink_0_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.ieee802_15_4_packet_sink_0_0, 'out'), (self.foo_wireshark_connector_0_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.single_pole_iir_filter_xx_0_0, 0))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.freq_xlating_fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.ieee802_15_4_packet_sink_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.ieee802_15_4_packet_sink_0_0, 0))
        self.connect((self.foo_wireshark_connector_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.foo_wireshark_connector_0_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_simple_squelch_cc_1, 0))


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

    def get_channel_spacing(self):
        return self.channel_spacing

    def set_channel_spacing(self, channel_spacing):
        self.channel_spacing = channel_spacing
        self.set_freq((self.base_freq+(self.channel_spacing*(self.channel-11))))
        self.set_freq_msg(1000000 * (2400 + self.channel_spacing * (self.channel - 10)))

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq((self.base_freq+(self.channel_spacing*(self.channel-11))))
        self.set_freq_msg(1000000 * (2400 + self.channel_spacing * (self.channel - 10)))

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.set_decim(int(self.sample_rate/2000000))
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/2e6/self.decim)
        self.digital_clock_recovery_mm_xx_0_0.set_omega(self.sample_rate/2e6/self.decim)
        self.uhd_usrp_source_0.set_samp_rate(self.sample_rate)

    def get_freq_msg(self):
        return self.freq_msg

    def set_freq_msg(self, freq_msg):
        self.freq_msg = freq_msg
        self.set_cmd_msg(pmt.to_pmt({'antenna': self.ant_msg, 'gain': self.gain_msg, 'chan': 0, 'freq': self.freq_msg, 'lo_offset': self.lo_msg}))

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.set_freq((self.base_freq+(self.channel_spacing*(self.channel-11))))

    def get_squelch_threshold(self):
        return self.squelch_threshold

    def set_squelch_threshold(self, squelch_threshold):
        self.squelch_threshold = squelch_threshold
        self.analog_simple_squelch_cc_1.set_threshold(self.squelch_threshold)

    def get_lowpass_filter(self):
        return self.lowpass_filter

    def set_lowpass_filter(self, lowpass_filter):
        self.lowpass_filter = lowpass_filter
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(self.lowpass_filter)
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(self.lowpass_filter)

    def get_gmsk_sps(self):
        return self.gmsk_sps

    def set_gmsk_sps(self, gmsk_sps):
        self.gmsk_sps = gmsk_sps

    def get_gmsk_omega_limit(self):
        return self.gmsk_omega_limit

    def set_gmsk_omega_limit(self, gmsk_omega_limit):
        self.gmsk_omega_limit = gmsk_omega_limit

    def get_gmsk_mu(self):
        return self.gmsk_mu

    def set_gmsk_mu(self, gmsk_mu):
        self.gmsk_mu = gmsk_mu

    def get_gmsk_gain_mu(self):
        return self.gmsk_gain_mu

    def set_gmsk_gain_mu(self, gmsk_gain_mu):
        self.gmsk_gain_mu = gmsk_gain_mu

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(-self.freq_offset)
        self.freq_xlating_fir_filter_xxx_0_0_0.set_center_freq(self.freq_offset)
        self.uhd_usrp_source_0.set_center_freq(self.freq+self.freq_offset, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq+self.freq_offset, 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/2e6/self.decim)
        self.digital_clock_recovery_mm_xx_0_0.set_omega(self.sample_rate/2e6/self.decim)

    def get_cmd_msg(self):
        return self.cmd_msg

    def set_cmd_msg(self, cmd_msg):
        self.cmd_msg = cmd_msg
        self.blocks_message_strobe_0.set_msg(self.cmd_msg)




def argument_parser():
    parser = ArgumentParser()
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


def main(top_block_cls=zigbee_dual_channel_scan, options=None):
    if options is None:
        options = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
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
