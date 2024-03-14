# Copyright (c) 2018-2020, NVIDIA CORPORATION. All rights reserved.
# Copyright (c) 2021-2023, Texas Instruments Incorporated. All rights reserved.
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

import os
import os.path
import sys

J721E_SK = "J721E_SK"
AM68_SK = "AM68_SK"
AM69_SK = "AM69_SK"
AM62A_SK = "AM62A_SK"
AM62P_SK = "AM62P_SK"

OFFSET_ENTRY = 0
GPIO_CHIP_ENTRY = 1
SYSFS_DIR_ENTRY = 2
BOARD_PIN_ENTRY = 3
BCM_PIN_ENTRY = 4
SOC_NAME_ENTRY = 5
PWM_SYSFS_DIR_ENTRY = 6
PWM_ID_ENTRY = 7

# These arrays contain tuples of all the relevant GPIO data for each SOC
# Platform. The fields are:
# - Linux GPIO pin number (within chip, not global),
#   (map from chip GPIO count to value, to cater for different numbering schemes)
# - Linux exported GPIO name,
#   (map from chip GPIO count to value, to cater for different naming schemes)
#   (entries omitted if exported filename is gpio%i)
# - GPIO chip sysfs directory
# - Pin number (BOARD mode)
# - Pin number (BCM mode)
# - Pin name (SOC mode)
# - PWM chip sysfs directory
# - PWM ID within PWM chip
# The values are used to generate dictionaries that map the corresponding pin
# mode numbers to the Linux GPIO pin number and GPIO chip directory

J721E_SK_PIN_DEFS = [
    #   OFFSET  GPIOCHIP_X   sysfs_dir    BOARD BCM SOC_NAME   PWM_SysFs       PWM_Id
    (84, 1, "600000.gpio", 3, 2, "GPIO0_84", None, None),
    (83, 1, "600000.gpio", 5, 3, "GPIO0_83", None, None),
    (7, 1, "600000.gpio", 7, 4, "GPIO0_7", None, None),
    (70, 1, "600000.gpio", 8, 14, "GPIO0_70", None, None),
    (81, 1, "600000.gpio", 10, 15, "GPIO0_81", None, None),
    (71, 1, "600000.gpio", 11, 17, "GPIO0_71", None, None),
    (1, 1, "600000.gpio", 12, 18, "GPIO0_1", None, None),
    (82, 1, "600000.gpio", 13, 27, "GPIO0_82", None, None),
    (11, 1, "600000.gpio", 15, 22, "GPIO0_11", None, None),
    (5, 1, "600000.gpio", 16, 23, "GPIO0_5", None, None),
    (12, 2, "601000.gpio", 18, 24, "GPIO0_12", None, None),
    (101, 1, "600000.gpio", 19, 10, "GPIO0_101", None, None),
    (107, 1, "600000.gpio", 21, 9, "GPIO0_107", None, None),
    (8, 1, "600000.gpio", 22, 25, "GPIO0_8", None, None),
    (103, 1, "600000.gpio", 23, 11, "GPIO0_103", None, None),
    (102, 1, "600000.gpio", 24, 8, "GPIO0_102", None, None),
    (108, 1, "600000.gpio", 26, 7, "GPIO0_108", None, None),
    (93, 1, "600000.gpio", 29, 5, "GPIO0_93", "3020000.pwm", 0),
    (94, 1, "600000.gpio", 31, 6, "GPIO0_94", "3020000.pwm", 1),
    (98, 1, "600000.gpio", 32, 12, "GPIO0_98", "3030000.pwm", 0),
    (99, 1, "600000.gpio", 33, 13, "GPIO0_99", "3030000.pwm", 1),
    (2, 1, "600000.gpio", 35, 19, "GPIO0_2", None, None),
    (97, 1, "600000.gpio", 36, 16, "GPIO0_97", None, None),
    (115, 1, "600000.gpio", 37, 26, "GPIO0_115", None, None),
    (3, 1, "600000.gpio", 38, 20, "GPIO0_3", None, None),
    (4, 1, "600000.gpio", 40, 21, "GPIO0_4", None, None),
]

