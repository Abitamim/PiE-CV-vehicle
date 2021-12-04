# Jacob Smilg's serial_device code
# Modified by Abitamim Bharmal

import serial
import serial.tools.list_ports as list_ports
from serial.tools.list_ports_common import ListPortInfo

class SerialDevice:
    STANDARD_BAUDS = (50, 75, 110, 134, 150, 200, 300, 600,
                        1200, 1800, 2400, 4800, 9600, 19200,
                        38400, 57600, 115200)

    EXTENDED_BAUDS = (230400, 460800, 500000, 576000, 921600,
                        1000000, 1152000, 1500000, 2000000,
                        2500000, 3000000, 3500000, 4000000)

    ARDUINO_HIDS = ((0x2341, 0x0043), (0x2341, 0x0001),
                    (0x2A03, 0x0043), (0x2341, 0x0243),
                    (0x0403, 0x6001), (0x1A86, 0x7523))

    def __init__(self, port = None, baud = 9600) -> None:
        self.ser = serial.Serial(timeout = 1)
        self.connected = False
        self.port = port
        self.ser.baudrate = baud

        # try to autoselect a port if no port was specified
        if not port:
            arduino_ports = self.autodetect_ports()
            for port in arduino_ports:
                if not self.connected:
                    print('possible arduino port detected:')
                    print_port_info(port)
                    self.connect(port)
    
    def __del__(self) -> None:
        '''
        close the serial connection when the object is deleted
        '''
        self.ser.close()

    def autodetect_ports(self) -> list:
        '''
        check if any of the visible COM ports have matching Arduino
        (or clone) HIDS, and return a list of the ones that do.
        Returns:
            list: a list of ListPortInfo objects that match Arduino HIDS
        '''
        ports = list_ports.comports()
        arduino_ports = []
        for port in ports:
            if (port.vid, port.pid) in SerialDevice.ARDUINO_HIDS:
                arduino_ports.append(port)
        return arduino_ports

    def connect(self, port: ListPortInfo) -> None:
        '''
        confirm connection to a serial port, and connect (or don't).
        Args:
            port (ListPortInfo): the port to possibly be connected to.
        '''
        self.port = port
        try:
            self.ser.port = self.port.device
            self.ser.open()
            self.connected = True
            print('opened port {}'.format(port.name))
        except:
            print(('can\'t connect to port {}! is '+\
                'the port already in use?').format(self.port.device))
            pass


    def read(self) -> str:
        '''
        read the serial input buffer
        Returns:
            str: the contents of the serial input buffer
        '''
        line = ''
        if self.connected:
            line = self.ser.readline().decode()
        return line

    def write(self, string: str) -> None:
        '''
        send something over the serial port.
        Args:
            string (str): data to send over the serial port.
        '''
        if self.connected:
            self.ser.write('{}\r'.format(string).encode())


def print_port_info(port: ListPortInfo) -> None:
    '''
    list information about a specific serial port.
    Args:
        port (ListPortInfo): the serial port to print info about.
    '''
    print('\tname: {}'.format(port.name))
    print('\tdevice: {}'.format(port.device))
    print('\tdescription: {}'.format(port.description))
    print('\thwid: {}'.format(port.hwid))