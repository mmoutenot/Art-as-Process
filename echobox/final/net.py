#!/usr/bin/env python

# This is some example code for python-gstreamer.
# It's a gstreamer TCP/IP server that listens on
# the localhost for a client to send data to it.
# It shows how to use the tcpserversrc and tcpclientsink
# elements.

import gobject, pygst
pygst.require("0.10")
import gst
import sys

if len(sys.argv) != 2:
    print("Error - usage is " + sys.argv[0] + " host_ip_address")
    sys.exit(1)

# Callback for the decodebin source pad
def new_decode_pad(dbin, pad, islast):
        pad.link(convert.get_pad("sink"))

# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
pipeline = gst.Pipeline("server")

tcpsrc = gst.element_factory_make("tcpserversrc", "source")
pipeline.add(tcpsrc)
tcpsrc.set_property("host", sys.argv[1])
tcpsrc.set_property("port", 3201)

decode = gst.element_factory_make("decodebin", "decode")
decode.connect("new-decoded-pad", new_decode_pad)
pipeline.add(decode)
tcpsrc.link(decode)

convert = gst.element_factory_make("audioconvert", "convert")
pipeline.add(convert)

#Audio Output
sink = gst.element_factory_make("autoaudiosink", "sink")
pipeline.add(sink)
convert.link(sink)

pipeline.set_state(gst.STATE_PLAYING)

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