compats_j721e = (
    "ti,j721e-sk",
    "ti,j721e",
)

AM68_SK_PIN_DEFS = [
    #   OFFSET   GPIOCHIP_X  sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    (4, 4, "600000.gpio", 3, 2, "GPIO0_4", None, None),
    (5, 4, "600000.gpio", 5, 3, "GPIO0_5", None, None),
    (66, 3, "42110000.gpio", 7, 4, "WKUP_GPIO0_66", None, None),
    (1, 4, "600000.gpio", 8, 14, "GPIO0_1", None, None),
    (2, 4, "600000.gpio", 10, 15, "GPIO0_2", None, None),
    (42, 4, "600000.gpio", 11, 17, "GPIO0_42", None, None),
    (46, 4, "600000.gpio", 12, 18, "GPIO0_46", None, None),
    (36, 4, "600000.gpio", 13, 27, "GPIO0_36", None, None),
    (49, 3, "42110000.gpio", 15, 22, "WKUP_GPIO0_49", None, None),
    (3, 4, "600000.gpio", 16, 23, "GPIO0_3", None, None),
    (13, 4, "600000.gpio", 18, 24, "GPIO0_13", None, None),
    (1, 3, "42110000.gpio", 19, 10, "WKUP_GPIO0_1", None, None),
    (2, 3, "42110000.gpio", 21, 9, "WKUP_GPIO0_2", None, None),
    (67, 3, "42110000.gpio", 22, 25, "WKUP_GPIO0_67", None, None),
    (0, 3, "42110000.gpio", 23, 11, "WKUP_GPIO0_0", None, None),
    (3, 3, "42110000.gpio", 24, 8, "WKUP_GPIO0_3", None, None),
    (15, 3, "42110000.gpio", 26, 7, "WKUP_GPIO0_15", None, None),
    (56, 3, "42110000.gpio", 29, 5, "WKUP_GPIO0_56", None, None),
    (57, 3, "42110000.gpio", 31, 6, "WKUP_GPIO0_57", None, None),
    (35, 4, "600000.gpio", 32, 12, "GPIO0_35", "3030000.pwm", 0),
    (51, 4, "600000.gpio", 33, 13, "GPIO0_51", "3000000.pwm", 0),
    (47, 4, "600000.gpio", 35, 19, "GPIO0_47", None, None),
    (41, 4, "600000.gpio", 36, 16, "GPIO0_41", "3040000.pwm", 0),
    (27, 4, "600000.gpio", 37, 26, "GPIO0_27", None, None),
    (48, 4, "600000.gpio", 38, 20, "GPIO0_48", None, None),
    (45, 4, "600000.gpio", 40, 21, "GPIO0_45", None, None),
]

compats_am68sk = (
    "ti,am68-sk",
    "ti,j721s2",
)

