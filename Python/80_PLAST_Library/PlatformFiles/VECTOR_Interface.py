# coding: utf-8
'''
Created on Mar 14, 2014

@author: uidv9994
'''

import ctypes
import time
from threading import Thread  # import only the Thread function
from ParserDBC_Interface import *
from ParserLDF_Interface import *
from array import array
import sys

XLuint64 = ctypes.c_ulonglong
XLaccess = XLuint64  # access mask
XLstatus = ctypes.c_short  # driver status
XLeventtag = ctypes.c_ubyte
XLporthandle = ctypes.c_long  # porthandle
XL_INVALID_PORTHANDLE = -1
b_HW_IO_CAB = False

# SIMULATED SLAVES DEFINES
SIMULATED_SLAVE_ID = 0
SIMULATED_SLAVE_DATA = 1
SIMULATED_SLAVE_DLC = 2
SIMULATED_SLAVE_CHECKSUM_TYPE = 3
SIMULATED_SLAVE_APPLICATION_ID = 4
SIMULATED_SLAVE_ALIVE_THRESHOLD = 5
SIMULATED_SLAVE_ALIVE_SHIFT_VALUE = 6
SIMULATED_SLAVE_CRC_BYTE_POSITION = 7
SIMULATED_SLAVE_ALIVE_BYTE_POSITION = 8

# Transceiver Type
XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO = 0x0139 # IO CAB
XL_TRANSCEIVER_TYPE_PB_DAIO_8642 = 0x0280   # IO Piggy
XL_TRANSCEIVER_TYPE_DAIO_1021_FIX = 0x013D  # Onboard IO of VN1630/VN1640

# driver status
XL_SUCCESS = 0
XL_PENDING = 1

# activate - channel flags
XL_ACTIVATE_NONE = 0
XL_ACTIVATE_RESET_CLOCK = 8

XL_RECEIVE_EVENT_SIZE = 512
XL_BUS_TYPE_NONE = 0x0
XL_BUS_TYPE_CAN = 0x1
XL_BUS_TYPE_LIN = 0x2
XL_BUS_TYPE_FLEXRAY = 0x4
XL_BUS_TYPE_MOST = 0x10
XL_BUS_TYPE_DAIO = 0x40 # IO cab/piggy
XL_BUS_TYPE_J1708 = 0x100

# interface version for our events
XL_INTERFACE_VERSION = 3

MAX_MSG_LEN = 8
XL_TRANSMIT_MSG = 10
WAIT_TIMEOUT = 0x102,
XL_ERR_QUEUE_IS_EMPTY = 10

# for LIN we have special events
XL_LIN_MSGFLAG_TX = 0x40
XL_LIN_MSG = 20
XL_LIN_ERRMSG = 21
XL_LIN_SYNCERR = 22
XL_LIN_NOANS = 23
XL_LIN_WAKEUP = 24
XL_LIN_SLEEP = 25
XL_LIN_CRCINFO = 26
XL_LIN_MASTER = 1
XL_LIN_SLAVE = 2
XL_LIN_VERSION_1_3 = 0x01  # //!< LIN version 1.3
XL_LIN_VERSION_2_0 = 0x02  # //!< LIN version 2.0
XL_LIN_VERSION_2_1 = 0x03  # //!< LIN version 2.1

# defines for lin_set_slave function
XL_LIN_CALC_CHECKSUM = 0x100
XL_LIN_CALC_CHECKSUM_ENHANCED = 0x200

# for D/A IO bus
XL_RECEIVE_DAIO_DATA = 32
XL_RECEIVE_DAIO_PIGGY= 34
XL_DAIO_TRIGGER_TYPE_CYCLIC = 0x01
XL_DAIO_TRIGGER_TYPE_PORT = 0x02

XL_DAIO_PORT_TYPE_MASK_DIGITAL = 0x01
XL_DAIO_PORT_TYPE_MASK_ANALOG = 0x02

# Port mask
XL_DAIO_PORT_MASK_DIGITAL_D0 = 0x01
XL_DAIO_PORT_MASK_DIGITAL_D1 = 0x02
XL_DAIO_PORT_MASK_DIGITAL_D2 = 0x04
XL_DAIO_PORT_MASK_DIGITAL_D3 = 0x08
XL_DAIO_PORT_MASK_DIGITAL_D4 = 0x10
XL_DAIO_PORT_MASK_DIGITAL_D5 = 0x20
XL_DAIO_PORT_MASK_DIGITAL_D6 = 0x40
XL_DAIO_PORT_MASK_DIGITAL_D7 = 0x80

# Type of slope
XL_DAIO_TRIGGER_TYPE_RISING=0x01
XL_DAIO_TRIGGER_TYPE_FALLING=0x02
XL_DAIO_TRIGGER_TYPE_BOTH=0x03

# Port functions Digital
XL_DAIO_PORT_DIGITAL_IN=0
XL_DAIO_PORT_DIGITAL_PUSHPULL=1
XL_DAIO_PORT_DIGITAL_OPENDRAIN=2

# Port Mask Analog
XL_DAIO_PORT_MASK_ANALOG_A0=0x01
XL_DAIO_PORT_MASK_ANALOG_A1=0x02
XL_DAIO_PORT_MASK_ANALOG_A2=0x04
XL_DAIO_PORT_MASK_ANALOG_A3=0x08

# Port functions Analoag
XL_DAIO_PORT_ANALOG_DIFF=2
XL_DAIO_PORT_ANALOG_IN=0
XL_DAIO_PORT_ANALOG_OFF=3
XL_DAIO_PORT_ANALOG_OUT=1


XL_DAIO_EVT_ID_DIGITAL = XL_DAIO_PORT_TYPE_MASK_DIGITAL
XL_DAIO_EVT_ID_ANALOG = XL_DAIO_PORT_TYPE_MASK_ANALOG

# defines for xlGetDriverConfig structures
XL_MAX_LENGTH = 31
XL_CONFIG_MAX_CHANNELS = 64



class s_xl_lin_stat_par(ctypes.Structure):
    _fields_ = [('LINMode', ctypes.c_uint),    # XL_LIN_SLAVE | XL_LIN_MASTER
                ('baudrate', ctypes.c_int),    # the baudrate will be calculated within the API. Here: e.g. 9600, 19200
                ('LINVersion', ctypes.c_uint), # define for the LIN version (actual V1.3 of V2.0)
                ('reserved', ctypes.c_uint)]   # for future use

# structure for XL_RECEIVE_MSG, XL_TRANSMIT_MSG
class s_xl_can_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ulong),
                ("flags", ctypes.c_ushort),
                ("dlc", ctypes.c_ushort),
                ("res1", XLuint64),
                ("data", ctypes.c_ubyte * MAX_MSG_LEN)]

# structure for XL_CHIP_STATE
class s_xl_chip_state(ctypes.Structure):
    _fields_ = [("busStatus", ctypes.c_ubyte),
                ("txErrorCounter", ctypes.c_ubyte),
                ("rxErrorCounter", ctypes.c_ubyte),
                ("chipStatte", ctypes.c_ubyte),
                ("flags", ctypes.c_uint)]

# LIN event structures
class s_xl_lin_crc_info(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("flags", ctypes.c_ubyte)]

class s_xl_lin_wake_up(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]

class s_xl_lin_no_ans(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte)]

class s_xl_lin_sleep(ctypes.Structure):
    _fields_ = [("flag", ctypes.c_ubyte)]

class s_xl_lin_msg(ctypes.Structure):
    _fields_ = [("id", ctypes.c_ubyte),
                ("dlc", ctypes.c_ubyte),
                ("flags", ctypes.c_ushort),
                ("data", ctypes.c_ubyte * MAX_MSG_LEN),
                ("crc", ctypes.c_ubyte)]
    
# LIN messages structure
class s_xl_lin_msg_api(ctypes.Union):
    _fields_ = [("s_xl_lin_msg", s_xl_lin_msg),
                ("s_xl_lin_no_ans", s_xl_lin_no_ans),
                ("s_xl_lin_wake_up", s_xl_lin_wake_up),
                ("s_xl_lin_sleep", s_xl_lin_sleep),
                ("s_xl_lin_crc_info", s_xl_lin_crc_info)]

class s_xl_sync_pulse(ctypes.Structure):
    _fields_ = [("pulseCode", ctypes.c_ubyte),
                ("time", XLuint64)]

# structure for XL_TRANSMIT_DAIO_DATA
XL_DAIO_DATA_GET = 0x8000
XL_DAIO_DATA_VALUE_DIGITAL = 0x0001
XL_DAIO_DATA_VALUE_ANALOG = 0x0002
XL_DAIO_DATA_PWM = 0x0010
XL_DAIO_MODE_PULSE = 0x0020  # generates pulse in values of PWM 

class s_xl_daio_data(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_ubyte),               # 2
                ("timestamp_correction", ctypes.c_uint), # 4
                ("mask_digital", ctypes.c_ubyte),        # 1
                ("value_digital", ctypes.c_ubyte),       # 1
                ("mask_analog", ctypes.c_ubyte),         # 1
                ("reserved", ctypes.c_ubyte),            # 1
                ("value_analog", ctypes.c_ubyte * 4),    # 8
                ("pwm_frequency", ctypes.c_uint),        # 4
                ("pwm_value", ctypes.c_ubyte),           # 2
                ("reserved1", ctypes.c_uint),            # 4
                ("reserved2", ctypes.c_uint)]            # 4
    
class s_xl_daio_digital_params(ctypes.Structure):
    _fields_ = [("portMask", ctypes.c_uint),
                ("valueMask", ctypes.c_uint)]
    
class s_xl_io_digital_data(ctypes.Structure):
    _fields_ = [("digitalInputData", ctypes.c_uint)]
    
class s_xl_io_analog_data(ctypes.Structure):
    _fields_ = [("measuredAnalogData0", ctypes.c_uint),
                ("measuredAnalogData1", ctypes.c_uint),
                ("measuredAnalogData2", ctypes.c_uint),
                ("measuredAnalogData3", ctypes.c_uint)]

class s_xl_io_data(ctypes.Union):
    _fields_ = [('digital', s_xl_io_digital_data),
                ('analog', s_xl_io_analog_data)]

class s_xl_daio_piggy_data(ctypes.Structure):
    _fields_ = [("daioEvtTag", ctypes.c_uint),
                ("triggerType", ctypes.c_uint),
                ("data", s_xl_io_data)]
    
class s_xl_digital(ctypes.Structure):
    _fields_ = [("portMask", ctypes.c_uint),
                ("type", ctypes.c_uint) ]
    
class u_xl_triggerTypeParams(ctypes.Union):
    _fields_ = [("cycleTime", ctypes.c_uint),
                ("digital", s_xl_digital) ]
    
class s_xl_daio_trigger_mode(ctypes.Structure):
    _fields_ = [("portTypeMask", ctypes.c_uint),
                ("triggerType", ctypes.c_uint),
                ("param", u_xl_triggerTypeParams)]

class s_xl_transceiver(ctypes.Structure):
    _fields_ = [("event_reason", ctypes.c_ubyte), # reason for what was event sent
                ("is_present", ctypes.c_ubyte)]   # allways valid transceiver presence flag

# BASIC bus message structure
class s_xl_tag_data(ctypes.Union):
    _fields_ = [("msg", s_xl_can_msg),
                ("chipState", s_xl_chip_state),
                ("linMsgApi", s_xl_lin_msg_api),
                ("syncPulse", s_xl_sync_pulse),
                ("daioData", s_xl_daio_data),
                ("transceiver", s_xl_transceiver),
                ("daioPiggyData", s_xl_daio_piggy_data)]

# XL_EVENT structures, event type definition
class s_xl_event(ctypes.Structure):
    _fields_ = [ ("tag", XLeventtag),
                ("chanIndex", ctypes.c_ubyte),
                ("transId", ctypes.c_ushort),
                ("portHandle", ctypes.c_ushort),
                ("reserved", ctypes.c_ushort),
                ("timeStamp", XLuint64),
                ("tagData", s_xl_tag_data)]

XLevent = s_xl_event

listOfLINSlaves = []

class XLbusParams_can(ctypes.Structure):
    _fields_ = [("bitRate", ctypes.c_uint),
               ("sjw", ctypes.c_ubyte),
               ("tseg1", ctypes.c_ubyte),
               ("tseg2", ctypes.c_ubyte),
               ("sam", ctypes.c_ubyte),
               ("outputMode", ctypes.c_ubyte),
               ("padding", ctypes.c_ubyte * 23)]

class XLbusParams(ctypes.Structure):
    _fields_ = [("busType", ctypes.c_uint),
               ("can", XLbusParams_can)]

# structures for get_driver_config function
class s_xl_channel_config(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("name", ctypes.c_char * (XL_MAX_LENGTH + 1)),
               ("hwType", ctypes.c_ubyte),
               ("hwIndex", ctypes.c_ubyte),
               ("hwChannel", ctypes.c_ubyte),
               ("transceiverType", ctypes.c_ushort),
               ("transceiverState", ctypes.c_uint),
               ("channelIndex", ctypes.c_ubyte),
               ("channelMask", XLuint64),
               ("channelCapabilities", ctypes.c_uint),
               ("channelBusCapabilities", ctypes.c_uint),
               ("isOnBus", ctypes.c_ubyte),
               ("connectedBusType", ctypes.c_uint),
               ("busParams", XLbusParams),
               ("driverVersion", ctypes.c_uint),
               ("interfaceVersion", ctypes.c_uint),
               ("raw_data", ctypes.c_uint * 10),
               ("serialNumber", ctypes.c_uint),
               ("articleNumber", ctypes.c_uint),
               ("transceiverName", ctypes.c_char * (XL_MAX_LENGTH + 1)),
               ("specialCabFlags", ctypes.c_uint),
               ("dominantTimeout", ctypes.c_uint),
               ("dominantRecessiveDelay", ctypes.c_ubyte),
               ("recessiveDominantDelay", ctypes.c_ubyte),
               ("connectionInfo", ctypes.c_ubyte),
               ("currentlyAvailableTimestamps", ctypes.c_ubyte),
               ("minimalSupplyVoltage", ctypes.c_ushort),
               ("maximalSupplyVoltage", ctypes.c_ushort),
               ("maximalBaudrate", ctypes.c_uint),
               ("fpgaCoreCapabilities", ctypes.c_ubyte),
               ("specialDeviceStatus", ctypes.c_ubyte),
               ("channelBusActiveCapabilities", ctypes.c_ushort),
               ("breakOffset", ctypes.c_ushort),
               ("delimiterOffset", ctypes.c_ushort),
               ("reserved", ctypes.c_uint * 3)]

