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

J721E_SK = 'J721E_SK'
AM68_SK  = 'AM68_SK'
AM69_SK  = 'AM69_SK'

OFFSET_ENTRY        = 0
GPIO_NAME_ENTRY     = 1 # Currently unused
SYSFS_DIR_ENTRY     = 2
BOARD_PIN_ENTRY     = 3
BCM_PIN_ENTRY       = 4
SOC_NAME_ENTRY      = 5
PWM_SYSFS_DIR_ENTRY = 6
PWM_ID_ENTRY        = 7

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
#   OFFSET     sysfs_dir    BOARD BCM SOC_NAME   PWM_SysFs       PWM_Id
    ( 84, {}, "600000.gpio",  3,   2, 'GPIO0_84',  None,          None),
    ( 83, {}, "600000.gpio",  5,   3, 'GPIO0_83',  None,          None),
    (  7, {}, "600000.gpio",  7,   4, 'GPIO0_7',   None,          None),
    ( 70, {}, "600000.gpio",  8,  14, 'GPIO0_70',  None,          None),
    ( 81, {}, "600000.gpio", 10,  15, 'GPIO0_81',  None,          None),
    ( 71, {}, "600000.gpio", 11,  17, 'GPIO0_71',  None,          None),
    (  1, {}, "600000.gpio", 12,  18, 'GPIO0_1',   None,          None),
    ( 82, {}, "600000.gpio", 13,  27, 'GPIO0_82',  None,          None),
    ( 11, {}, "600000.gpio", 15,  22, 'GPIO0_11',  None,          None),
    (  5, {}, "600000.gpio", 16,  23, 'GPIO0_5',   None,          None),
    ( 12, {}, "601000.gpio", 18,  24, 'GPIO0_12',  None,          None),
    (101, {}, "600000.gpio", 19,  10, 'GPIO0_101', None,          None),
    (107, {}, "600000.gpio", 21,   9, 'GPIO0_107', None,          None),
    (  8, {}, "600000.gpio", 22,  25, 'GPIO0_8',   None,          None),
    (103, {}, "600000.gpio", 23,  11, 'GPIO0_103', None,          None),
    (102, {}, "600000.gpio", 24,   8, 'GPIO0_102', None,          None),
    (108, {}, "600000.gpio", 26,   7, 'GPIO0_108', None,          None),
    ( 93, {}, "600000.gpio", 29,   5, 'GPIO0_93',  '3020000.pwm', 0   ),
    ( 94, {}, "600000.gpio", 31,   6, 'GPIO0_94',  '3020000.pwm', 1   ),
    ( 98, {}, "600000.gpio", 32,  12, 'GPIO0_98',  '3030000.pwm', 0   ),
    ( 99, {}, "600000.gpio", 33,  13, 'GPIO0_99',  '3030000.pwm', 1   ),
    (  2, {}, "600000.gpio", 35,  19, 'GPIO0_2',   None,          None),
    ( 97, {}, "600000.gpio", 36,  16, 'GPIO0_97',  None,          None),
    (115, {}, "600000.gpio", 37,  26, 'GPIO0_115', None,          None),
    (  3, {}, "600000.gpio", 38,  20, 'GPIO0_3',   None,          None),
    (  4, {}, "600000.gpio", 40,  21, 'GPIO0_4',   None,          None)
]

compats_j721e = (
    'ti,j721e-sk',
    'ti,j721e',
)