AM69_SK_PIN_DEFS = [
    #   OFFSET   GPIOCHIP_X  sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    (87, 2, "42110000.gpio", 3, 2, "WKUP_GPIO0_87", None, None),
    (65, 3, "600000.gpio", 5, 3, "WKUP_GPIO0_65", None, None),
    (66, 2, "42110000.gpio", 7, 4, "WKUP_GPIO0_66", None, None),
    (1, 3, "600000.gpio", 8, 14, "GPIO0_1", None, None),
    (2, 3, "600000.gpio", 10, 15, "GPIO0_2", None, None),
    (42, 3, "600000.gpio", 11, 17, "GPIO0_42", None, None),
    (46, 3, "600000.gpio", 12, 18, "GPIO0_46", None, None),
    (36, 3, "600000.gpio", 13, 27, "GPIO0_36", None, None),
    (49, 2, "42110000.gpio", 15, 22, "WKUP_GPIO0_49", None, None),
    (3, 3, "600000.gpio", 16, 23, "GPIO0_3", None, None),
    (13, 3, "600000.gpio", 18, 24, "GPIO0_13", None, None),
    (1, 2, "42110000.gpio", 19, 10, "WKUP_GPIO0_1", None, None),
    (2, 2, "42110000.gpio", 21, 9, "WKUP_GPIO0_2", None, None),
    (67, 2, "42110000.gpio", 22, 25, "WKUP_GPIO0_67", None, None),
    (0, 2, "42110000.gpio", 23, 11, "WKUP_GPIO0_0", None, None),
    (3, 2, "42110000.gpio", 24, 8, "WKUP_GPIO0_3", None, None),
    (15, 2, "42110000.gpio", 26, 7, "WKUP_GPIO0_15", None, None),
    (56, 2, "42110000.gpio", 29, 5, "WKUP_GPIO0_56", None, None),
    (57, 2, "42110000.gpio", 31, 6, "WKUP_GPIO0_57", None, None),
    (35, 3, "600000.gpio", 32, 12, "GPIO0_35", "3030000.pwm", 0),
    (51, 3, "600000.gpio", 33, 13, "GPIO0_51", "3000000.pwm", 0),
    (47, 3, "600000.gpio", 35, 19, "GPIO0_47", None, None),
    (41, 3, "600000.gpio", 36, 16, "GPIO0_41", "3040000.pwm", 0),
    (27, 3, "600000.gpio", 37, 26, "GPIO0_27", None, None),
    (48, 3, "600000.gpio", 38, 20, "GPIO0_48", None, None),
    (45, 3, "600000.gpio", 40, 21, "GPIO0_45", None, None),
]

compats_am69sk = (
    "ti,am69-sk",
    "ti,j784s4",
)

AM62A_SK_PIN_DEFS = [
    #   OFFSET   GPIOCHIP_X  sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    (44, 2, "600000.gpio", 3, 2, "I2C2_SDA", None, None),
    (43, 2, "600000.gpio", 5, 3, "I2C2_SCL", None, None),
    (30, 3, "601000.gpio", 7, 4, "GPIO1_30", None, None),
    (25, 3, "601000.gpio", 8, 14, "GPIO1_25", None, None),
    (24, 3, "601000.gpio", 10, 15, "GPIO1_24", None, None),
    (11, 3, "601000.gpio", 11, 17, "GPIO1_11", None, None),
    (14, 3, "601000.gpio", 12, 18, "GPIO1_14", "23000000.pwm", 1),
    (42, 2, "600000.gpio", 13, 27, "GPIO0_42", None, None),
    (22, 3, "601000.gpio", 15, 22, "GPIO1_22", None, None),
    (38, 2, "600000.gpio", 16, 23, "GPIO0_38", None, None),
    (39, 2, "600000.gpio", 18, 24, "GPIO0_39", None, None),
    (18, 3, "601000.gpio", 19, 10, "GPIO1_18", None, None),
    (19, 3, "601000.gpio", 21, 9, "GPIO1_19", None, None),
    (14, 2, "600000.gpio", 22, 25, "GPIO0_14", None, None),
    (17, 3, "601000.gpio", 23, 11, "GPIO1_17", None, None),
    (15, 3, "601000.gpio", 24, 8, "GPIO1_15", None, None),
    (16, 3, "601000.gpio", 26, 7, "GPIO1_16", None, None),
    (36, 2, "600000.gpio", 29, 5, "GPIO0_36", None, None),
    (33, 2, "600000.gpio", 31, 6, "GPIO0_33", None, None),
    (40, 2, "600000.gpio", 32, 12, "GPIO0_40", None, None),
    (10, 3, "601000.gpio", 33, 13, "GPIO1_10", "23010000.pwm", 1),
    (13, 3, "601000.gpio", 35, 19, "GPIO1_13", "23000000.pwm", 0),
    (9,  3, "601000.gpio", 36, 16, "GPIO1_09", "23010000.pwm", 0),
    (41, 2, "600000.gpio", 37, 26, "GPIO0_41", None, None),
    (8,  3, "601000.gpio", 38, 20, "GPIO1_08", None, None),
    (7,  3, "601000.gpio", 40, 21, "GPIO1_07", None, None),
]

