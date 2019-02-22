"""
libhdhomerun

libhdhomerun is a python module for accessing the SiliconDust
shared library using python ctypes foreign function technology.

Copyright (c) 2012 by Gary Buhrmaster <gary.buhrmaster@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__author__      = "Gary Buhrmaster"
__copyright__   = "Copyright 2012, Gary Buhrmaster"
__credits__     = ["Gary Buhrmaster"]
__license__     = "Apache License 2.0"
__version__     = "0.1.2"
__maintainer__  = "Gary Buhrmaster"
__email__       = "gary.buhrmaster@gmail.com"
__status__      = "Beta"
__title__       = "libhdhomerun"

import ctypes
import sys
import logging

HDHOMERUN_STATUS_COLOR_NEUTRAL            = 0xFFFFFFFF
HDHOMERUN_STATUS_COLOR_RED                = 0xFFFF0000
HDHOMERUN_STATUS_COLOR_YELLOW             = 0xFFFFFF00
HDHOMERUN_STATUS_COLOR_GREEN              = 0xFF00C000
HDHOMERUN_CHANNELSCAN_MAX_PROGRAM_COUNT   = 64
HDHOMERUN_CHANNELSCAN_PROGRAM_NORMAL      = 0
HDHOMERUN_CHANNELSCAN_PROGRAM_NODATA      = 1
HDHOMERUN_CHANNELSCAN_PROGRAM_CONTROL     = 2
HDHOMERUN_CHANNELSCAN_PROGRAM_ENCRYPTED   = 3
HDHOMERUN_DEVICE_TYPE_WILDCARD            = 0xFFFFFFFF
HDHOMERUN_DEVICE_TYPE_TUNER               = 0x00000001
HDHOMERUN_DEVICE_ID_WILDCARD              = 0xFFFFFFFF
HDHOMERUN_DEVICE_MAX_TUNE_TO_LOCK_TIME    = 1500
HDHOMERUN_DEVICE_MAX_LOCK_TO_DATA_TIME    = 2000
HDHOMERUN_DEVICE_MAX_TUNE_TO_DATA_TIME    = (HDHOMERUN_DEVICE_MAX_TUNE_TO_LOCK_TIME + HDHOMERUN_DEVICE_MAX_LOCK_TO_DATA_TIME)
TS_PACKET_SIZE                            = 188
VIDEO_DATA_PACKET_SIZE                    = (188 * 7)
VIDEO_DATA_BUFFER_SIZE_1S                 = (20000000 / 8)
VIDEO_RTP_DATA_PACKET_SIZE                = ((188 * 7) + 12)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class hdhomerun_device_t(ctypes.Structure):
    pass


class hdhomerun_debug_t(ctypes.Structure):
    pass


class hdhomerun_control_sock_t(ctypes.Structure):
    pass


class hdhomerun_video_sock_t(ctypes.Structure):
    pass


class hdhomerun_video_stats_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_video.h
    struct hdhomerun_video_stats_t {
        uint32_t packet_count;
        uint32_t network_error_count;
        uint32_t transport_error_count;
        uint32_t sequence_error_count;
        uint32_t overflow_error_count;
    };
    '''
    _fields_ = [
        ("packet_count", ctypes.c_uint32),
        ("network_error_count", ctypes.c_uint32),
        ("transport_error_count", ctypes.c_uint32),
        ("sequence_error_count", ctypes.c_uint32),
        ("overflow_error_count", ctypes.c_uint32)
    ]


class hdhomerun_tuner_status_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_types.h
    struct hdhomerun_tuner_status_t {
        char channel[32];
        char lock_str[32];
        bool signal_present;
        bool lock_supported;
        bool lock_unsupported;
        unsigned int signal_strength;
        unsigned int signal_to_noise_quality;
        unsigned int symbol_error_quality;
        uint32_t raw_bits_per_second;
        uint32_t packets_per_second;
    };
    '''
    _fields_ = [
        ("channel", ctypes.c_char * 32),
        ("lock_str", ctypes.c_char * 32),
        ("signal_present", ctypes.c_bool),
        ("lock_supported", ctypes.c_bool),
        ("lock_unsupported", ctypes.c_bool),
        ("signal_strength", ctypes.c_uint32),
        ("signal_to_noise_quality", ctypes.c_uint32),
        ("symbol_error_quality", ctypes.c_uint32),
        ("raw_bits_per_second", ctypes.c_uint32),
        ("packets_per_second", ctypes.c_uint32)
    ]


class hdhomerun_tuner_vstatus_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_types.h
    struct hdhomerun_tuner_vstatus_t {
        char vchannel[32];
        char name[32];
        char auth[32];
        char cci[32];
        char cgms[32];
        bool not_subscribed;
        bool not_available;
        bool copy_protected;
    };
    '''
    _fields_ = [
        ("vchannel", ctypes.c_char * 32),
        ("name", ctypes.c_char * 32),
        ("auth", ctypes.c_char * 32),
        ("cci", ctypes.c_char * 32),
        ("cgms", ctypes.c_char * 32),
        ("not_subscribed", ctypes.c_bool),
        ("not_available", ctypes.c_bool),
        ("copy_protected", ctypes.c_bool)
    ]


class hdhomerun_channelscan_program_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_types.h
    struct hdhomerun_channelscan_program_t {
        char program_str[64];
        uint16_t program_number;
        uint16_t virtual_major;
        uint16_t virtual_minor;
        uint16_t type;
        char name[32];
    };
    '''
    _fields_ = [
        ("program", ctypes.c_char * 64),
        ("program_number", ctypes.c_uint16),
        ("virtual_major", ctypes.c_uint16),
        ("virtual_minor", ctypes.c_uint16),
        ("type", ctypes.c_uint16),
        ("name", ctypes.c_char * 32)
    ]


class hdhomerun_channelscan_result_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_types.h
    struct hdhomerun_channelscan_result_t {
        char channel_str[64];
        uint32_t channelmap;
        uint32_t frequency;
        struct hdhomerun_tuner_status_t status;
        int program_count;
        struct hdhomerun_channelscan_program_t programs[HDHOMERUN_CHANNELSCAN_MAX_PROGRAM_COUNT];
        bool transport_stream_id_detected;
        bool original_network_id_detected;
        uint16_t transport_stream_id;
        uint16_t original_network_id;
    };
    '''
    _fields_ = [
        ("channel_str", ctypes.c_char * 64),
        ("channelmap", ctypes.c_uint32),
        ("frequency", ctypes.c_uint32),
        ("status", hdhomerun_tuner_status_t),
        ("program_count", ctypes.c_int32),
        (
            "programs",
            hdhomerun_channelscan_program_t * 
            HDHOMERUN_CHANNELSCAN_MAX_PROGRAM_COUNT
        ),
        ("transport_stream_id_detected", ctypes.c_bool),
        ("original_network_id_detected", ctypes.c_bool),
        ("transport_stream_id", ctypes.c_uint16),
        ("original_network_id", ctypes.c_uint16),
    ]


class hdhomerun_plotsample_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_types.h
    struct hdhomerun_plotsample_t {
        int16_t real;
        int16_t imag;
    };
    '''
    _fields_ = [
        ("real", ctypes.c_int16),
        ("imag", ctypes.c_int16),
    ]


class hdhomerun_discover_device_t(ctypes.Structure):
    '''
    https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_discover.h
    struct hdhomerun_discover_device_t {
        uint32_t ip_addr;
        uint32_t device_type;
        uint32_t device_id;
        uint8_t tuner_count;
        bool is_legacy;
        char device_auth[25];
        char base_url[29];
    };
    '''
    _fields_ = [
        ("ip_addr", ctypes.c_uint32),
        ("device_type", ctypes.c_uint32),
        ("device_id", ctypes.c_uint32),
        ("tuner_count", ctypes.c_uint8),
        ("is_legacy", ctypes.c_bool),
        ("device_auth", ctypes.c_char * 25),
        ("base_url", ctypes.c_char * 29),
    ]

# Define function prototypes...
__prototypes = (
    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API struct hdhomerun_device_t
            *hdhomerun_device_create(
                uint32_t device_id,
                uint32_t device_ip,
                unsigned int tuner,
                struct hdhomerun_debug_t *dbg
            );
        ''',
        'hdhomerun_device_create',
        ctypes.POINTER(hdhomerun_device_t),
        (
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint,
            ctypes.POINTER(hdhomerun_debug_t)
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API struct hdhomerun_device_t 
            *hdhomerun_device_create_from_str(
                uint32_t device_id,
                uint32_t device_ip,
                unsigned int tuner,
                struct hdhomerun_debug_t *dbg
            );
        ''',
        'hdhomerun_device_create_from_str',
        ctypes.POINTER(hdhomerun_device_t),
        (
            ctypes.c_char_p,
            ctypes.POINTER(hdhomerun_debug_t)
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API void
            hdhomerun_device_destroy(
                struct hdhomerun_device_t *hd
            );
        ''',
        'hdhomerun_device_destroy',
        ctypes.c_void_p,
        (
            ctypes.POINTER(hdhomerun_device_t),
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_discover.h

        extern LIBHDHOMERUN_API void
            hdhomerun_discover_destroy(
                struct hdhomerun_discover_t *ds
            );
        ''',
        'hdhomerun_discover_destroy',
        ctypes.c_void_p,
        (
            ctypes.POINTER(hdhomerun_discover_device_t),
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_discover.h

        extern LIBHDHOMERUN_API int
            hdhomerun_discover_find_devices_custom_v2(
                uint32_t target_ip,
                uint32_t device_type,
                uint32_t device_id,
                struct hdhomerun_discover_device_t result_list[],
                int max_count
            );
        ''',
        'hdhomerun_discover_find_devices_custom_v2',
        ctypes.c_int32,
        (
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.POINTER(hdhomerun_discover_device_t),
            ctypes.c_int
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API uint32_t
            hdhomerun_device_get_device_id(
                struct hdhomerun_device_t *hd
            );
        ''',
        'hdhomerun_device_get_device_id',
        ctypes.c_uint32,
        (
            ctypes.POINTER(hdhomerun_device_t),
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API uint32_t
            hdhomerun_device_get_device_ip(
                struct hdhomerun_device_t *hd
            );
        ''',
        'hdhomerun_device_get_device_ip',
        ctypes.c_uint32,
        (
            ctypes.POINTER(hdhomerun_device_t),
        )
    ),

    (
        '''https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API const char *
            hdhomerun_device_get_model_str(
                struct hdhomerun_device_t *hd
            );
        ''',
        'hdhomerun_device_get_model_str',
        ctypes.c_char_p,
        (
            ctypes.POINTER(hdhomerun_device_t),
        )
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API int
            hdhomerun_device_get_tuner_channelmap(
                struct hdhomerun_device_t *hd,
                char **pchannelmap
            );
        ''',
        'hdhomerun_device_get_tuner_channelmap',
        ctypes.c_int32,
        (
            ctypes.POINTER(hdhomerun_device_t),
            ctypes.POINTER(ctypes.c_char_p),
        ),
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_channels.h

        extern LIBHDHOMERUN_API const char *
            hdhomerun_channelmap_get_channelmap_scan_group(
                const char *channelmap
            );
        ''',
        'hdhomerun_channelmap_get_channelmap_scan_group',
        ctypes.c_char_p,
        (
            ctypes.c_char_p,
        ),
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API int
            hdhomerun_device_channelscan_init(
                struct hdhomerun_device_t *hd,
                const char *channelmap
            );
        ''',
        'hdhomerun_device_channelscan_init',
        ctypes.c_int32,
        (
            ctypes.POINTER(hdhomerun_device_t),
            ctypes.c_char_p,
        ),
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API int
            hdhomerun_device_channelscan_advance(
                struct hdhomerun_device_t *hd,
                struct hdhomerun_channelscan_result_t *result
            );
        ''',
        'hdhomerun_device_channelscan_advance',
        ctypes.c_int32,
        (
            ctypes.POINTER(hdhomerun_device_t),
            ctypes.POINTER(hdhomerun_channelscan_result_t),
        ),
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API int
            hdhomerun_device_channelscan_detect(
                struct hdhomerun_device_t *hd,
                struct hdhomerun_channelscan_result_t *result
            );
        ''',
        'hdhomerun_device_channelscan_detect',
        ctypes.c_int32,
        (
            ctypes.POINTER(hdhomerun_device_t),
            ctypes.POINTER(hdhomerun_channelscan_result_t),
        ),
    ),

    (
        '''
        https://github.com/Silicondust/libhdhomerun/blob/master/hdhomerun_device.h

        extern LIBHDHOMERUN_API uint8_t
            hdhomerun_device_channelscan_get_progress(
                struct hdhomerun_device_t *hd
            );
        ''',
        'hdhomerun_device_channelscan_get_progress',
        ctypes.c_uint8,
        (
            ctypes.POINTER(hdhomerun_device_t),
        ),
    ),
)

# Due to platform/compiler differences, the shared library
# may have differing names on differing platforms.  Try the
# alternatives on the specified platforms (POSIX is the default)
if (sys.platform == 'darwin'):
    __lib_name_formats = [
        'lib%s.dylib', 'lib%s.so', 'lib%s.bundle', '%s.dylib', '%s.so',
        '%s.bundle', '%s'
    ]
elif (sys.platform == 'win32') or (sys.platform == 'cygwin'):
    __lib_name_formats = ['lib%s.dll', '%s.dll', '%slib.dll']
else:
    __lib_name_formats = ['lib%s.so', 'lib%s.sl', '%s.so', '%s.sl']

__libhdhomerun = None
__lib_errors = []

for __lib_name in __lib_name_formats:
    __libname = __lib_name % ('hdhomerun')
    try:
        __libhdhomerun = ctypes.CDLL(__libname)
        break

    except Exception as e:
        __lib_errors.append('Attempting to load %s: ' % (__libname) + str(e))

# Raise the error for failing to load library, displaying
# all the accumlated places that were searched....
if __libhdhomerun is None:
    __lib_load_error = ('; '.join(__lib_errors))
    raise OSError(__lib_load_error)

# Convert prototypes into module functions...
module = sys.modules[__name__]

for doc, name, restype, argtypes in __prototypes:
    try:
        func = getattr(__libhdhomerun, name)
    except AttributeError:
        raise AttributeError('libhdhomerun has no function: %s' % name)

    func.__doc__ = doc
    func.restype = restype
    func.argtypes = argtypes

    # Install functon to this module.
    setattr(module, name, func)