AM68_SK_PIN_DEFS = [
#   OFFSET     sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    ( 4, {}, "600000.gpio",    3,   2, 'GPIO0_4',       None, None),
    ( 5, {}, "600000.gpio",    5,   3, 'GPIO0_5',       None, None),
    (66, {}, "42110000.gpio",  7,   4, 'WKUP_GPIO0_66', None, None),
    ( 1, {}, "600000.gpio",    8,  14, 'GPIO0_1',       None, None),
    ( 2, {}, "600000.gpio",   10,  15, 'GPIO0_2',       None, None),
    (42, {}, "600000.gpio",   11,  17, 'GPIO0_42',      None, None),
    (46, {}, "600000.gpio",   12,  18, 'GPIO0_46',      None, None),
    (36, {}, "600000.gpio",   13,  27, 'GPIO0_36',      None, None),
    (49, {}, "42110000.gpio", 15,  22, 'WKUP_GPIO0_49', None, None),
    ( 3, {}, "600000.gpio",   16,  23, 'GPIO0_3',       None, None),
    (13, {}, "600000.gpio",   18,  24, 'GPIO0_13',      None, None),
    ( 1, {}, "42110000.gpio", 19,  10, 'WKUP_GPIO0_1',  None, None),
    ( 2, {}, "42110000.gpio", 21,   9, 'WKUP_GPIO0_2',  None, None),
    (67, {}, "42110000.gpio", 22,  25, 'WKUP_GPIO0_67', None, None),
    ( 0, {}, "42110000.gpio", 23,  11, 'WKUP_GPIO0_0',  None, None),
    ( 3, {}, "42110000.gpio", 24,   8, 'WKUP_GPIO0_3',  None, None),
    (15, {}, "42110000.gpio", 26,   7, 'WKUP_GPIO0_15', None, None),
    (56, {}, "42110000.gpio", 29,   5, 'WKUP_GPIO0_56', None, None),
    (57, {}, "42110000.gpio", 31,   6, 'WKUP_GPIO0_57', None, None),
    (35, {}, "600000.gpio",   32,  12, 'GPIO0_35',      None, None),
    (51, {}, "600000.gpio",   33,  13, 'GPIO0_51',      None, None),
    (47, {}, "600000.gpio",   35,  19, 'GPIO0_47',      None, None),
    (41, {}, "600000.gpio",   36,  16, 'GPIO0_41',      None, None),
    (27, {}, "600000.gpio",   37,  26, 'GPIO0_27',      None, None),
    (48, {}, "600000.gpio",   38,  20, 'GPIO0_48',      None, None),
    (45, {}, "600000.gpio",   40,  21, 'GPIO0_45',      None, None)
]

compats_am68sk = (
    'ti,am68-sk',
    'ti,j721s2',
)

AM69_SK_PIN_DEFS = [
#   OFFSET     sysfs_dir      BOARD BCM SOC_NAME    PWM_SysFs  PWM_Id
    (87, {}, "42110000.gpio",  3,  2,  'WKUP_GPIO0_87', None, None),
    (65, {}, "600000.gpio",    5,  3,  'WKUP_GPIO0_65', None, None),
    (66, {}, "42110000.gpio",  7,  4,  'WKUP_GPIO0_66', None, None),
    ( 1, {}, "600000.gpio",    8, 14,  'GPIO0_1',       None, None),
    ( 2, {}, "600000.gpio",   10, 15,  'GPIO0_2',       None, None),
    (42, {}, "600000.gpio",   11, 17,  'GPIO0_42',      None, None),
    (46, {}, "600000.gpio",   12, 18,  'GPIO0_46',      None, None),
    (36, {}, "600000.gpio",   13, 27,  'GPIO0_36',      None, None),
    (49, {}, "42110000.gpio", 15, 22,  'GPIO0_49',      None, None),
    ( 3, {}, "600000.gpio",   16, 23,  'GPIO0_3',       None, None),
    (13, {}, "600000.gpio",   18, 24,  'GPIO0_13',      None, None),
    ( 1, {}, "42110000.gpio", 19, 10,  'WKUP_GPIO0_1',  None, None),
    ( 2, {}, "42110000.gpio", 21,  9,  'WKUP_GPIO0_2',  None, None),
    (67, {}, "42110000.gpio", 22, 25,  'WKUP_GPIO0_67', None, None),
    ( 0, {}, "42110000.gpio", 23, 11,  'WKUP_GPIO0_0',  None, None),
    ( 3, {}, "42110000.gpio", 24,  8,  'WKUP_GPIO0_3',  None, None),
    (15, {}, "42110000.gpio", 26,  7,  'WKUP_GPIO0_15', None, None),
    (56, {}, "42110000.gpio", 29,  5,  'WKUP_GPIO0_56', None, None),
    (57, {}, "42110000.gpio", 31,  6,  'WKUP_GPIO0_57', None, None),
    (35, {}, "600000.gpio",   32, 12,  'GPIO0_35',      None, None),
    (51, {}, "600000.gpio",   33, 13,  'GPIO0_51',      None, None),
    (47, {}, "600000.gpio",   35, 19,  'GPIO0_47',      None, None),
    (41, {}, "600000.gpio",   36, 16,  'GPIO0_41',      None, None),
    (27, {}, "600000.gpio",   37, 26,  'GPIO0_27',      None, None),
    (48, {}, "600000.gpio",   38, 20,  'GPIO0_48',      None, None),
    (45, {}, "600000.gpio",   40, 21,  'GPIO0_45',      None, None),
]