compats_am62ask = (
    "ti,am62a7-sk",
    "ti,am62a7",
)

AM62P_SK_PIN_DEFS = [
    #   OFFSET   GPIOCHIP_X  sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    (44, 1, "600000.gpio", 3, 2, "I2C2_SDA", None, None),
    (43, 1, "600000.gpio", 5, 3, "I2C2_SCL", None, None),
    (30, 2, "601000.gpio", 7, 4, "GPIO1_30", None, None),
    (25, 2, "601000.gpio", 8, 14, "GPIO1_25", None, None),
    (24, 2, "601000.gpio", 10, 15, "GPIO1_24", None, None),
    (11, 2, "601000.gpio", 11, 17, "GPIO1_11", None, None),
    (14, 2, "601000.gpio", 12, 18, "GPIO1_14", None, None),
    (42, 1, "600000.gpio", 13, 27, "GPIO0_42", None, None),
    (22, 2, "601000.gpio", 15, 22, "GPIO1_22", None, None),
    (38, 1, "600000.gpio", 16, 23, "GPIO0_38", None, None),
    (39, 1, "600000.gpio", 18, 24, "GPIO0_39", None, None),
    (18, 2, "601000.gpio", 19, 10, "GPIO1_18", None, None),
    (19, 2, "601000.gpio", 21, 9, "GPIO1_19", None, None),
    (14, 1, "600000.gpio", 22, 25, "GPIO0_14", None, None),
    (17, 2, "601000.gpio", 23, 11, "GPIO1_17", None, None),
    (15, 2, "601000.gpio", 24, 8, "GPIO1_15", "23000000.pwm", 0),
    (16, 2, "601000.gpio", 26, 7, "GPIO1_16", "23000000.pwm", 1),
    (36, 1, "600000.gpio", 29, 5, "GPIO0_36", None, None),
    (33, 1, "600000.gpio", 31, 6, "GPIO0_33", None, None),
    (40, 1, "600000.gpio", 32, 12, "GPIO0_40", None, None),
    (10, 2, "601000.gpio", 33, 13, "GPIO1_10", "23010000.pwm", 1),
    (13, 2, "601000.gpio", 35, 19, "GPIO1_13", None, None),
    (9,  2, "601000.gpio", 36, 16, "GPIO1_09", "23010000.pwm", 0),
    (41, 1, "600000.gpio", 37, 26, "GPIO0_41", None, None),
    (8,  2, "601000.gpio", 38, 20, "GPIO1_08", None, None),
    (7,  2, "601000.gpio", 40, 21, "GPIO1_07", None, None),
]

compats_am62psk = (
    "ti,am62p5-sk",
    "ti,am62p5",
)

board_gpio_data = {
    J721E_SK: (
        J721E_SK_PIN_DEFS,
        {
            "RAM": "4096M",
            "REVISION": "E2",
            "TYPE": "J721E-EAIK",
            "MANUFACTURER": "TI",
            "PROCESSOR": "ARM A72",
        },
    ),
    AM68_SK: (
        AM68_SK_PIN_DEFS,
        {
            "RAM": "4096M",
            "REVISION": "E2",
            "TYPE": "AM68-SK",
            "MANUFACTURER": "TI",
            "PROCESSOR": "ARM A72",
        },
    ),
    AM69_SK: (
        AM69_SK_PIN_DEFS,
        {
            "RAM": "4096M",
            "REVISION": "E2",
            "TYPE": "AM69-SK",
            "MANUFACTURER": "TI",
            "PROCESSOR": "ARM A72",
        },
    ),
    AM62A_SK: (
        AM62A_SK_PIN_DEFS,
        {
            "RAM": "4096M",
            "REVISION": "E2",
            "TYPE": "AM62A-SK",
            "MANUFACTURER": "TI",
            "PROCESSOR": "ARM A53",
        },
    ),
    AM62P_SK: (
        AM62P_SK_PIN_DEFS,
        {
            "RAM": "8192M",
            "REVISION": "E1",
            "TYPE": "AM62P-SK",
            "MANUFACTURER": "TI",
            "PROCESSOR": "ARM A53",
        },
    ),
}


