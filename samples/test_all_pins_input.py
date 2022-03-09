#!/usr/bin/env python

# Copyright (c) 2019-2020, NVIDIA CORPORATION. All rights reserved.
# Copyright (c) 2021, Texas Instruments Incorporated. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys

import RPi.GPIO as GPIO

pin_defs = [
#    BOARD BCM SOC
    ( 7,   4, 'GPIO0_7'),
    ( 8,  14, 'GPIO0_70'),
    (10,  15, 'GPIO0_81'),
    (11,  17, 'GPIO0_71'),
    (12,  18, 'GPIO0_1'),
    (13,  27, 'GPIO0_82'),
    (15,  22, 'GPIO0_11'),
    (16,  23, 'GPIO0_5'),
    (18,  24, 'GPIO0_12'),
    (19,  10, 'GPIO0_101'),
    (21,   9, 'GPIO0_107'),
    (22,  25, 'GPIO0_8'),
    (23,  11, 'GPIO0_103'),
    (24,   8, 'GPIO0_102'),
    (26,   7, 'GPIO0_108'),
    #(29,   5, 'GPIO0_93'),
    #(31,   6, 'GPIO0_94'),
    #(32,  12, 'GPIO0_98'),
    #(33,  13, 'GPIO0_99'),
    (35,  19, 'GPIO0_2'),
    (36,  16, 'GPIO0_97'),
    (37,  26, 'GPIO0_115'),
    (38,  20, 'GPIO0_3'),
    (40,  21, 'GPIO0_4')
]

def pin_data(offset, table):
    return [t[offset] for t in table]

channel_data = {
    GPIO.BOARD: {'name': "GPIO.BOARD", "pins": pin_data(0, pin_defs)},
    GPIO.BCM:   {'name': "GPIO.BCM",   "pins": pin_data(1, pin_defs)},
    GPIO.SOC:   {'name': "GPIO.SOC",   "pins": pin_data(2, pin_defs)},
}

pin_status = {
        GPIO.HIGH: "GPIO.HIGH",
        GPIO.LOW:  "GPIO.LOW"
        }

status = 0
for board in [GPIO.BOARD, GPIO.BCM, GPIO.SOC]:
    name = channel_data[board]["name"]
    pins = channel_data[board]["pins"]
    print("Testing the pins in [{}] mode".format(name))
    for v in [GPIO.HIGH, GPIO.LOW]:
        GPIO.setmode(board)
        GPIO.setup(pins, GPIO.OUT)

        print("    Setting all pins to {}".format(pin_status[v]))
        GPIO.output(pins, v)

        for pin in pins:
            GPIO.setmode(board)
            GPIO.setup(pin, GPIO.IN)
            value = GPIO.input(pin)
            if value != v:
                print("******* FAILED: Pin [{}] value check. Expecting {} but got {} *******".format(pin, pin_status[v], pin_status[value]))
                status = -1
            else:
                print("        PASSED: Pin [{}] value check. Expecting {} and got {}".format(pin, pin_status[v], pin_status[value]))
            GPIO.cleanup()

# Return the status
sys.exit(status)