compats_am69sk = (
    'ti,am69-sk',
    'ti,j784s4',
)

board_gpio_data = {
    J721E_SK: (
        J721E_SK_PIN_DEFS,
        {
            'RAM': '4096M',
            'REVISION': 'E2',
            'TYPE': 'J721E-EAIK',
            'MANUFACTURER': 'TI',
            'PROCESSOR': 'ARM A72'
        }
    ),

    AM68_SK: (
        AM68_SK_PIN_DEFS,
        {
            'RAM': '4096M',
            'REVISION': 'E2',
            'TYPE': 'AM68-SK',
            'MANUFACTURER': 'TI',
            'PROCESSOR': 'ARM A72'
        }
    ),

    AM69_SK: (
        AM69_SK_PIN_DEFS,
        {
            'RAM': '4096M',
            'REVISION': 'E2',
            'TYPE': 'AM69-SK',
            'MANUFACTURER': 'TI',
            'PROCESSOR': 'ARM A72'
        }
    ),
}

class ChannelInfo(object):
    def __init__(self, channel, gpio_chip_dir, chip_gpio, gpio, gpio_name, pwm_chip_dir, pwm_id):
        self.channel = channel
        self.gpio_chip_dir = gpio_chip_dir
        self.chip_gpio = chip_gpio
        self.gpio = gpio
        self.gpio_name = gpio_name
        self.pwm_chip_dir = pwm_chip_dir
        self.pwm_id = pwm_id

ids_warned = False