class ChannelInfo(object):
    def __init__(
        self, channel, gpiochip, gpio, pwm_chip_dir, pwm_id
    ):
        self.channel = channel
        self.gpiochip = gpiochip
        self.gpio = gpio
        self.pwm_chip_dir = pwm_chip_dir
        self.pwm_id = pwm_id


ids_warned = False


def get_data():
    compatible_path = "/proc/device-tree/compatible"

    with open(compatible_path, "r") as f:
        compatibles = f.read().split("\x00")

    def matches(vals):
        return any(v in compatibles for v in vals)

    if matches(compats_j721e):
        model = J721E_SK
    elif matches(compats_am68sk):
        model = AM68_SK
    elif matches(compats_am69sk):
        model = AM69_SK
    elif matches(compats_am62ask):
        model = AM62A_SK
    elif matches(compats_am62psk):
        model = AM62P_SK

    else:
        raise Exception("Could not determine TI SOC model")

    pin_defs, board_info = board_gpio_data[model]
    pwm_dirs = {}

    sysfs_prefixes = [
        "/sys/devices/",
        "/sys/devices/platform/",
        "/sys/devices/platform/bus@100000/",
        "/sys/devices/platform/bus@100000/bus@100000:bus@28380000/",
        "/sys/devices/platform/bus@f0000/",
    ]

    pwm_chip_names = set(
        [x[PWM_SYSFS_DIR_ENTRY] for x in pin_defs if x[PWM_SYSFS_DIR_ENTRY] is not None]
    )
    for pwm_chip_name in pwm_chip_names:
        pwm_chip_dir = None
        for prefix in sysfs_prefixes:
            d = prefix + pwm_chip_name
            if os.path.isdir(d):
                pwm_chip_dir = d
                break
        # Some PWM controllers aren't enabled in all versions of the DT. In
        # this case, just hide the PWM function on this pin, but let all other
        # aspects of the library continue to work.
        if pwm_chip_dir is None:
            continue
        pwm_chip_pwm_dir = pwm_chip_dir + "/pwm"
        if not os.path.exists(pwm_chip_pwm_dir):
            continue
        for fn in os.listdir(pwm_chip_pwm_dir):
            if not fn.startswith("pwmchip"):
                continue
            pwm_chip_pwm_pwmchipn_dir = pwm_chip_pwm_dir + "/" + fn
            pwm_dirs[pwm_chip_name] = pwm_chip_pwm_pwmchipn_dir
            break

    def model_data(key_col, pin_defs):
        return {
            x[key_col]: ChannelInfo(
                x[key_col],
                x[GPIO_CHIP_ENTRY],
                x[OFFSET_ENTRY],
                pwm_chip_dir=pwm_dirs.get(x[PWM_SYSFS_DIR_ENTRY], None),
                pwm_id=x[PWM_ID_ENTRY]
            )
            for x in pin_defs
        }

    channel_data = {
        "BOARD": model_data(BOARD_PIN_ENTRY, pin_defs),
        "BCM": model_data(BCM_PIN_ENTRY, pin_defs),
        "SOC": model_data(SOC_NAME_ENTRY, pin_defs),
    }

    return model, board_info, channel_data