class s_xl_driver_config(ctypes.Structure):
    _fields_ = [ ("dllVersion", ctypes.c_uint),
                ("channelCount", ctypes.c_uint),
                ("reserved", ctypes.c_uint * 10),
                ("channel", s_xl_channel_config * XL_CONFIG_MAX_CHANNELS)]

class XLdaioSetPort(ctypes.Structure):
    _fields_ = [("portType", ctypes.c_uint),
                ("portMask", ctypes.c_uint),
                ("portFunction", ctypes.c_uint * 8),
                ("reserved", ctypes.c_uint * 8)]

class xl_daio_digital_params (ctypes.Structure):
    _fields_ = [("portMask", ctypes.c_uint),
                ("valueMask", ctypes.c_uint)]


class vectordriver():
    def __init__(self):
        self.vectordll = ctypes.windll.LoadLibrary("vxlapi.dll")
        
    def open_driver(self):
        """
        The Application calls this function to get access to the driver. If this call is not successfully, no other API calls are possible.
        @retval Returns an error code.
        """
        ok = self.vectordll.xlOpenDriver()
        return ok
    
    
    def get_driver_config(self, pDriverConfig):
        """
        Summary:
        Allows reading out more detailed information about the used hardware. This function can be called at any time after a successfully xlOpenDriver. 
        The result describes the current state of the driver configuration after each call.
        
        Parameters:
        pDriverConfig: Reference where to store configuration.
        """
        self.vectordll.xlGetDriverConfig.argtypes = [ctypes.POINTER(s_xl_driver_config)]
        ok = self.vectordll.xlGetDriverConfig(ctypes.byref(pDriverConfig))
        return ok
    
    """
    Summary:
    Returns the p_hw_index, p_hw_channel and p_hw_type for a specific Application and application channel. This gives the ability to register own applications into the Vector CAN DRIVER CONFIGURATION (VCANCONF.EXE).
    
    Parameters:
    app_name: Application name in Vector Hardware Config.
    app_channel: Channel of application; p_hw_type, p_hw_index, p_hw_channel: contains the the hardware information on success.
    bus_type: Bus type of configuration, should be BUS_TYPE_NONE when no bus type is set. (XL_BUS_TYPE_CAN, XL_BUS_TYPE_LIN)
    """
    def get_appl_config(self, appname, channel, bustype):
        app_name = ctypes.c_char_p(appname)
        app_channel = ctypes.c_uint(channel)
        p_hw_type = ctypes.pointer(ctypes.c_uint())
        p_hw_index = ctypes.pointer(ctypes.c_uint())
        p_hw_channel = ctypes.pointer(ctypes.c_uint())
        bus_type = ctypes.c_uint(bustype)
        ok = self.vectordll.xlGetApplConfig(app_name, app_channel, p_hw_type, p_hw_index, p_hw_channel, bus_type)
        return ok, p_hw_type.contents, p_hw_index.contents, p_hw_channel.contents
    
    """
    Summary:
    Returns the channel mask.
    
    Parameters:
    hwType: The hardware type.
    hwIndex: The hardware index of same hw types.
    hwChannel: The channel index of the selected hardware.
    """
    def get_channel_mask(self, hwtype, hwindex, hwchannel):
        self.vectordll.xlGetChannelMask.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        mask = self.vectordll.xlGetChannelMask(hwtype, hwindex, hwchannel)
        return ctypes.c_ulonglong(mask)
    
    def open_port(self, port_handle, user_name, access_mask, permission_mask, rx_queue_size, interface_version, bus_type):
        """
        The application tells the driver to which channels it wants to get access to and which of these channels it wants to get the permission to initialize the channel (on input must be in variable where pPermissionMask points).
        Only one port can get the permission to initialize a channel.
        The status, port handle and permitted init access is returned.
        
        Parameters:
        @param port_handle Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
        @param user_name Name which is displayed in Vector Hardware Config for a given hardware.
        @param access_mask Mask specifying which channels shall be used with this port.
        @param permission_mask Reference to a variable where the mask is returned for the channel for which init access is granted. As the input there must be the chan-nel mask where is the init access requested. A LIN channel needs init access.
        @param rx_queue_size Size of the port receive queue allocated by the driver. Specifies how many events can be stored in the queue. The value should be a power of 2 and within a range of 16…32786. The actual queue size is rxQueueSize-1.
        @param interface_version Current API version, e.g. XL_INTERFACE_VERSION (see s_xl_channel_config).
        @param bus_type Bus type that should be activated.
        """
        self.vectordll.xlOpenPort.argtypes = [ctypes.POINTER(XLporthandle), ctypes.c_char_p, XLaccess, ctypes.POINTER(XLaccess), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlOpenPort(port_handle, user_name, access_mask, permission_mask, rx_queue_size, interface_version, bus_type)
        return ok, port_handle, permission_mask
    
    """
    Summary:
    Defines the mode of the LIN channel and the baudrate.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    linStatPar: Parameter settings like baudrate and LIN version.
    """
    def lin_set_channel_params(self, port_handle, amask, linStatPar):
        self.vectordll.xlLinSetChannelParams.argtypes = [XLporthandle, XLaccess, s_xl_lin_stat_par]
        ok = self.vectordll.xlLinSetChannelParams(port_handle, amask, linStatPar)
        return ok
    
    """
    Summary:
    The selected channels go 'on the bus'. Type of the bus is specified by busType parameter. Additional parameters can be specified by flags parameter.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    access_mask: Mask specifying which channels shall be used with this port.
    bustype: Bus type that should be activated, e.g. XL_BUS_TYPE_CAN (see XLbusParams).
    flags: Additional flags for activating the channels.
    """
    def activate_channel(self, port_handle, access_mask, bustype, flags):
        self.vectordll.xlActivateChannel.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlActivateChannel(port_handle, access_mask, bustype, flags)
        return ok
    
    """
    Summary:
    The driver is asked to retrieve burst of Events from the application's receive queue. This function is optimized for speed. event_count on start must contain size of the buffer in messages, 
    on return it sets number of really received messages (messages written to event_list buffer). Application must allocate event_list buffer big enough to hold number of messages requested by event_count parameter.
    It returns VERR_QUEUE_IS_EMPTY and event_count=0 if no event was received. The function only works for CAN, LIN, DAIO. For MOST there is a different function.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    event_count: Number of events to be read at once from the queue.
    event_list: Empty list which will be loaded at once with the number of requestet events (if available).
    """
    def receive(self, port_handle, event_count, event_list):
        self.vectordll.xlReceive.argtypes = [XLporthandle, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(XLevent)]
        ok = self.vectordll.xlReceive(port_handle, ctypes.byref(event_count), ctypes.byref(event_list))
        return ok
     
    """
    Summary:
    Returns a textual description of the given event.
    
    Parameters:
    event_list: Buffer to a XL event with content.
    """
    def get_event_string(self, event_list):
        self.vectordll.xlGetEventString.argtypes = [ctypes.POINTER(XLevent)]
        self.vectordll.xlGetEventString.restype = ctypes.c_char_p
        rec_string = self.vectordll.xlGetEventString(ctypes.byref(event_list))
        return rec_string
     
    """
    Summary:
    Returns a textual description of the given status code.
    
    Parameters:
    err: An error code.
    """
    def get_error_string(self, err):
        self.vectordll.xlGetErrorString.argtypes = [XLstatus]
        self.vectordll.xlGetErrorString.restype = ctypes.c_char_p
        err_string = self.vectordll.xlGetErrorString(err)
        return err_string
    
    """
    Summary:
    Sets application configuration. This gives the ability to register own applications into the Vector CAN DRIVER CONFIGURATION (VCANCONF.EXE).
    
    Parameters:
    appname: Application name in Vector Hardware Config.
    appchannel: Channel of application.
    hwtype: The hardware type to store.
    hwindex: The hardware index of same hw types.
    hwchannel: The channel index of the selected hardware.
    bustype: Bus type of configuration, should be BUS_TYPE_NONE when no bus type is set.
    """
    def set_appl_config(self, appname, appchannel, hwtype, hwindex, hwchannel, bustype):
        self.vectordll.xlSetApplConfig.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlSetApplConfig(appname, appchannel, hwtype, hwindex, hwchannel, bustype)
        return ok
     
    """
    Summary:
    Get the channel index for a channel of a certain hardware. Parameter -1 means "don't care".
    
    Parameters:
    hw_type: The hardware type.
    hw_index: The hardware index of same hw types.
    hw_channel: The channel index of the selected hardware.
    """   
    def get_channel_index(self, hw_type, hw_index, hw_channel):
        self.vectordll.xlGetChannelIndex.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        channel_index = self.vectordll.xlGetChannelIndex(hw_type, hw_index, hw_channel)
        return channel_index

    """
    Summary:
    The driver is closed. This is used to unload the driver, if no more application is using it. Does not close the open ports !!!
    """
    def close_driver(self):
        ok = self.vectordll.xlCloseDriver()
        return  ok

    """
    Summary:
    The selected channels go 'off the bus'.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    access_mask: Mask specifying which channels shall be used with this port.
    """
    def deactivate_channel(self, port_handle, access_mask):
        self.vectordll.xlDeactivateChannel.argtypes = [XLporthandle, XLaccess]
        ok = self.vectordll.xlDeactivateChannel(port_handle, access_mask)
        return ok

    """
    Summary:
    The port is closed, channels are deactivated.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    """
    def close_port(self, port_handle):
        self.vectordll.xlClosePort.argtypes = [XLporthandle]
        ok = self.vectordll.xlClosePort(port_handle)
        return ok

    """
    Summary:
    Sends a master LIN request to the slave(s).
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    lin_id: Contains the master request LIN ID.
    flags: For future use. At the moment set to 0.
    """
    def lin_send_request(self, port_handle, amask, lin_id, flags):
        self.vectordll.xlLinSendRequest.argtypes = [XLporthandle, XLaccess, ctypes.c_ubyte, ctypes.c_uint]
        ok = self.vectordll.xlLinSendRequest(port_handle, amask, lin_id, flags)
        return ok
    
    """
    Summary:
    Sets up a LIN slave.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    slave_id: LIN ID on which the slave transmits a response.
    slave_data: Contains the data bytes.
    slave_DLC: Defines the dlc for the LIN message.
    slave_crc: Defines the checksum (it is also possible to set a faulty checksum). If the API should calculate the checksum use the following defines: XL_LIN_CALC_CHECKSUM or XL_LIN_CALC_CHECKSUM_ENHANCED.
    """
    def lin_set_slave(self, port_handle, amask, slave_id, slave_data, slave_DLC, slave_crc):
#         self.vectordll.xlLinSetSlave.argtypes=[XLporthandle, XLaccess, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_short]
        self.vectordll.xlLinSetSlave.argtypes = [XLporthandle, XLaccess, ctypes.c_ubyte, ctypes.c_ubyte * 8, ctypes.c_ubyte, ctypes.c_ushort]
        self.vectordll.xlLinSetSlave(port_handle, amask, ctypes.c_ubyte(6), (ctypes.c_ubyte * 8)(0, 0, 0, 0, 0, 0, 0, 0), ctypes.c_ubyte(8), ctypes.c_ushort(XL_LIN_CALC_CHECKSUM))
#         ok=self.vectordll.xlLinSetSlave(port_handle, amask, slave_id, slave_data, slave_DLC, slave_crc)
#         return ok

    """
    Summary:
    Sets up a list of LIN slaves. This function is similar to lin_set_slave.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    listOfSlaves: The list contains slaves data. (slave_id, slave_data, slave_DLC, slave_crc)
    """
    def lin_set_slaves(self, port_handle, amask):
        for slave in listOfLINSlaves:
            self.vectordll.xlLinSetSlave.argtypes = [XLporthandle, XLaccess, ctypes.c_ubyte, ctypes.c_ubyte * slave[2], ctypes.c_ubyte, ctypes.c_ushort]     
            self.vectordll.xlLinSetSlave(port_handle, amask, slave[0], slave[1], ctypes.c_ubyte(slave[2]), ctypes.c_ushort(slave[3]))
       
    """
    Summary:
    Transmits a wake-up signal.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    """
    def lin_wake_up(self, port_handle, amask):
        self.vectordll.xlLinWakeUp.argtypes = [XLporthandle, XLaccess]     
        self.vectordll.xlLinWakeUp(port_handle, amask)
            
    """
    Summary:
    Setup an event to notify the application if there are messages in the ports receive queue. queueLevel specifies the number of messages that triggers the event.
    Note that the event is triggered only once, when the queueLevel is reached. An application should read all available messages by xlReceive to be sure to re enable the event. The API generates the handle by itself.
    For LIN the queueLevel is fix to one.
    
    Parameters:
    port_handle: Reference to a variable where the port_handle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    ehandle: Buffer for WIN32 event handle.
    queueLevel: Queue level that triggers this event. For LIN it is fixed to 1.
    """
    def set_notification(self, port_handle, ehandle, queueLevel):
        self.vectordll.xlSetNotification.argtypes = [XLporthandle, ctypes.POINTER(XLporthandle), ctypes.c_int]
        ok = self.vectordll.xlSetNotification(port_handle, ehandle, queueLevel)
        return ok, ehandle
    
    """
    Summary:
    The receive queue of the port will be flushed.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    """
    def flush_receive_queue(self, port_handle):
        self.vectordll.xlFlushReceiveQueue.argtypes = [XLporthandle]
        ok = self.vectordll.xlFlushReceiveQueue(port_handle)
        return ok
    
    """
    Summary:
    The function flushes the transmit queues of the selected channels.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    """
    def flush_transmit_queue(self, port_handle, amask):
        self.vectordll.xlCanFlushTransmitQueue.argtypes = [XLporthandle, XLaccess]
        ok = self.vectordll.xlCanFlushTransmitQueue(port_handle, amask)
        return ok
    
#     """
#     Summary:
#     The receive queue of the port will be flushed.
#     
#     Parameters:
#     port_handle: Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
#     """
#     def flush_receive_queue(self, port_handle):
#         self.vectordll.xlFlushReceiveQueue.argtypes = [XLporthandle]
#         ok = self.vectordll.xlFlushReceiveQueue(port_handle)
#         return ok
    
    """
    Summary:
    Resets Clock (time stamps). The clock generating timestamps for the port will be reset.
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    """
    def reset_clock(self, port_handle):
        self.vectordll.xlResetClock.argtypes = [XLporthandle]
        ok = self.vectordll.xlResetClock(port_handle)
        return ok
     
    """
    Summary:
    The timer of the port will be activated/deactivated and the rate for cyclic timer events is set. The resolution of the parameter 'timerRate' is 10us.
    The accepted values for this parameter are 100, 200, 300,... resulting in an effective timerrate of 1000us, 2000us, 3000us,...
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This han-dle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    timer: Value specifying the interval for cyclic timer events generated by a port. If 0 is passed, no cyclic timer events will be generated.
    """
    def set_timer_rate(self, port_handle, timer):
        self.vectordll.xlSetTimerRate.argtypes = [XLporthandle, ctypes.c_ulong]
        ok = self.vectordll.xlSetTimerRate(port_handle, ctypes.c_ulong(timer))
        return ok
    
    """
    Summary:
    This function is designed to send different messages to supported bus. Usually p_messages is a pointer to XLevent array. p_messages points to variable which contains information about how many messages should be transmitted to desired channels. 
    It must be less or same as message_count buffer size in messages. On return function writes number of transmitted messages (moved to device queue for transmitting).
    
    Parameters:
    port_handle: Reference to a variable where the porthandle is returned. This handle must be used for any further calls to the port. If -1 is returned, the port was neither created nor opened.
    amask: Mask specifying which channels shall be used with this port.
    message_count:
    p_messages: A single XL event to be transmitted.
    """
    def can_transmit(self, port_handle, amask, message_count, p_messages):
        self.vectordll.xlCanTransmit.argtypes = [XLporthandle, XLaccess, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p]
        ok = self.vectordll.xlCanTransmit(port_handle, amask, ctypes.byref(message_count), ctypes.byref(p_messages))
        return ok

    def xlDAIOSetPWMOutput(self, port_handle, amask, frequency, value):
        self.vectordll.xlDAIOSetPWMOutput.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetPWMOutput(port_handle, amask, frequency, value)
        return ok
    
    def xlIoSetDigitalOutput(self, port_handle, amask, s_dig_params):
        self.vectordll.xlIoSetDigitalOutput.argtypes = [XLporthandle, XLaccess, ctypes.POINTER(s_xl_daio_digital_params)]
        ok = self.vectordll.xlIoSetDigitalOutput(port_handle, amask, s_dig_params)
        return ok
    
    def xlDAIOSetAnalogOutput(self, port_handle, amask, analogLine1, analogLine2, analogLine3, analogLine4):
        self.vectordll.xlDAIOSetAnalogOutput.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetAnalogOutput(port_handle, amask, analogLine1, analogLine2, analogLine3, analogLine4)
        return ok
    
    def xlDAIORequestMeasurement(self, port_handle, amask):
        self.vectordll.xlDAIORequestMeasurement.argtypes = [XLporthandle, XLaccess]
        ok = self.vectordll.xlDAIORequestMeasurement(port_handle, amask)
        return ok
    
    def xlDAIOSetDigitalParameters(self, port_handle, amask, inputMask, outputMask):
        self.vectordll.xlDAIOSetDigitalParameters.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetDigitalParameters(port_handle, amask, inputMask, outputMask)
        return ok
    
    def xlDAIOSetAnalogParameters(self, port_handle, amask, inputMask, outputMask, highRangeMask):
        self.vectordll.xlDAIOSetAnalogParameters.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetAnalogParameters(port_handle, amask, inputMask, outputMask, highRangeMask)
        return ok
    
    def xlDAIOSetAnalogTrigger(self, port_handle, amask, triggerMask, triggerLevel, triggerEventMode):
        self.vectordll.xlDAIOSetAnalogTrigger.argtypes = [XLporthandle, XLaccess, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetAnalogTrigger(port_handle, amask, triggerMask, triggerLevel, triggerEventMode)
        return ok
    
    def xlDAIOSetMeasurementFrequency(self, port_handle, amask, measurementInterval):
        self.vectordll.xlDAIOSetMeasurementFrequency.argtypes = [XLporthandle, XLaccess, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetMeasurementFrequency(port_handle, amask, measurementInterval)
        return ok
    
    def xlDAIOSetDigitalTrigger(self, port_handle, amask, triggerMask):
        self.vectordll.xlDAIOSetDigitalTrigger.argtypes = [XLporthandle, XLaccess, ctypes.c_uint]
        ok = self.vectordll.xlDAIOSetDigitalTrigger(port_handle, amask, triggerMask)
        return ok

    def xlIoSetTriggerMode(self, port_handle, amask, s_trigger_mode):
        self.vectordll.xlIoSetTriggerMode.argtypes=[XLporthandle, XLaccess, ctypes.POINTER(s_xl_daio_trigger_mode)]
        ok=self.vectordll.xlIoSetTriggerMode(port_handle,amask,s_trigger_mode)
        return ok
    
    def xlIoSetDigOutLevel(self, port_handle, amask, do_output_level ):
        self.vectordll.xlIoSetDigOutLevel.argtypes=[XLporthandle, XLaccess,ctypes.c_uint]
        ok=self.vectordll.xlIoSetDigOutLevel(port_handle, amask, do_output_level)
        return ok

    def xlIoSetDigInThreshold(self, port_handle, amask, input_threshold ):
        self.vectordll.xlIoSetDigOutLevel.argtypes=[XLporthandle, XLaccess,ctypes.c_uint]
        ok=self.vectordll.xlIoSetDigInThreshold(port_handle, amask, input_threshold)
        return ok

    def xlIoConfigurePorts(self, port_handle, amask, portConfig):
        for i in range(8):
            portConfig.reserved[i]=0
                
        self.vectordll.xlIoConfigurePorts.argtypes = [XLporthandle, XLaccess, ctypes.POINTER(XLdaioSetPort)]
        ok = self.vectordll.xlIoConfigurePorts(port_handle, amask, portConfig)
        return ok
    
    def xlIoStartSampling(self, port_handle, amask, portTypeMask):
        self.vectordll.xlIoStartSampling.argtypes= [XLporthandle, XLaccess, ctypes.c_uint]
        ok = self.vectordll.xlIoStartSampling(port_handle, amask, portTypeMask)
        return ok
        

# analog lines
AIO0 = 0x01
AIO1 = 0x02
AIO2 = 0x04
AIO3 = 0x08
AIO_ALL = 0x0F

# digital lines
DIO0 = 0x01
DIO1 = 0x02
DIO2 = 0x04
DIO3 = 0x08
DIO4 = 0x10
DIO5 = 0x20
DIO6 = 0x40
DIO7 = 0x80
DIO_ALL = 0xFF

# combined digital lines for output mask
OUTPUT_DIO0_DIO01 = 0x03
OUTPUT_DIO2_DIO03 = 0x0C
OUTPUT_DIO4_DIO05 = 0x30
OUTPUT_DIO6_DIO07 = 0xC0

# masks for switches
SWITCH_DIO0_DIO01 = 0x01
SWITCH_DIO2_DIO03 = 0x02
SWITCH_DIO4_DIO05 = 0x04
SWITCH_DIO6_DIO07 = 0x08

XL_DAIO_DO_LEVEL_0V=0
XL_DAIO_DO_LEVEL_5V=5
XL_DAIO_DO_LEVEL_12V=12

digitalOutputMask = 0
digitalInputMask = 0
analogOutputMask = 0
analogInputMask = 0
switchMask = 0;
switchState = 0 # 0 = relay open, 1 = relay closed
frequency = 500
outputMilliVolt = 4096

class daio_api():
    # open xl driver
    def __init__(self):
        self.driver = vectordriver()
        self.driver.open_driver()
        
    def __setupPiggy__(self):
        portConfig=XLdaioSetPort()
        portConfig.portType=ctypes.c_uint(XL_DAIO_PORT_TYPE_MASK_DIGITAL)
        portConfig.portMask=ctypes.c_uint(XL_DAIO_PORT_MASK_DIGITAL_D0 | XL_DAIO_PORT_MASK_DIGITAL_D1 | 
                                          XL_DAIO_PORT_MASK_DIGITAL_D2 | XL_DAIO_PORT_MASK_DIGITAL_D3 | 
                                          XL_DAIO_PORT_MASK_DIGITAL_D4 | XL_DAIO_PORT_MASK_DIGITAL_D5 | 
                                          XL_DAIO_PORT_MASK_DIGITAL_D6 | XL_DAIO_PORT_MASK_DIGITAL_D7 )
        
        portConfig.portFunction[0]=XL_DAIO_PORT_DIGITAL_PUSHPULL
        portConfig.portFunction[1]=XL_DAIO_PORT_DIGITAL_PUSHPULL
        portConfig.portFunction[2]=XL_DAIO_PORT_DIGITAL_PUSHPULL
        portConfig.portFunction[3]=XL_DAIO_PORT_DIGITAL_PUSHPULL
        
        portConfig.portFunction[4]=XL_DAIO_PORT_DIGITAL_IN
        portConfig.portFunction[5]=XL_DAIO_PORT_DIGITAL_IN
        portConfig.portFunction[6]=XL_DAIO_PORT_DIGITAL_IN
        portConfig.portFunction[7]=XL_DAIO_PORT_DIGITAL_IN

        ok=self.driver.xlIoConfigurePorts(self.phandle, self.pmask, portConfig)
        if (ok != XL_SUCCESS):
            print "ERROR: Configure Digital Ports failed!", self.driver.get_error_string(ok)
            raise Exception("Configure Digital Ports failed!")
        
        ok=self.driver.xlIoSetDigOutLevel(self.phandle, self.pmask, XL_DAIO_DO_LEVEL_5V)
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoSetDigOutLevel failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoSetDigOutLevel failed!")
        
        ok=self.driver.xlIoSetDigInThreshold(self.phandle, self.pmask, 1000 ) # 1000mV threshold for input
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoSetDigOutLevel failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoSetDigOutLevel failed!")
        
        
        portConfig=XLdaioSetPort()
        portConfig.portType=ctypes.c_uint(XL_DAIO_PORT_TYPE_MASK_ANALOG)
        portConfig.portMask=ctypes.c_uint(XL_DAIO_PORT_MASK_ANALOG_A0 | 
                                          XL_DAIO_PORT_MASK_ANALOG_A1 | 
                                          XL_DAIO_PORT_MASK_ANALOG_A2 | 
                                          XL_DAIO_PORT_MASK_ANALOG_A3  )
        
        portConfig.portFunction[0]=XL_DAIO_PORT_ANALOG_OUT
        portConfig.portFunction[1]=XL_DAIO_PORT_ANALOG_OUT
        portConfig.portFunction[2]=XL_DAIO_PORT_ANALOG_IN
        portConfig.portFunction[3]=XL_DAIO_PORT_ANALOG_IN
        
        ok=self.driver.xlIoConfigurePorts(self.phandle, self.pmask, portConfig)
        if (ok != XL_SUCCESS):
            print "ERROR: Configure Analog Ports failed!", self.driver.get_error_string(ok)
            raise Exception("Configure Analog Ports failed!")

        
        s_trigger_mode=s_xl_daio_trigger_mode()
        s_trigger_mode.portTypeMask=ctypes.c_uint(XL_DAIO_PORT_TYPE_MASK_ANALOG ) #| XL_DAIO_PORT_TYPE_MASK_DIGITAL )
        s_trigger_mode.triggerType=ctypes.c_uint(XL_DAIO_TRIGGER_TYPE_CYCLIC)
        
        u_trg_param=u_xl_triggerTypeParams()
        u_trg_param.cylceTime=ctypes.c_uint(1000000)
        
        s_trigger_mode.param=u_trg_param
        
        ok=self.driver.xlIoSetTriggerMode(self.phandle, self.pmask, s_trigger_mode)
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoSetTriggerMode failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoSetTriggerMode failed!")
        
        s_trigger_mode=s_xl_daio_trigger_mode()
        s_trigger_mode.portTypeMask=ctypes.c_uint( XL_DAIO_PORT_TYPE_MASK_DIGITAL )
        s_trigger_mode.triggerType=ctypes.c_uint(XL_DAIO_TRIGGER_TYPE_PORT)
        
        s_dig_trg_param=s_xl_digital()
        s_dig_trg_param.portMask=  ctypes.c_uint( XL_DAIO_PORT_MASK_DIGITAL_D0 |
                                    XL_DAIO_PORT_MASK_DIGITAL_D1 |
                                    XL_DAIO_PORT_MASK_DIGITAL_D2 |
                                    XL_DAIO_PORT_MASK_DIGITAL_D3 )
        s_dig_trg_param.type=XL_DAIO_TRIGGER_TYPE_BOTH
        
        u_trg_param=u_xl_triggerTypeParams()
        u_trg_param.cylceTime=s_dig_trg_param
        
        s_trigger_mode.param=u_trg_param
        
        ok=self.driver.xlIoSetTriggerMode(self.phandle, self.pmask, s_trigger_mode)
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoSetTriggerMode failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoSetTriggerMode failed!")

        ok, self.ehandle=self.driver.set_notification ( self.phandle, XLporthandle(XL_INVALID_PORTHANDLE), 2)
        if (ok != XL_SUCCESS):
            print "ERROR: set_notification failed!", self.driver.get_error_string(ok)
            raise Exception("set_notification failed!")
        
        ok=self.driver.activate_channel(self.phandle, self.pmask, XL_BUS_TYPE_DAIO, 0)
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoSetTriggerMode failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoSetTriggerMode failed!")
        
        ok=self.driver.xlIoStartSampling(self.phandle, self.pmask, XL_DAIO_PORT_TYPE_MASK_DIGITAL | XL_DAIO_PORT_TYPE_MASK_ANALOG )
        if (ok != XL_SUCCESS):
            print "ERROR: xlIoStartSampling failed!", self.driver.get_error_string(ok)
            raise Exception("xlIoStartSampling failed!")
        
        ok=self.driver.set_timer_rate(self.phandle,5000)
        if (ok != XL_SUCCESS):
            print "ERROR: set_timer_rate failed!", self.driver.get_error_string(ok)
            raise Exception("set_timer_rate failed!")
        
        self.driver.reset_clock(self.phandle)


    
    def __setupIOCAB__(self):
        print "ERROR: __setupIOCAB__ not implemented"
        raise Exception("__setupIOCAB__ not implemented")
    
    def __setupFixPiggy__(self):
        print "ERROR: __setupFixPiggy__ not implemented"
        raise Exception("__setupFixPiggy__ not implemented")
    
        
    def get_driver_info(self):
        p = s_xl_driver_config()
        self.driver.get_driver_config(p)
        return p

    def channel_init(self, channelselector=0):
        # Application Config
        bHWFound=False
        ok, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', 0, XL_BUS_TYPE_DAIO)
        if (ok != XL_SUCCESS):
            p = self.get_driver_info()
            channelFound = 0
            for channel in range(0, p.channelCount):
                if channelFound == channelselector:
                    # search a channel which supports DAIO 
                    if (p.channel[channel].channelBusActiveCapabilities == XL_BUS_TYPE_DAIO):
#                         print p.channel[channel].channelBusActiveCapabilities
#                         print p.channel[channel].transceiverName
                        channelFound = 1
                        # create application with 1 channel in Vector Hardware Config
                        ok=self.driver.set_appl_config('PLAST', 0, p.channel[channel].hwType, p.channel[channel].hwIndex, p.channel[channel].hwChannel, XL_BUS_TYPE_DAIO)
                        if ok!=XL_SUCCESS:
                            print "ERROR xlSetApplConfig failed: ", self.driver.get_error_string(ok)
                            raise Exception("ERROR xlSetApplConfig failed ")

                        print 'PLAST application has created in Vector Hardware Config.'
                        
                        self.hwt = p.channel[channel].hwType
                        self.hwi = p.channel[channel].hwIndex
                        self.hwc = p.channel[channel].hwChannel
                        bHWFound=True
                        break
        else:
            bHWFound=True
            
        if not bHWFound:
            print "Error: HW found in Registry"
            raise Exception("Error: HW found in Registry")
        else:
            print "DAIO Driver type found:", self.hwt.value, ", HW Index ",self.hwi.value, ", HW channel ",self.hwc.value
        
        ci = self.driver.get_channel_index(self.hwt, self.hwi, self.hwc)
        if (ci > XL_CONFIG_MAX_CHANNELS):
            print "Error: xlGetChannelIndex", ci
            raise Exception("Error: xlGetChannelIndex")

        p = self.get_driver_info()        
        self.nTransceiverType= p.channel[ci].transceiverType
            
        # Get channel mask is also permission mask
        self.mask = self.driver.get_channel_mask(self.hwt.value, self.hwi.value, self.hwc.value)
        if (self.mask == 0 ):
            print "ERROR: Vector Hardware Configuration not properly set. Check your settings!"
            raise Exception("Vector Hardware Configuration not properly set")

        
        # open port for the channel
        ok, self.phandle, self.pmask = self.driver.open_port(XLporthandle(XL_INVALID_PORTHANDLE), 'PLAST', XLaccess(self.mask.value), XLaccess(self.mask.value), 1024, XL_INTERFACE_VERSION, XL_BUS_TYPE_DAIO)
        if (ok != XL_SUCCESS):
            print "ERROR: OpenPort failed!", self.driver.get_error_string(ok)
            raise Exception("OpenPort failed!")
        
        if self.nTransceiverType==XL_TRANSCEIVER_TYPE_PB_DAIO_8642:
            self.__setupPiggy__()
        elif self.nTransceiverType==XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO:
            self.__setupIOCAB__()
        elif self.nTransceiverType==XL_TRANSCEIVER_TYPE_DAIO_1021_FIX:
            self.__setupFixPiggy__()
        else:
            print "Error: Invalid transceiver", self.nTransceiverType
            raise Exception("Error: Invalid transceiver")
        
        return self.phandle, self.pmask, self.driver

    def channel_close(self):
        self.driver.deactivate_channel(self.phandle, self.mask)
        self.driver.close_port(self.phandle)
        self.driver.close_driver()

    def setDigitalOutput(self,port,data):
        if self.nTransceiverType==XL_TRANSCEIVER_TYPE_DAIO_8444_OPTO:
            print "Error: Invalid transceiver", self.nTransceiverType
            raise Exception("Error: Invalid transceiver")
        elif self.nTransceiverType==XL_TRANSCEIVER_TYPE_PB_DAIO_8642 or self.nTransceiverType==XL_TRANSCEIVER_TYPE_DAIO_1021_FIX:

            sdiao_params=s_xl_daio_digital_params()
            sdiao_params.portMask=port
            sdiao_params.valueMask=data
            
            ok=self.driver.xlIoSetDigitalOutput (self.phandle, self.pmask, sdiao_params)

        if (ok != XL_SUCCESS):
            print "ERROR: xlDAIOSetDigitalOutput failed!", self.driver.get_error_string(ok)
            raise Exception("xlDAIOSetDigitalOutput failed!")

        return ok
    
    def receive(self, evtCount=1 ):
        event_count = ctypes.c_uint(evtCount)
        event_list = XLevent()
        lstAnalogData=[]
        digData=-1

        ok=self.driver.receive (self.phandle, event_count, event_list )
        if (ok != XL_SUCCESS):
            if ok == XL_ERR_QUEUE_IS_EMPTY:
                self.driver.flush_receive_queue(self.phandle)
            else:
                print "ERROR: Receive failed!", self.driver.get_error_string(ok)
                raise Exception("Receive failed!")
        else:
            print event_list.tag
            if event_list.tag==XL_RECEIVE_DAIO_DATA:
                print "ERROR Reading IO CAB: Currently not supported"
                raise Exception("Receive failed!")
            elif event_list.tag==XL_RECEIVE_DAIO_PIGGY:
                if event_list.tagData.daioPiggyData.daioEvtTag == XL_DAIO_EVT_ID_DIGITAL:
                    digData=event_list.tagData.daioPiggyData.data.digital.digitalInputData
                    digData=digData>>4
                elif event_list.tagData.daioPiggyData.daioEvtTag == XL_DAIO_EVT_ID_ANALOG:
                    lstAnalogData.append(event_list.tagData.daioPiggyData.data.analog.measuredAnalogData0)
                    lstAnalogData.append(event_list.tagData.daioPiggyData.data.analog.measuredAnalogData1)
                    lstAnalogData.append(event_list.tagData.daioPiggyData.data.analog.measuredAnalogData2)
                    lstAnalogData.append(event_list.tagData.daioPiggyData.data.analog.measuredAnalogData3)
    
        return digData, lstAnalogData

    def multipleRead (self, nTimes=1):
        for i in range (nTimes):
            digData, lstAnalogData=self.receive()
            print digData, lstAnalogData

class Thread_Measuring_DAIO(): # only for channel 0
    loop = 0
    
    def __init__(self):
        pass
         
    def OnDAIO(self):
        global loop
        daio = daio_api()
        phndle, msk, ehndle, driverr = daio.channel_init()
        kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")

        # read hardware queue while not empty
        while loop:
            if(kernel32dll.WaitForSingleObject(ehndle, 10) != WAIT_TIMEOUT):
                xlStatus = XL_SUCCESS
                if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
                    msg, evList = daio.get_msg()
                    print msg
                    if (evList.tag == XL_RECEIVE_DAIO_DATA):
                        
                        # TODO manipulate the received message
#                         print evList.tagData.daioData.value_analog
                        pass
                                     
        daio.channel_close()
         
    def start(self):
        global loop
        loop = 1
        alive = 1
        Thread(target=self.OnDAIO, args=()).start()
          
    def stop(self):
        global loop
        loop = 0
        
    def isAlive(self):
        global loop
        return loop


class lin_api():
    def __init__(self, baud, DLC, master = False):
        # open xl driver
        self.driver = vectordriver()
        self.driver.open_driver()
        if(master):
            self.DLC = ()      
            for i in DLC:
                self.DLC = self.DLC + (i,)
            self.DLC = (ctypes.c_ubyte * len(DLC))(*self.DLC)
        self.baud = baud
        self.master = master

#         self.sList = sL
#         self.sList.extend(sL)
        
    def get_driver_info(self):
        p = s_xl_driver_config()
        self.driver.get_driver_config(p)
        return p

    def channel_init(self, channelselector=0):
        # Application Config
        ok, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', 0, XL_BUS_TYPE_LIN)
        if (ok != XL_SUCCESS):
            # get complete xl driver configuration, stored in p object
            p = self.get_driver_info()
            channelFound = 0
            for channel in range(0, p.channelCount):
                if channelFound == channelselector:
                    if (p.channel[channel].channelBusActiveCapabilities == XL_BUS_TYPE_LIN):
                        channelFound = 1
                        # create application with 1 channel in Vector Hardware Config
                        self.driver.set_appl_config('PLAST', 0, p.channel[channel].hwType, p.channel[channel].hwIndex, p.channel[channel].hwChannel, XL_BUS_TYPE_LIN)
                        print 'PLAST application was created in Vector Hardware Config.'
                        self.hwt = p.channel[channel].hwType
                        self.hwi = p.channel[channel].hwIndex
                        self.hwc = p.channel[channel].hwChannel
        # read setting of LIN
        if(not self.master):
            gac, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', 0, XL_BUS_TYPE_LIN)
        self.mask = self.driver.get_channel_mask(self.hwt.value, self.hwi.value, self.hwc.value)
        # open port for the channel
        op, self.phandle, self.pmask = self.driver.open_port(XLporthandle(XL_INVALID_PORTHANDLE), 'PLAST', XLaccess(self.mask.value), XLaccess(self.mask.value), XL_RECEIVE_EVENT_SIZE, XL_INTERFACE_VERSION, XL_BUS_TYPE_LIN)
        if not(op):
            # set channel params, slaves and activate it
            self.linStatPar = s_xl_lin_stat_par()
            self.linStatPar.baudrate = self.baud
            if(self.master):
                self.linStatPar.LINMode = XL_LIN_MASTER
            else:
                self.linStatPar.LINMode = XL_LIN_SLAVE
            self.linStatPar.LINVersion = XL_LIN_VERSION_2_0;
            self.driver.lin_set_channel_params(self.phandle, self.mask.value, self.linStatPar)             
            self.driver.lin_set_slaves(self.phandle, self.mask.value)
            if(self.master):
                self.driver.vectordll.xlLinSetDLC(self.phandle, self.mask, self.DLC)        
            ok = self.driver.activate_channel(self.phandle, self.mask.value, XL_BUS_TYPE_LIN, XL_ACTIVATE_RESET_CLOCK)
            if ok == -1:
                print 'ACTIVATING FAILED!'
            ok, self.ehandle = self.driver.set_notification(self.phandle, XLporthandle(XL_INVALID_PORTHANDLE), 1)
        return self.phandle, self.pmask


    def channel_close(self):
        self.driver.deactivate_channel(self.phandle, self.mask)
        self.driver.close_port(self.phandle)
        self.driver.close_driver()

    def get_msg(self):
        event_count = ctypes.c_uint(1)
        event_list = XLevent()
        ok = self.driver.receive(self.phandle, event_count, event_list)
        if ok:
            rec_string = self.driver.get_error_string(ok)
        else:
            rec_string = self.driver.get_event_string(event_list)
        return rec_string, event_list
        
class can_api():
    def __init__(self):
        self.driver = vectordriver()
        self.driver.open_driver()
        
    def get_driver_info(self):
        p = s_xl_driver_config()
        self.driver.get_driver_config(p)
        return p
    
    def channel_init(self, channelselector=0):
        ok, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', channelselector, XL_BUS_TYPE_CAN)
#         print ok
        if (ok == XL_SUCCESS):
            # get complete xl driver configuration, stored in p object
            p = self.get_driver_info()
            channelFound = 0
            for channel in range(0, p.channelCount):
#                 print p.channel[channel].name, p.channel[channel].channelCapabilities
                if channelFound == 0:
                    if (p.channel[channel].channelBusActiveCapabilities == XL_BUS_TYPE_CAN):
                        channelFound = 1
#                         print p.channel[channel].name
#                         create application with 1 channel in Vector Hardware Config
                        self.driver.set_appl_config('PLAST', 0, p.channel[channel].hwType, p.channel[channel].hwIndex, p.channel[channel].hwChannel, XL_BUS_TYPE_CAN)
#                         print 'PLAST application was created in Vector Hardware Config.'
                        self.hwt = p.channel[channel].hwType
                        self.hwi = p.channel[channel].hwIndex
                        self.hwc = p.channel[channel].hwChannel
                        
        # read setting of CAN
        gac, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', channelselector, XL_BUS_TYPE_CAN)
        self.mask = self.driver.get_channel_mask(self.hwt.value, self.hwi.value, self.hwc.value)
        # open port for the channel
        op, self.phandle, self.pmask = self.driver.open_port(XLporthandle(XL_INVALID_PORTHANDLE), 'PLAST', XLaccess(self.mask.value), XLaccess(self.mask.value), XL_RECEIVE_EVENT_SIZE, XL_INTERFACE_VERSION, XL_BUS_TYPE_CAN)
        
        if not(op):
            ok = self.driver.activate_channel(self.phandle, self.mask.value, XL_BUS_TYPE_CAN, XL_ACTIVATE_RESET_CLOCK)
            self.driver.flush_receive_queue(self.phandle)
            self.driver.flush_transmit_queue(self.phandle, self.mask.value)
        err_string = self.driver.get_error_string(ok)
        return err_string

    def channel_close(self):
        self.driver.deactivate_channel(self.phandle, self.mask)
        self.driver.close_port(self.phandle)
        self.driver.close_driver()

    def send_msg(self, data, ids):
        event_msg = XLevent()
        event_msg.tag = XL_TRANSMIT_MSG
        event_msg.tagData.msg.id = ids
        event_msg.tagData.msg.flags = 0
        dlc = len(data)
        for n in range(0, dlc):
            event_msg.tagData.msg.data[n] = data[n]
        event_msg.tagData.msg.dlc = dlc
        event_count = ctypes.c_uint(1)
        ok = self.driver.can_transmit(self.phandle, self.mask, event_count, event_msg)
        err_string = self.driver.get_error_string(ok)
        return err_string

    def get_msg(self):
        event_count = ctypes.c_uint(1)
        event_list = XLevent()
        ok = self.driver.receive(self.phandle, event_count, event_list)
        if ok:
            rec_string = self.driver.get_error_string(ok)
        else:
            rec_string = self.driver.get_event_string(event_list)
        return rec_string
    
    
# def CANReadMsg():
#     can = can_api()
#     can.channel_init()
#     msg = can.get_msg()
#     can.channel_close()
#     return msg
    

# RX_MSG c=1, t=503029760, id=0540 l=8, 00000000001F0240 tid=00
# class can_message_object():
#     def __init__(self, msg):
#         self.id = msg.split(',')[2].split('l')[0].split('id=')[1].strip()
#         self.length = msg.split(',')[2].split('l=')[1].strip()
#         self.data = msg.split(',')[3].split('tid')[0].strip()
#          
#     def get_id(self):
#         return self.id
#      
#     def get_data_length(self):
#         return self.length
#      
#     def get_data(self):
#         return self.data


def CAN_ReadMultipleMessages_return(channelselector, time_):
    msglist = []
    start_time = time.time()
    can = can_api()
    can.channel_init(channelselector)
    ok = 1
    while(ok):
#         time.sleep(0.01)
        msg = can.get_msg()
        if msg == 'XL_ERR_QUEUE_IS_EMPTY':
            pass
        else:
            msglist.append(msg)
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
    return msglist

def CAN_ReadMultipleMessagesAndRun_return(channelselector, time_, dbg):
    msglist = []
    start_time = time.time()
    can = can_api()
    can.channel_init(channelselector)
    dbg.run()
    ok = 1
    while(ok):
#         time.sleep(0.01)
        msg = can.get_msg()
        if msg == 'XL_ERR_QUEUE_IS_EMPTY':
            pass
        else:
            msglist.append(msg)
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
    return msglist

# 
def CAN_ReadMultipleMessages_print(channelselector, time_):  # in seconds
#     i = 0
    start_time = time.time()
    can = can_api()
    can.channel_init(channelselector)
    ok = 1
    while(ok):
#         time.sleep(0.01)
        msg = can.get_msg()
        if msg == 'XL_ERR_QUEUE_IS_EMPTY':
            pass
        else:
            print msg
#         i = i + 1
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
     
def WriteMessageOnce(id_, data_, channelselector):
    can = can_api()
    can.channel_init(channelselector)
    can.send_msg(data_, id_)
    can.channel_close()
     
def WriteMessageMultiple(time_, id_, data_, cycle_, channelselector):  # in seconds
    start_time = time.time()
    can = can_api()
    can.channel_init(channelselector)
#     print st
    ok = 1
    while(ok):
        time.sleep(cycle_)
        can.send_msg(data_, id_)
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
     
def ActivateKL15(channelselector):
    ''' Project related: BMW BDC 35up '''
    can = can_api()
    can.channel_init(channelselector)
    can.send_msg([0x40, 0x10, 0x07, 0x31, 0x01, 0x10, 0x01, 0x0A], 1787)
    ok = 1
    while ok:
        msg = can.get_msg()
        if 'id=0640' in msg:
            print msg
            can.send_msg([0x40, 0x21, 0x0A, 0x43, 0xFF, 0xFF, 0xFF, 0xFF], 1787)
            ok = 0
    ok1 = 1
    while ok1:
        msg = can.get_msg()
        if 'id=0640' in msg:
            print msg
#             can.send_msg([0x40, 0x21, 0x0A, 0x43, 0xFF, 0xFF, 0xFF, 0xFF], 1787)
            ok1 = 0
     
    can.channel_close()
     
class WriteCAN_Thread():
    loop = 0
    def __init__(self, i, d, c, channel=0):
        self.id_ = i
        self.data_ = d
        self.cycle_ = c
        self.channel_=channel
         
    def SendOnCAN(self, id__, data__, cycle__, channel__):
        print "========== Thread started!"
        can = can_api()
        can.channel_init(channel__)
        while loop:
            can.send_msg(data__, id__)
            time.sleep(cycle__)
        can.channel_close()
         
    def start(self):
        global loop
        loop = 1
        Thread(target=self.SendOnCAN, args=(self.id_, self.data_, self.cycle_, self.channel_)).start()
          
    def stop(self):
        global loop
        loop = 0
        
class WriteCAN_Thread_Variant():
    loop = 0
    def __init__(self, i, c, channel=0):
        self.id_ = i
        self.cycle_ = c
        self.data = []
        self.channel_=channel
          
    def SendOnCAN(self, id__, cycle__, channel__):
        can = can_api()
        can.channel_init(channel__)
        while loop:
            can.send_msg(self.data, id__)
            time.sleep(cycle__)
          
    def start(self):
        global loop
        loop = 1
        Thread(target=self.SendOnCAN, args=(self.id_, self.cycle_, self.channel_)).start()
           
    def stop(self):
        global loop
        loop = 0
         
    def setData(self, d):
        self.data = d    
        
        
 
'''
matrix used for CRC calculation
'''        
crc8table = [ 0x00, 0x1D, 0x3A, 0x27, 0x74, 0x69, 0x4E, 0x53, 0xE8, 0xF5, 0xD2, 0xCF, 0x9C, 0x81, 0xA6, 0xBB, 0xCD, 0xD0, 0xF7, 0xEA,
          0xB9, 0xA4, 0x83, 0x9E, 0x25, 0x38, 0x1F, 0x02, 0x51, 0x4C, 0x6B, 0x76, 0x87, 0x9A, 0xBD, 0xA0, 0xF3, 0xEE, 0xC9, 0xD4,
          0x6F, 0x72, 0x55, 0x48, 0x1B, 0x06, 0x21, 0x3C, 0x4A, 0x57, 0x70, 0x6D, 0x3E, 0x23, 0x04, 0x19, 0xA2, 0xBF, 0x98, 0x85,
          0xD6, 0xCB, 0xEC, 0xF1, 0x13, 0x0E, 0x29, 0x34, 0x67, 0x7A, 0x5D, 0x40, 0xFB, 0xE6, 0xC1, 0xDC, 0x8F, 0x92, 0xB5, 0xA8,
          0xDE, 0xC3, 0xE4, 0xF9, 0xAA, 0xB7, 0x90, 0x8D, 0x36, 0x2B, 0x0C, 0x11, 0x42, 0x5F, 0x78, 0x65, 0x94, 0x89, 0xAE, 0xB3,
          0xE0, 0xFD, 0xDA, 0xC7, 0x7C, 0x61, 0x46, 0x5B, 0x08, 0x15, 0x32, 0x2F, 0x59, 0x44, 0x63, 0x7E, 0x2D, 0x30, 0x17, 0x0A,
          0xB1, 0xAC, 0x8B, 0x96, 0xC5, 0xD8, 0xFF, 0xE2, 0x26, 0x3B, 0x1C, 0x01, 0x52, 0x4F, 0x68, 0x75, 0xCE, 0xD3, 0xF4, 0xE9,
          0xBA, 0xA7, 0x80, 0x9D, 0xEB, 0xF6, 0xD1, 0xCC, 0x9F, 0x82, 0xA5, 0xB8, 0x03, 0x1E, 0x39, 0x24, 0x77, 0x6A, 0x4D, 0x50,
          0xA1, 0xBC, 0x9B, 0x86, 0xD5, 0xC8, 0xEF, 0xF2, 0x49, 0x54, 0x73, 0x6E, 0x3D, 0x20, 0x07, 0x1A, 0x6C, 0x71, 0x56, 0x4B,
          0x18, 0x05, 0x22, 0x3F, 0x84, 0x99, 0xBE, 0xA3, 0xF0, 0xED, 0xCA, 0xD7, 0x35, 0x28, 0x0F, 0x12, 0x41, 0x5C, 0x7B, 0x66,
          0xDD, 0xC0, 0xE7, 0xFA, 0xA9, 0xB4, 0x93, 0x8E, 0xF8, 0xE5, 0xC2, 0xDF, 0x8C, 0x91, 0xB6, 0xAB, 0x10, 0x0D, 0x2A, 0x37,
          0x64, 0x79, 0x5E, 0x43, 0xB2, 0xAF, 0x88, 0x95, 0xC6, 0xDB, 0xFC, 0xE1, 0x5A, 0x47, 0x60, 0x7D, 0x2E, 0x33, 0x14, 0x09,
          0x7F, 0x62, 0x45, 0x58, 0x0B, 0x16, 0x31, 0x2C, 0x97, 0x8A, 0xAD, 0xB0, 0xE3, 0xFE, 0xD9, 0xC4 ]
 
'''
@brief Sends a message on CAN through a thread so that the testcase doesn't depend on connection time
@param 0: the ID of the message (found on CAN Bus Catalogue)
@param 1: application data id for the CRC calculation
@param 2: alive threshold - in TSC_LCE_1167 when the alive reach 14 it resets to 0
@param 3: data to send beginning from byte 3 (because first byte is used for crc and second byte is used for alive - both on them are software calculated)
@param 4: cyclic time
'''
class WriteCAN__CRC_Alive_Thread():
    loop = 0
    def __init__(self, i, adi, a, d, c, channel=0):
        self.application_data_id_ = adi
        self.alive_ = a
        self.id_ = i
        self.data_ = d
#         self.port_ = CAN_PORT
        self.cycle_ = c
        self.channel_=channel
         
    def SendOnCAN(self, id__, application_data_id__, alive__, data__, cycle__, channel__):
        can = can_api()
        can.channel_init(channel__)
        crc = 0
        d2 = 0
        dataList = []
        crcList = []
        while loop:
            if d2 == alive__:
                d2 = 0
            else:
                d2 = d2 + 1
            crcList = [application_data_id__, 0x0, d2]
            crcList.extend(data__)
            for i in range(0, len(crcList)):
                crc = crc8table[crc ^ crcList[i]]
            dataList = [crc, d2]
            dataList.extend(data__)
                 
            can.send_msg(dataList, id__)
            time.sleep(cycle__)
            dataList = []
            crc = 0
         
    def start(self):
        global loop
        loop = 1
        Thread(target=self.SendOnCAN, args=(self.id_, self.application_data_id_, self.alive_, self.data_, self.cycle_, self.channel_)).start()
          
    def stop(self):
        global loop
        loop = 0        
        
def CAN_CRC_Check(time_, can_id, app_id): # only for channel 0
    datalist = []
    crclist = [app_id, 0x0]
    resultlist = []
    start_time = time.time()
    can = can_api()
    can.channel_init()
    ok = 1
    crc = 0
    while(ok):
        msg = can.get_msg()
        if msg == 'XL_ERR_QUEUE_IS_EMPTY':
            pass
        else:
            if str(hex(can_id)[2:]).upper() in msg:
                print msg
                
                data = msg.split(',')[-1].split('tid')[0].strip()
                l = (len(data))
                crcreaded = int(str(data)[0:2], 16)
#                 print hex(crcreaded)
                for i in range(2, l, 2):
                    datalist.append(int(str(data)[i:i+2], 16))
#                 print datalist
                crclist.extend(datalist)
#                 print crclist
                for j in range(0, len(crclist)):
                    crc = crc8table[crc ^ crclist[j]]
#                 print hex(crc)
                
                if crcreaded == crc:
                    resultlist.append(1)
                else:
                    resultlist.append(0)
                
                datalist = []
                crclist=[app_id, 0x0]
                crc = 0
                
#                 print 'crc', str(data)[0:2]
#                 print 'alive', str(data)[2:4]
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
    return resultlist
        
'''
@brief Connect to LIN with a list of slaves through a thread so that the testcase doesn't depend on connection time. 
       The thread calculate CRC and increment the alive counter - if needed
@brief This thread should be called with a list of slaves. Few rules are required in initializing the slaves.

-------------------------------------------------------------------------------------------------------------------------------------------------

Example of simulation for LIN K-LIN8 channel:

slaveList = [
                [3, (ctypes.c_ubyte * 8)(0, 1, 2, 3, 4, 5, 6, 7), 8, XL_LIN_CALC_CHECKSUM_ENHANCED,    0,  0,    0, 0, 0], # ST_FAS_LIN
                [6, (ctypes.c_ubyte * 8)(0, 1, 2, 3, 4, 5, 6, 7), 8, XL_LIN_CALC_CHECKSUM_ENHANCED, 0xF9, 14, 0x04, 0, 2], # ST_LP_SW_2_LIN
                [1, (ctypes.c_ubyte * 2)(0, 1),                   2, XL_LIN_CALC_CHECKSUM_ENHANCED,    0,  0,    0, 0, 0], # ERR_ST_FAS_LIN
                [7, (ctypes.c_ubyte * 4)(0, 1, 2, 3),             4, XL_LIN_CALC_CHECKSUM_ENHANCED,    0,  0,    0, 0, 0], # ST_SWCL_AUDCU_LIN
                [0, (ctypes.c_ubyte * 2)(0, 1),                   2, XL_LIN_CALC_CHECKSUM_ENHANCED,    0,  0,    0, 0, 0]  # ERR_ST_LP_SW_LIN
            ]
            
After the list is initialized, the thread is called with the list as parameter:

thrd = SimulateSlavesLIN__CRC_Alive_Thread(slaveList)
thrd.start()

.. code ..

thrd.stop() # the thread is no more needed

-------------------------------------------------------------------------------------------------------------------------------------------------

@param 0: Slave ID.
@param 1: Simulated data bytes for the slave. No worries about CRC and ALIVE signals yet.
@param 2: Slave DLC. (The number of bytes composing the data)
@param 3: XL_LIN_CALC_CHECKSUM or XL_LIN_CALC_CHECKSUM_ENHANCED (default should be XL_LIN_CALC_CHECKSUM_ENHANCED)
@param 4: Application-Data-ID for the CRC calculation - this is founded in the Bus Catalogue at the CRC signal properties
          This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
          If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
@param 5: The limit on which the ALIVE signal increment before it resets - this is founded in the Bus Catalogue at the ALIVE signal properties
          This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
          If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
@param 6: Usually the ALIVE value is 4-bit long. 
          This parameter represent how much to shift inside one byte in order to 
              find the beggining of ALIVE value - this is founded in the Bus Catalogue at the ALIVE signal properties -> Signaltyp
          This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
          If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
@param 7: Byte number who contain the CRC signal. (in which byte the signal is found)
@param 8: Byte number who contain the ALIVE signal. (in which byte the signal is found)

'''


# class SimulateSlavesLIN__CRC_Alive_Thread():
#     loop = 0
#     def __init__(self, sList):
#         global listOfLINSlaves
#         listOfLINSlaves = sList
#          
#     def OnLIN(self):
#         global listOfLINSlaves
#         lin = lin_api()
#         phndle, msk = lin.channel_init()
#         kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")
#         
#         # initialization of alive counters based on how many slaves are simulated
#         aliveList = []
#         for i in range(0, len(listOfLINSlaves)):
#             aliveList.append(0)
#             
#         # initialization of alive counters based on how many slaves are simulated
#         crcList = []
#         for i in range(0, len(listOfLINSlaves)):
#             crcList.append(0)
#             
#         while loop:
#             if(kernel32dll.WaitForSingleObject(lin.ehandle, 1000) != WAIT_TIMEOUT):
#                 xlStatus = XL_SUCCESS
#                 if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
#                     msg, evList = lin.get_msg()
#                     dataList = []
#                     if (evList.tag == XL_LIN_MSG):
#                         dire = 'RX'
#                         if ((evList.tagData.linMsgApi.s_xl_lin_msg.flags & XL_LIN_MSGFLAG_TX) == XL_LIN_MSGFLAG_TX):
#                             dire = 'TX'
#                         for dataByte in range(0, evList.tagData.linMsgApi.s_xl_lin_msg.dlc):
#                             dataList.append(hex(evList.tagData.linMsgApi.s_xl_lin_msg.data[dataByte]))
#                         print msg, 'XL_LIN_MSG,', dire, ' id: ', \
#                             evList.tagData.linMsgApi.s_xl_lin_msg.id, ', dlc: ', \
#                             evList.tagData.linMsgApi.s_xl_lin_msg.dlc, ', crc: ', \
#                             evList.tagData.linMsgApi.s_xl_lin_msg.crc, ', data: ', dataList
# 
#                         if dire == 'TX':
#                             # CRC and ALIVE check/creation
#                             crcList = []
#                             calculatedCRC = 0
#                             for slaveIndex in range(0, len(listOfLINSlaves)):
#                                 if (evList.tagData.linMsgApi.s_xl_lin_msg.id == listOfLINSlaves[slaveIndex][0]):
#                                     if (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID] != 0) and (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD] != 0): # application-id-data and alive threshold
#                                         if aliveList[slaveIndex] == listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD]:
#                                             aliveList[slaveIndex] = 0
#                                         else:
#                                             aliveList[slaveIndex] = aliveList[slaveIndex] + 1
#                                             
#                                         listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_BYTE_POSITION]] = (aliveList[slaveIndex] << listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_SHIFT_VALUE])
#                                         crcList = [listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID], 0]
#                                         crcList.extend(listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][1:])
#                                         for i in range(0, len(crcList)):
#                                             calculatedCRC = crc8table[calculatedCRC ^ crcList[i]]
#                                         listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_CRC_BYTE_POSITION]] = calculatedCRC 
#                                         lin.driver.lin_set_slaves(phndle, msk)
#                     else:
#                         if (evList.tag == XL_LIN_ERRMSG):
#                             print 'XL_LIN_ERRMSG'
#                         else:
#                             if (evList.tag == XL_LIN_SYNCERR):
#                                 print 'XL_LIN_SYNCERR'
#                             else:
#                                 if (evList.tag == XL_LIN_NOANS):
#                                     print 'XL_LIN_NOANS'
#                                 else:
#                                     if (evList.tag == XL_LIN_WAKEUP):
#                                         print 'XL_LIN_WAKEUP'
#                                     else:
#                                         if (evList.tag == XL_LIN_SLEEP):
#                                             print 'XL_LIN_SLEEP'
#                                         else:
#                                             if (evList.tag == XL_LIN_CRCINFO):
#                                                 print 'XL_LIN_CRCINFO'
#                      
#         lin.channel_close()
#          
#     def start(self):
#         global loop
#         loop = 1
# #         for sl in self.slaveList_:
# #             print sl
#         Thread(target=self.OnLIN, args=()).start()
#           
#     def stop(self):
#         global loop
#         loop = 0


class SimulateSlavesLIN__CRC_Alive_Thread():
    loop = 0
    
    def __init__(self, sList, baud):
        global listOfLINSlaves
        listOfLINSlaves = sList
        self.baud = baud
         
    def OnLIN(self):
        global listOfLINSlaves
        lin = lin_api(self.baud, 0, False)
        phndle, msk = lin.channel_init()
        kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")
        
        # initialization of alive counters based on how many slaves are simulated
        aliveList = []
        for i in range(0, len(listOfLINSlaves)):
            aliveList.append(0)
            
        # initialization of alive counters based on how many slaves are simulated
        crcList = []
        for i in range(0, len(listOfLINSlaves)):
            crcList.append(0)
            
        while loop:

            xlStatus = XL_SUCCESS
            if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
                msg, evList = lin.get_msg()
                dataList = []
                if (evList.tag == XL_LIN_MSG):
                    dire = 'RX'
                    if ((evList.tagData.linMsgApi.s_xl_lin_msg.flags & XL_LIN_MSGFLAG_TX) == XL_LIN_MSGFLAG_TX):
                        dire = 'TX'
                    for dataByte in range(0, evList.tagData.linMsgApi.s_xl_lin_msg.dlc):
                        dataList.append(hex(evList.tagData.linMsgApi.s_xl_lin_msg.data[dataByte]))
                        
                    print msg, 'XL_LIN_MSG,', dire, ' id: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.id, ', dlc: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.dlc, ', crc: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.crc, ', data: ', dataList, dire
                    if dire == 'TX':
                        # CRC and ALIVE check/creation
                        crcList = []
                        calculatedCRC = 0
                        for slaveIndex in range(0, len(listOfLINSlaves)):
                            if (evList.tagData.linMsgApi.s_xl_lin_msg.id == listOfLINSlaves[slaveIndex][0]):
                                if (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID] != 0) and (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD] != 0):  # application-id-data and alive threshold
                                    if aliveList[slaveIndex] == listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD]:
                                        aliveList[slaveIndex] = 0
                                    else:
                                        aliveList[slaveIndex] = aliveList[slaveIndex] + 1                                      

                                    listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_BYTE_POSITION]] = (aliveList[slaveIndex] << listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_SHIFT_VALUE])
                                    crcList = [listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID], 0]
                                    crcList.extend(listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][1:])
                                    for i in range(0, len(crcList)):
                                        calculatedCRC = crc8table[calculatedCRC ^ crcList[i]]
                                    listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_CRC_BYTE_POSITION]] = calculatedCRC 
                                    lin.driver.lin_set_slaves(phndle, msk)
                else:
                    if (evList.tag == XL_LIN_ERRMSG):
                        print 'XL_LIN_ERRMSG'
                    else:
                        if (evList.tag == XL_LIN_SYNCERR):
                            print 'XL_LIN_SYNCERR'
                        else:
                            if (evList.tag == XL_LIN_NOANS):
                                print 'XL_LIN_NOANS'
                            else:
                                if (evList.tag == XL_LIN_WAKEUP):
                                    print 'XL_LIN_WAKEUP'
                                else:
                                    if (evList.tag == XL_LIN_SLEEP):
                                        lin.driver.lin_wake_up(phndle, msk)
                                        print 'XL_LIN_SLEEP'
                                    else:
                                        if (evList.tag == XL_LIN_CRCINFO):
                                            print 'XL_LIN_CRCINFO'
                     
        lin.channel_close()
         
    def start(self):
        global loop
        loop = 1
        alive = 1

        Thread(target=self.OnLIN, args=()).start()
          
    def stop(self):
        global loop
        loop = 0
        
    def setData(self, data):
        '''
            Sets the data to be used in the simulation while the thread is running
            
            data = a list containing the informations to be send on LIN. This list can be created with 
            AddFrame() / RemoveFrame() function from LINNode class
        '''
        listOfLINSlaves = data[ : ] 