def get_data():
    compatible_path = '/proc/device-tree/compatible'
    ids_path = '/proc/device-tree/chosen/plugin-manager/ids'

    with open(compatible_path, 'r') as f:
        compatibles = f.read().split('\x00')

    def matches(vals):
        return any(v in compatibles for v in vals)

    def find_pmgr_board(prefix):
        global ids_warned
        if not os.path.exists(ids_path):
            if not ids_warned:
                ids_warned = True
                msg = """\
WARNING: Plugin manager information missing from device tree.
WARNING: Cannot determine whether the expected SK board is present.
"""
                sys.stderr.write(msg)
            return None
        for f in os.listdir(ids_path):
            if f.startswith(prefix):
                return f
        return None

    def warn_if_not_carrier_board(*carrier_boards):
        found = False
        for b in carrier_boards:
            found = find_pmgr_board(b + '-')
            if found:
                break
        if not found:
            msg = """\
WARNING: Carrier board is not from a SK Developer Kit.
WARNNIG: TI.GPIO library has not been verified with this carrier board,
WARNING: and in fact is unlikely to work correctly.
"""
            sys.stderr.write(msg)

    if matches(compats_j721e):
        model = J721E_SK
    elif matches(compats_am68sk):
        model = AM68_SK
    elif matches(compats_am69sk):
        model = AM69_SK
    else:
        raise Exception('Could not determine TI SOC model')

    pin_defs, board_info = board_gpio_data[model]
    gpio_chip_dirs = {}
    gpio_chip_base = {}
    gpio_chip_ngpio = {}
    pwm_dirs = {}

    sysfs_prefixes = ['/sys/devices/',
                      '/sys/devices/platform/',
                      '/sys/devices/platform/bus@100000/',
                      '/sys/devices/platform/bus@100000/bus@100000:bus@28380000/']

    # Get the gpiochip offsets
    gpio_chip_names = set([x[SYSFS_DIR_ENTRY] for x in pin_defs if x[SYSFS_DIR_ENTRY] is not None])
    for gpio_chip_name in gpio_chip_names:
        gpio_chip_dir = None
        for prefix in sysfs_prefixes:
            d = prefix + gpio_chip_name
            if os.path.isdir(d):
                gpio_chip_dir = d
                break
        if gpio_chip_dir is None:
            raise Exception('Cannot find GPIO chip ' + gpio_chip_name)
        gpio_chip_dirs[gpio_chip_name] = gpio_chip_dir
        gpio_chip_gpio_dir = gpio_chip_dir + '/gpio'
        for fn in os.listdir(gpio_chip_gpio_dir):
            if not fn.startswith('gpiochip'):
                continue
            base_fn = gpio_chip_gpio_dir + '/' + fn + '/base'
            with open(base_fn, 'r') as f:
                gpio_chip_base[gpio_chip_name] = int(f.read().strip())
            ngpio_fn = gpio_chip_gpio_dir + '/' + fn + '/ngpio'
            with open(ngpio_fn, 'r') as f:
                gpio_chip_ngpio[gpio_chip_name] = int(f.read().strip())
            break

    def global_gpio_id_name(chip_relative_ids, gpio_names, gpio_chip_name):
        chip_gpio_ngpio = gpio_chip_ngpio[gpio_chip_name]
        if isinstance(chip_relative_ids, dict):
            chip_relative_id = chip_relative_ids[chip_gpio_ngpio]
        else:
            chip_relative_id = chip_relative_ids
        gpio = gpio_chip_base[gpio_chip_name] + chip_relative_id
        if isinstance(gpio_names, dict):
            gpio_name = gpio_names.get(chip_gpio_ngpio, None)
        else:
            gpio_name = gpio_names
        if gpio_name is None:
            gpio_name = 'gpio%i' % gpio
        return (gpio, gpio_name)

    pwm_chip_names = set([x[PWM_SYSFS_DIR_ENTRY] for x in pin_defs if x[PWM_SYSFS_DIR_ENTRY] is not None])
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
        pwm_chip_pwm_dir = pwm_chip_dir + '/pwm'
        if not os.path.exists(pwm_chip_pwm_dir):
            continue
        for fn in os.listdir(pwm_chip_pwm_dir):
            if not fn.startswith('pwmchip'):
                continue
            pwm_chip_pwm_pwmchipn_dir = pwm_chip_pwm_dir + '/' + fn
            pwm_dirs[pwm_chip_name] = pwm_chip_pwm_pwmchipn_dir
            break

    def model_data(key_col, pin_defs):
        return {x[key_col]: ChannelInfo(
            x[key_col],
            gpio_chip_dirs[x[SYSFS_DIR_ENTRY]],
            x[OFFSET_ENTRY],
            *global_gpio_id_name(*x[OFFSET_ENTRY:BOARD_PIN_ENTRY]),
            pwm_chip_dir=pwm_dirs.get(x[PWM_SYSFS_DIR_ENTRY], None),
            pwm_id=x[PWM_ID_ENTRY]) for x in pin_defs}

    channel_data = {
        'BOARD': model_data(BOARD_PIN_ENTRY, pin_defs),
        'BCM': model_data(BCM_PIN_ENTRY, pin_defs),
        'SOC': model_data(SOC_NAME_ENTRY, pin_defs),
    }

    return model, board_info, channel_data
