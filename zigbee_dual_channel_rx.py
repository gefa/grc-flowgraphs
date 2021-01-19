#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: zigbee_dual_channel_rx
# GNU Radio version: 3.8.1.0

from gnuradio import analog
import math
from gnuradio import blocks
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
import foo
import ieee802_15_4


class zigbee_dual_channel_rx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "zigbee_dual_channel_rx")

        ##################################################
        # Variables
        ##################################################
        self.transition_width = transition_width = 300e3
        self.sample_rate = sample_rate = 8e6
        self.cutoff_freq = cutoff_freq = 850e3
        self.channel_spacing = channel_spacing = 5e6
        self.channel = channel = 0
        self.base_freq = base_freq = int(2405e6)
        self.squelch_threshold = squelch_threshold = -75
        self.lowpass_filter = lowpass_filter = firdes.low_pass(1, sample_rate, cutoff_freq, transition_width, firdes.WIN_HAMMING, 6.76)
        self.gmsk_sps = gmsk_sps = 4
        self.gmsk_omega_limit = gmsk_omega_limit = 0.035
        self.gmsk_mu = gmsk_mu = 0.5
        self.gmsk_gain_mu = gmsk_gain_mu = 0.7
        self.freq_offset = freq_offset = 2.5e6
        self.freq = freq = (base_freq+(channel_spacing*channel))
        self.decim = decim = 4

        ##################################################
        # Blocks
        ##################################################
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
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_char*1, '/tmp/sensor11.pcap', False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/tmp/sensor12.pcap', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc(squelch_threshold, 0.1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_15_4_packet_sink_0, 'out'), (self.foo_wireshark_connector_0, 'in'))
        self.msg_connect((self.ieee802_15_4_packet_sink_0_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
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


    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_rate/2e6/self.decim)
        self.digital_clock_recovery_mm_xx_0_0.set_omega(self.sample_rate/2e6/self.decim)
        self.uhd_usrp_source_0.set_samp_rate(self.sample_rate)

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.set_lowpass_filter(firdes.low_pass(1, self.sample_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_channel_spacing(self):
        return self.channel_spacing

    def set_channel_spacing(self, channel_spacing):
        self.channel_spacing = channel_spacing
        self.set_freq((self.base_freq+(self.channel_spacing*self.channel)))

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq((self.base_freq+(self.channel_spacing*self.channel)))

    def get_base_freq(self):
        return self.base_freq

    def set_base_freq(self, base_freq):
        self.base_freq = base_freq
        self.set_freq((self.base_freq+(self.channel_spacing*self.channel)))

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





def main(top_block_cls=zigbee_dual_channel_rx, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

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