class LINClass_Master_Thread():

    loop = 0    

    def __init__(self, sList, sTable, baud):
        global loop
        global listOfLINSlaves
        global table
        loop = 0
        listOfLINSlaves = sList
        # the schedule table
        table = sTable
        #the baudrate
        self.baud = baud
          
    def OnLIN(self):
        global listOfLINSlaves
        DLC = []
        for slave in listOfLINSlaves:
            DLC.append(slave[2])
        lin = lin_api(self.baud, DLC, True)

        phndle, msk = lin.channel_init()
        kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")
        
        # initialization of alive counters based on how many slaves are simulated
        aliveList = []
        for i in range(0, len(listOfLINSlaves)):
            aliveList.append(0)
 
        # initialization of alive counters based on how many slaves are simulated
        crcList = []
        for i in range(0, len(listOfLINSlaves)):
            crcList.append(0)
            
        while loop:
            for i in range(len(table)):
                if (loop):
                    time.sleep((float(table.delay[i]) / 1000))
                if (loop):
                    lin.driver.lin_send_request(phndle, msk, table.frames[i].frameID , 0)
            
            
            xlStatus = XL_SUCCESS
            if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
                msg, evList = lin.get_msg()
                dataList = []  
                if (evList.tag == XL_LIN_MSG):               
                    lin.driver.lin_set_slaves(phndle, msk)
                    dire = 'RX'
                    
                    for dataByte in range(0, evList.tagData.linMsgApi.s_xl_lin_msg.dlc):
                        dataList.append(hex(evList.tagData.linMsgApi.s_xl_lin_msg.data[dataByte]))
                        
                    if ((evList.tagData.linMsgApi.s_xl_lin_msg.flags & XL_LIN_MSGFLAG_TX) == XL_LIN_MSGFLAG_TX):
                          dire = 'TX'                         
                          
                    print msg, 'XL_LIN_MSG,', dire, ' id: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.id, ', dlc: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.dlc, ', crc: ', \
                        evList.tagData.linMsgApi.s_xl_lin_msg.crc, ', data: ', dataList, dire
                    if(dire == "TX"):

                        # CRC and ALIVE check/creation
                        crcList = []
                        calculatedCRC = 0
                        for slaveIndex in range(0, len(listOfLINSlaves)):
                            if (evList.tagData.linMsgApi.s_xl_lin_msg.id == listOfLINSlaves[slaveIndex][0]):
                                if (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID] != 0) and (listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD] != 0):  # application-id-data and alive threshold
                                    if aliveList[slaveIndex] == listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_THRESHOLD]:
                                        aliveList[slaveIndex] = 0
                                    else:
                                        aliveList[slaveIndex] = aliveList[slaveIndex] + 1                                      
                                    listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_BYTE_POSITION]] = (aliveList[slaveIndex] << listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_ALIVE_SHIFT_VALUE])
                                    crcList = [listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_APPLICATION_ID], 0]
                                    crcList.extend(listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][1:])
                                    for i in range(0, len(crcList)):
                                        calculatedCRC = crc8table[calculatedCRC ^ crcList[i]]
                                    listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_DATA][listOfLINSlaves[slaveIndex][SIMULATED_SLAVE_CRC_BYTE_POSITION]] = calculatedCRC 
                                    lin.driver.lin_set_slaves(phndle, msk)
                    # print dataList
                else:
                    if (evList.tag == XL_LIN_ERRMSG):
                        print 'XL_LIN_ERRMSG', msg

                    else:
                        if (evList.tag == XL_LIN_SYNCERR):
                            print 'XL_LIN_SYNCERR'
                        else:
                            if (evList.tag == XL_LIN_NOANS):
                                print 'XL_LIN_NOANS'
                            else:
                                if (evList.tag == XL_LIN_WAKEUP):
                                    print 'XL_LIN_WAKEUP'
                                else:
                                    if (evList.tag == XL_LIN_SLEEP):
                                        print 'XL_LIN_SLEEP' 
                                        lin.driver.lin_wake_up(phndle, msk)                                                                          

                                    else:
                                        if (evList.tag == XL_LIN_CRCINFO):
                                            print 'XL_LIN_CRCINFO'  

    def start(self):
        global loop
        loop = 1
        alive = 1
        Thread(target=self.OnLIN, args=()).start()
          
    def stop(self):
        global loop
        loop = 0
        
    def isAlive(self):
        global loop
        return loop
    
    def setData(self, data):
        '''
            Sets the data to be used in the simulation while the thread is running
            
            data = a list containing the informations to be send on LIN. This list can be created with 
            AddFrame() / RemoveFrame() function from LINNode class
        '''
        listOfLINSlaves = data[ : ]    
                 
def CAN_Alive_Check(time_, can_id, aliveLimit):
    datalist = []
    resultlist = []
    start_time = time.time()
    can = can_api()
    can.channel_init()
    ok = 1
    alivePrev = 0
    firstRead = 1
    while(ok):
        msg = can.get_msg()
        if msg == 'XL_ERR_QUEUE_IS_EMPTY':
            pass
        else:
            if str(hex(can_id)[2:]).upper() in msg:
                data = msg.split(',')[-1].split('tid')[0].strip()
                alive = int(str(data)[3], 16)
                if firstRead == 1:
                    firstRead = 0
                    alivePrev = alive
                else:
                    if (alive <= aliveLimit):
                        if (alive == (alivePrev + 1)):
                            resultlist.append(1)
                        else:
                            if ((alivePrev - alive) == aliveLimit):
                                resultlist.append(1)
                            else:
                                resultlist.append(0)
                    else:
                        resultlist.append(0)
                    alivePrev = alive
        if (time.time() - start_time) >= time_:
            ok = 0
        else:
            ok = 1
    can.channel_close()
    return resultlist
        
class id_LIN_sleep_then_wakeup():
    loop = 0
    def __init__(self, sList):
        global listOfLINSlaves
        listOfLINSlaves = sList
         
    def OnLIN(self):
        global listOfLINSlaves
        global loop
        lin = lin_api()
        phndle, msk = lin.channel_init()
        kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")
            
        while loop:
#             print lin.ehandle.value
            if(kernel32dll.WaitForSingleObject(lin.ehandle, 1000) != WAIT_TIMEOUT):
                xlStatus = XL_SUCCESS
                if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
                    msg, evList = lin.get_msg()
                    if (evList.tag == XL_LIN_MSG):
#                         print 'XL_LIN_MSG'
                        pass
                    else:
                        if (evList.tag == XL_LIN_ERRMSG):
                            print 'XL_LIN_ERRMSG'
#                             pass
                        else:
                            if (evList.tag == XL_LIN_SYNCERR):
                                print 'XL_LIN_SYNCERR'
#                                 pass
                            else:
                                if (evList.tag == XL_LIN_NOANS):
                                    print 'XL_LIN_NOANS'
#                                     pass
                                else:
                                    if (evList.tag == XL_LIN_WAKEUP):
                                        print 'XL_LIN_WAKEUP'
#                                         loop = 0
                                    else:
                                        if (evList.tag == XL_LIN_SLEEP):
                                            print 'XL_LIN_SLEEP'
                                            lin.driver.lin_wake_up(phndle, msk)
                                            lin.driver.lin_wake_up(phndle, msk)
#                                             loop = 0
                                        else:
                                            if (evList.tag == XL_LIN_CRCINFO):
                                                print 'XL_LIN_CRCINFO'
#                                                 pass
                     
        lin.channel_close()
         
    def start(self):
        global loop
        loop = 1
        alive = 1
        Thread(target=self.OnLIN, args=()).start()
          
    def stop(self):
        global loop
        loop = 0
        
class CANMessage(Message):

    auxData = ""  # Auxiliary string used for converting the message data field from HEX to binary and for breaking data field into bytes
    nrBytes = 0  # Auxiliary number used for calculating the number of bytes from a field
    sgnData = ""  # Auxiliary string used for binary value of a signal
    global thrd  # The thread on which the message will be send
    byteList = []  # The list of bytes to be send on CAN
           
    def __init__(self, dbcParser, msgName):
        '''
            Identifies the message with 'msgName' and initializes
            the corresponding data fields 
  
            dbcParser = the parser used to read the DBC file.
            msgName = the name of the message
        '''                       
        self.genMsgCycleTime = []
        self.signals = []
        self.genMsgSendType = []
        self.genMsgStartDelayTime = []
        self.genMsgDelayTime = []
        
        # Identify the message with the 'msgName' and copy its data from the messages list
        for m in dbcParser.arrMessages:      
            if (m.name == msgName):
                self.name = msgName
                self.id = m.id   
                self.transmyter = m.transmyter
                self.dlc = m.dlc
                self.lomgName = m.longName
                self.diagResponse = m.diagResponse
                self.diagRequest = m.diagRequest
                self.data = m.data
                for sgn in m.signals:
                    self.signals.append(sgn)             
                for str in m.genMsgCycleTime:
                    self.genMsgCycleTime.append(str)
                for str in m.genMsgSendType:
                    self.genMsgSendType.append(str)
                for str in m.genMsgStartDelayTime:
                    self.genMsgStartDelayTime.append(str)
                for str in m.genMsgDelayTime:
                    self.genMsgDelayTime.append(str)
                return
            
        print "No message found with the name %s" % msgName
    
    def SetSignalValue(self, signalName, value):
        '''
            Sets the value of the signal 'signalName' to 'value'
            Returns the updated value of the message data
            
            signalName = the name of the signal whose value we want to change
            value = the new value of the signal. This shoul be a hexadecimal value
        '''
        try:
            for sgn in self.signals:  # search the signal with the signalName
                if(sgn.name == signalName):  # if signal is found
                    if(self.data.startswith("0x")):  # if value starts with 0x in hex, remove the 0x prefix
                        self.data = self.data[2 : ]
                    
                    auxData = bin(int("1" + self.data, 16)) [3 :]  # convert data to binary. 1 upfront is for keeping the leading zeros
                    auxData = auxData.zfill(self.dlc * 8)
            
                    if(value.startswith("0x")):  # if the value starts with 0x remove the prefix
                        nrBytes = (len(value) - 1) / 2  # calculate the number of bytes of the value
                    else:
                        nrBytes = (len(value) + 1) / 2
                        
                    sgnData = self.GetSignalValue(signalName)[2 : ]  # extract the corresponding bits from message data
                    sgnData = bin(int(sgnData, 16))[2 : ].zfill(sgn.length)  # convert the extracted data from hexadecimal to binary
                    val = (bin(int(value, 16))[2 : ]).zfill(sgn.length)  # convert the given value to binary
                     
                    for iIndex in range(len(val)):  # foreach bit of the value           
                        if val[iIndex] != sgnData[iIndex]:  # if the value bit is different of the corresponding data bit
                            sgnData = toggleBit(sgnData, iIndex)  # switch value of corresponding data bit
            
                    self.data = auxData[ : sgn.startbit] + sgnData + auxData[sgn.startbit + sgn.length : ]  # replace the signal value from the message data with the modified bit set
                    self.data = hex(int('1' + self.data, 2))  # convert the result back to hex.1 is for keepng the leading zeros.
                    if(self.data.endswith("L")):
                        self.data = self.data [3 :-1]  # -1 removes the L suffix(tested only on large numbers) and the 0x preffix and the added 1
                    else:
                        self.data = self.data [3 : ]
    
                    if not (self.data.startswith("0x")):  # add the 0x prefix if it's necesary
                        self.data = "0x" + self.data
                        
                    return self.data
                
            print "No signal found with the name %s" % signalName
    
        except:            
            print "Unexpected error:", sys.exc_info()[1]
            print "Possibe error reason: the given value exceedes the signal length"
             
            if not (self.data.startswith("0x")):  # add the 0x prefix if it's necesary
                self.data = "0x" + self.data 
            return self.data
    
    def GetSignalValue(self, signalName):
        '''
        Returns the value of the signal
        
        signalName = the name of the signal whose value we want to return
        '''
        try:
            for sgn in self.signals:  # search the signal with the signalName
                if(sgn.name == signalName):  # if signal is found
                    if(self.data.startswith("0x")):  # if value starts with 0x in hex, remove the 0x prefix
                        self.data = self.data[2 : ]
                        
                    auxData = bin(int("1" + self.data, 16)) [3 : ]  # convert data to binary. 1 upfront is for keeping the leading zeros
                    auxData = auxData.zfill(self.dlc * 8)  # add the leading zeros
                    
                    return hex(int(auxData[sgn.startbit : sgn.startbit + sgn.length], 2))  # .zfill(sgn.length / 4)
        except:
            print "Unexpected error:", sys.exc_info()[1] 
            return "error"
    
    def CreateThread(self):
        '''
            Creates and returns a new thread on which the messages will be sent
        '''
        return 
        
    def StartSending(self):
        '''
            Starts sending the message on the thrd thread
        '''
        try:
            auxData = self.data
            if(auxData.startswith("0x") == True):
                auxData = self.data[2 :]  # remove the 0x preffix
            for iIndex in range(self.dlc * 2):  # foreach character of datafield
                if(iIndex % 2 == 0):
                    self.byteList.append(int(auxData[iIndex : iIndex + 2], 16))  # break the datafield in bytes to be send on CAN
            
            self.thrd = WriteCAN_Thread(self.id, self.byteList, float(self.genMsgCycleTime[4]))
            self.thrd.daemon = True 
            self.thrd.start()
        
        except:
            print "Unexpected error:", sys.exc_info()[1] 
            return 0
        
    def StopSending(self):
        '''
            Stops sending the message
        '''
        try:
            self.thrd.stop();
        except:
            print "Unexpected error:", sys.exc_info()[1] 

class LINNode():
    
    messageList = []      # a list containing the data on the message that will be sent over LIN
    frameList = []        # a list containg only the frame objects that will be sent over LIN
    scheduleTable = None  # the schedule table associated with the LINMaster
    global thrd           # The thread on which the message will be send
    
    def __init__(self, ldfParser, tableName = ""):
        '''
            Creates a new LINMaster object
            
            ldfParser = the parser object used to read and parse the *.ldf file
            tableName = the schedule table name used by the LINMaster
        '''
        self.ldfParser = ldfParser;
        if(tableName == ""):
            self.master = False
        else:
            self.master = True  
            self.scheduleTable = self.SetScheduleTable(tableName)
    
    def AddFrame(self, frame, enhancedChecksum, appID=0, aliveLimit=0, aliveshift=0, CRCByteNo=0, ALIVEByteNo=0):
        '''
        Adds an item to an existing slave list and returns the list
        
        frame = the LINFrame object to be added to the slave
        arrFrames = the frames list that the frame will be added to
        enhancedChecksum: the XL_LIN_CALC_CHECKSUM_ENHANCED will be used if TRUE; the XL_LIN_CALC_CHECKSUM value will be used if enhancedChecksum is FALSE
        appID = application-Data-ID for the CRC calculation - this is founded in the Bus Catalogue at the CRC signal properties
                This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
                If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
        aliveLimit = the limit on which the ALIVE signal increment before it resets - this is founded in the Bus Catalogue at the ALIVE signal properties
                     This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
                     If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
        aliveshift = usually the ALIVE value is 4-bit long. 
                     This parameter represent how much to shift inside one byte in order to 
                     find the beggining of ALIVE value - this is founded in the Bus Catalogue at the ALIVE signal properties -> Signaltyp
                     This parameter apply only to those LIN messages who have CRC and ALIVE signals. 
                     If the LIN message does not have CRC and ALIVE signal, the parameter must be left 0.
        CRCByteNo = Byte number who contain the CRC signal. (in which byte the signal is found)
        ALIVEByteNo = Byte number who contain the ALIVE signal. (in which byte the signal is found)
        '''
        
        item = []  # the item that will be added in the frames list
        # add the frame id
        item.append(frame.frameID)
        # prepare the string with sizes and the default values
        list = ()  
        if(frame.data.startswith("0x")):  # if value starts with 0x in hex, remove the 0x prefix
            frame.data = frame.data[2 :]    
        for i in range(frame.size - 1):
            list = list + (int(frame.data[2 * i : 2 * i + 2] , 16),)
        list = (ctypes.c_ubyte * int(frame.size))(*list)
        item.append(list)
        
        # add the DLC
        item.append(frame.size)
        
        # set the XL_LIN_CALC_CHECKSUM
        if(enhancedChecksum == True):
            item.append(XL_LIN_CALC_CHECKSUM_ENHANCED)
        else:
            item.append(XL_LIN_CALC_CHECKSUM)
        
        # set the rest of the parmeters
        item.append(appID)
        item.append(aliveLimit)
        item.append(aliveshift)
        item.append(CRCByteNo)
        item.append(ALIVEByteNo)
        
        # add the item to the list
        self.messageList.append(item)
        self.frameList.append(frame)
        # return the list
        return self.messageList
            
    def RemoveFrame(self, frame):
        '''
        Removes a frame from the slave list and returns the list
        
        frame = the frame we want to remove
        '''
        # foreach item in the slave list
        for i in range(len(self.messageList)):
            # if the frame name is readed from the LDF file, get the corresponding id
            if(frame.frameID == self.messageList[i][0]):
                # remove the item from the list
                self.messageList.pop(i)
                self.frameList.pop(i)
                # return the list after the item was removed
                return self.messageList

    def GetFrames(self):
        '''
            Returns the list of frames associated with the LIN Master
        '''
        return self.frameList[ : ]
    
    def StartSending(self):
        '''
            Starts sending a message on the given thread
        '''
        try:
            if(self.master):
                # create master thread
                self.thrd = LINClass_Master_Thread(self.messageList, self.scheduleTable, self.ldfParser.GetParams())
            else:
                # create slave thread
                self.thrd = SimulateSlavesLIN__CRC_Alive_Thread(self.messageList, self.ldfParser.GetParams())
            # ensure that the thread will not keep the application awake
            self.thrd.daemon = True
            self.thrd.start()        
        except:
            print "Unexpected error:", sys.exc_info()[1]
        
    def StopSending(self):
        '''
            Stops the thread on which the message is sent
        '''
        try:
            self.thrd.stop();
        except:
            print "Unexpected error:", sys.exc_info()[1]
    
    def SetScheduleTable(self, tableName):
        '''
            Seraches the schedule table with the name 'tableName' in the table from the *.ldf file and, if found, return it
            
            tableName =  the name of the schedule table which is to be assigned to the LINMaster
        '''
        # schedule table apply just to master nodes
        if(self.master == True):
            # foreach table from the LDF file
            for table in self.ldfParser.arrScheduleTables:
                # if the table is the one the user wanted return the table object
                if(tableName == table.name):
                    return table 
            return "error"           
        else:
            print "Slave nodes do not support schedule tables"
            return "error"    

class LINFrame(Frame):
    
    auxData = ""   # Auxiliary string used for converting the message data field from HEX to binary and for breaking data field into bytes
    nrBytes = 0    # Auxiliary number used for calculating the number of bytes from a field
    sgnData = ""   # Auxiliary string used for binary value of a signal
    thrd = None    # The thread on which the message will be send
    byteList = []  # The list of bytes to be send on CAN
    
    def __init__(self, ldfParser, frameName):
        '''
            Identifies the frame with 'frameName' and initializes
            the corresponding data fields 
            
            ldfParser = the parser used to read the LDF file.
            frameName = the name of the frame
        '''  
        self.subscribers = []
        self.signals = []
        ok = False  # flag for frame found in the list of frames from LDF
        # foreach frame from LDF file
        for frm in ldfParser.arrFrames:
            # if the searched frame is found
            if(frm.name == frameName):
                # get frame parameters from the frame in list
                ok = True
                self.name = frameName
                self.size = frm.size
                self.publisher = frm.publisher
                self.frameID = frm.frameID
                self.data = frm.data
                
                # get the subscribers of the frame
                for node in frm.subscribers:
                    self.subscribers.append(node)\
                # get the signals of the frame
                for sgn in frm.signals:
                    self.signals.append(sgn)
        if(ok == False):
            raise ValueError("The frame %s was not found in the parser object" % frameName)
    
    def SetSignalValue(self, signalName, value):
        '''
            Sets the value of the signal 'signalName' to 'value'
            Returns the updated value of the message data
            
            linParser = the parser used for reading the LDF file
            signalName = the name of the signal whose value we want to change
            value = the new value of the signal. This shoul be a hexadecimal value
        '''
        try:
            for sgn in self.signals:                 # search the signal with the signalName
                if(sgn.name == signalName):          # if signal is found
                    if(self.data.startswith("0x")):  # if value starts with 0x in hex, remove the 0x prefix
                        self.data = self.data[2 : ]
                    
                    self.auxData = bin(int("1" + self.data, 16)) [3 : ]  # convert data to binary. 1 upfront is for keeping the leading zeros
                    self.auxData = self.auxData.zfill(self.size * 8)
                    self.data = self.auxData
                    for i in range(0, len(self.auxData) / 8):
                        for j in range(0, 4):
                            self.data = self.data[: 8 * i +j] + self.data[8 * i + 7 - j] + self.data[8 * i + j + 1: 8 * i + 7 - j] + self.data[8 * i +j] + self.data[8 * i + 7 - j + 1 : ]
                    value = str(value)
                    if(value.startswith("0x")):              # if the value starts with 0x remove the prefix
                        self.nrBytes = (len(value) - 1) / 2  # calculate the number of bytes of the value
                    else:
                        self.nrBytes = (len(value) + 1) / 2
                        
                    self.sgnData = self.GetSignalValue(signalName)[2 :]                # extract the corresponding bits from message data
                    self.sgnData = bin(int(self.sgnData, 16))[2 : ].zfill(sgn.length)  # convert the extracted data fropm hexadecimal to binary
                    val = (bin(int(value, 16)) [2 :]).zfill(sgn.length)                # convert the given value to binary

                    for iIndex in range(len(val)):               # foreach bit of the value           
                        if val[iIndex] != self.sgnData[iIndex]:  # if the value bit is different of the corresponding data bit
                            self.sgnData = toggleBit(self.sgnData, iIndex)  # switch value of corresponding data bit

                    self.data = self.data[ : sgn.startbit] + self.sgnData + self.data[sgn.startbit + sgn.length : ]  # replace the signal value from the message data with the modified bit set
                    for i in range(0, len(self.data) / 8):
                        for j in range(0, 4):
                            self.data = self.data[: 8 * i +j] + self.data[8 * i + 7 - j] + self.data[8 * i + j + 1: 8 * i + 7 - j] + self.data[8 * i +j] + self.data[8 * i + 7 - j + 1 : ]
                    self.data = hex(int('1' + self.data, 2))  # convert the result back to hex. 1 is for keeping the leading zeros.

                    if(self.data.endswith("L")):
                        self.data = self.data [3 :-1]  # -1 removes the L suffix(tested only on large numbers) and the 0x preffix and the added 1
                    else:
                        self.data = self.data [3 : ]

                    if not (self.data.startswith("0x")):  # add the 0x prefix if it's necesary
                        self.data = "0x" + self.data
                        
                    return self.data
                
            raise ValueError("The frame with the name %s does not contain any signal with the name %s" % (self.name, signalName))
        
        except IndexError:            
            print "\n\nUnexpected error:", sys.exc_info()[1]
            print "Possibe error reason: the given value exceedes the signal length"
             
            if not (self.data.startswith("0x")):  # add the 0x prefix if it's necesary
                self.data = "0x" + self.data.zfill(self.size * 2) 
                
            print "The data field of this frame will be considerate %s\n\n" % self.data
            
            return self.data
    
    def GetSignalValue(self, signalName):
        '''
        Returns the value of the signal
        
        signalName = the name of the signal whose value we want to return
        '''
        try:
            for sgn in self.signals:                 # search the signal with the signalName
                if(sgn.name == signalName):          # if signal is found
                    if(self.data.startswith("0x")):  # if value starts with 0x in hex, remove the 0x prefix
                        self.data = self.data[2 :]
                    
                    auxData = bin(int("1" + self.data, 16)) [3 : ]  # convert data to binary. 1 upfront is for keeping the leading zeros
                    auxData = auxData.zfill(self.size * 8)          # add the leading zeros
                    return hex(int(auxData[sgn.startbit : sgn.startbit + sgn.length], 2)).zfill(sgn.length / 4)
        except:
            print "Unexpected error:", sys.exc_info()[1] 
            return "error"            
            
def toggleBit(bin_type, offset):
    '''Returns a binary string with value of offset toggled
    
    bin_type = the binary string
    offset = the position of the bit we want to toggle
    '''
    try:
        if(bin_type[offset] == '0'):
            bin_type = bin_type[ : offset] + bin_type[offset : ].replace(bin_type[offset], '1', 1)
        else: 
            bin_type = bin_type[ : offset] + bin_type[offset : ].replace(bin_type[offset], '0', 1)
        return bin_type
    
    except:
        print "Unexpected error:", sys.exc_info()[1] 
        return 'error'


# # analog lines
# AIO0 = 0x01
# AIO1 = 0x02
# AIO2 = 0x04
# AIO3 = 0x08
# AIO_ALL = 0x0F
# 
# # digital lines
# DIO0 = 0x01
# DIO1 = 0x02
# DIO2 = 0x04
# DIO3 = 0x08
# DIO4 = 0x10
# DIO5 = 0x20
# DIO6 = 0x40
# DIO7 = 0x80
# DIO_ALL = 0xFF
# 
# # combined digital lines for output mask
# OUTPUT_DIO0_DIO01 = 0x03
# OUTPUT_DIO2_DIO03 = 0x0C
# OUTPUT_DIO4_DIO05 = 0x30
# OUTPUT_DIO6_DIO07 = 0xC0
# 
# # masks for switches
# SWITCH_DIO0_DIO01 = 0x01
# SWITCH_DIO2_DIO03 = 0x02
# SWITCH_DIO4_DIO05 = 0x04
# SWITCH_DIO6_DIO07 = 0x08
# 
# digitalOutputMask = 0
# digitalInputMask = 0
# analogOutputMask = 0
# analogInputMask = 0
# switchMask = 0;
# switchState = 0 # 0 = relay open, 1 = relay closed
# frequency = 500
# outputMilliVolt = 4096
# 
# class daio_api():
#     # open xl driver
#     def __init__(self):
#         self.driver = vectordriver()
#         self.driver.open_driver()
#         
#     def get_driver_info(self):
#         p = s_xl_driver_config()
#         self.driver.get_driver_config(p)
#         return p
# 
#     def channel_init(self, channelselector=0):
#         # Application Config
#         ok, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', 0, XL_BUS_TYPE_DAIO)
#         if (ok != XL_SUCCESS):
#             # get complete xl driver configuration, stored in p object
#             p = self.get_driver_info()
#             channelFound = 0
#             for channel in range(0, p.channelCount):
#                 if channelFound == channelselector:
#                     if (p.channel[channel].channelBusActiveCapabilities == XL_BUS_TYPE_DAIO):
# #                         print p.channel[channel].channelBusActiveCapabilities
# #                         print p.channel[channel].transceiverName
#                         channelFound = 1
#                         # create application with 1 channel in Vector Hardware Config
#                         self.driver.set_appl_config('PLAST', 0, p.channel[channel].hwType, p.channel[channel].hwIndex, p.channel[channel].hwChannel, XL_BUS_TYPE_DAIO)
#                         print 'PLAST application was created in Vector Hardware Config.'
#                         self.hwt = p.channel[channel].hwType
#                         self.hwi = p.channel[channel].hwIndex
#                         self.hwc = p.channel[channel].hwChannel
#         # read setting of DAIO
#         gac, self.hwt, self.hwi, self.hwc = self.driver.get_appl_config('PLAST', 0, XL_BUS_TYPE_DAIO)
#         self.mask = self.driver.get_channel_mask(self.hwt.value, self.hwi.value, self.hwc.value)
#         # open port for the channel
#         op, self.phandle, self.pmask = self.driver.open_port(XLporthandle(XL_INVALID_PORTHANDLE), 'PLAST', XLaccess(self.mask.value), XLaccess(self.mask.value), XL_RECEIVE_EVENT_SIZE, XL_INTERFACE_VERSION, XL_BUS_TYPE_DAIO)
#         
#         if not(op): # if everything is ok, provide settings
#             ok, self.ehandle = self.driver.set_notification(self.phandle, XLporthandle(XL_INVALID_PORTHANDLE), 1)
#             
#             self.driver.reset_clock(self.phandle)
#             
#             # DIO0/DIO1 = Output (0b00000011), DIO2...DIO7 = Input (0b11111100)
#             switchMask        = SWITCH_DIO0_DIO01
#             digitalOutputMask = OUTPUT_DIO0_DIO01
#             digitalInputMask  = DIO_ALL & (~digitalOutputMask)
#             self.driver.xlDAIOSetDigitalParameters(self.phandle, self.mask.value, digitalInputMask, digitalOutputMask)
#             
#             # AIO0 = Output (0b0001), AIO1...AI03 = Input (0b1110)
#             analogOutputMask = AIO0;
#             analogInputMask  = AIO_ALL & (~analogOutputMask);
#             self.driver.xlDAIOSetAnalogParameters(self.phandle, self.mask.value, analogInputMask, analogOutputMask, 0x00)
#             
#             # Set AIO0 (defined output) to maximum voltage
#             self.driver.xlDAIOSetAnalogOutput(self.phandle, self.mask.value, outputMilliVolt, 0, 0, 0)
#             
#             # Measure cyclically analog and digital ports
#             self.driver.xlDAIOSetMeasurementFrequency(self.phandle, self.mask.value, frequency)
#             
#             self.driver.xlDAIOSetPWMOutput(self.phandle, self.mask.value, 100, 2500)
#             
#             
#             self.driver.activate_channel(self.phandle, self.mask.value, XL_BUS_TYPE_DAIO, 0)
#             
#         return self.phandle, self.pmask, self.ehandle, self.driver
# 
#     def channel_close(self):
#         self.driver.deactivate_channel(self.phandle, self.mask)
#         self.driver.close_port(self.phandle)
#         self.driver.close_driver()
# 
#     def get_msg(self):
#         event_count = ctypes.c_uint(1)
#         event_list = XLevent()
#         ok = self.driver.receive(self.phandle, event_count, event_list)
#         if ok:
#             rec_string = self.driver.get_error_string(ok)
#         else:
#             rec_string = self.driver.get_event_string(event_list)
#         return rec_string, event_list
# 
# def DAIO_Test():
#     thrd = Thread_Measuring_DAIO()
#     thrd.start()
#     time.sleep(3)
#     thrd.stop()
# 
# class Thread_Measuring_DAIO(): # only for channel 0
#     loop = 0
#     
#     def __init__(self):
#         pass
#          
#     def OnDAIO(self):
#         global loop
#         daio = daio_api()
#         phndle, msk, ehndle, driverr = daio.channel_init()
#         kernel32dll = ctypes.windll.LoadLibrary("kernel32.dll")
# 
#         # read hardware queue while not empty
#         while loop:
#             if(kernel32dll.WaitForSingleObject(ehndle, 10) != WAIT_TIMEOUT):
#                 xlStatus = XL_SUCCESS
#                 if(xlStatus != XL_ERR_QUEUE_IS_EMPTY):
#                     msg, evList = daio.get_msg()
#                     if (evList.tag == XL_RECEIVE_DAIO_DATA):
#                         
#                         # TODO manipulate the received message
# #                         print evList.tagData.daioData.value_analog
#                         pass
#                                      
#         daio.channel_close()
#          
#     def start(self):
#         global loop
#         loop = 1
#         alive = 1
#         Thread(target=self.OnDAIO, args=()).start()
#           
#     def stop(self):
#         global loop
#         loop = 0
#         
#     def isAlive(self):
#         global loop
#         return loop