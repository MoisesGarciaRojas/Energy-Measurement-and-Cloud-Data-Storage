from machine import UART
import time



class PZEM_V3:
    """
        Communication with the device PZEM-004T-100A(V3.0)
    """
    def __init__(self, address):
        # init UART with given parameters
        self.uart = UART(1, baudrate=9600, pins=('P3','P11'))
        # uart.init(). It is not needed and will reset the pins to the default values.
        # self.uart.init(9600, bits=8, parity=None, stop=1, timeout_chars=2)
        # Command format to reset energy registry
        self.reset = [address, 0x42, 0xC2, 0x41]
        # Command format to request measurement
        self.command = [address, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x64, 0x64]

    # Read measurement function
    def readData(self):
        '''
            Read the device´s variables
            0xF8 0x04 0x00 0x00 0x00 0x0A 0x64 0x64
            0x6464 is the CRC of the 6 most significant bytes
            NOTE: THE CODE INSIDE THIS FUNCTION WORKS WELL WHEN ALL VARIABLES ARE
            REQUESTED. IN CASE OF REQUIRING A DIFFERENT BEHAVIOR IT WILL NEED TO
            BE MODIFIED TOTALLY OR PARTIALLY. BESIDES, THE "data2measures" FUNCTION
            IS WRITTEN ACCORDING TO THIS FUNCTION (readData), THEREFORE
            "data2measures" WILL NEED MODIFICATION
        '''
        # Definition of the reset and error variables
        response = []                                                          ###
        error = []                                                             ###
        # For-loop to transmit byte by byte and read response from PZEM device
        for d in self.command:
            self.uart.write(bytes([d]))
        # Check if response´s length is different from the desired response data
        # length. Then Check if response´s length is equal to the error command
        # format, If TRUE return the negation of the abnormal code. Otherwise,
        # return code number -6 (Other error).
        # If response´s length is equal to the correct reply format, return response
        time.sleep(1)
        availableChars = self.uart.any()
        if availableChars != 25:
            if availableChars == 5:
                response = self.uart.readall()
                error = [-1 * response[2]]
                return error
            else:
                error = [-6]
                return error
        else:
            response = self.uart.readall()
            return response


    def resetEnergy(self):
        '''
            Reset energy registers to 0 and read its response
            0xF8 0x42 0xC2 0x41
            0x41C2 is the CRC of the 2 most significant bytes
        '''
        # Definition of the reset and error variables
        response = []
        error = 0
        # For-loop to transmit byte by byte and read response from PZEM device
        for d in self.reset:
            self.uart.write(bytes([d]))
        # Check if response´s length is different from the desired response data
        # length. Then Check if response´s length is equal to the error command
        # format, If TRUE return the negation of the abnormal code. Otherwise,
        # return code number -6 (Other error).
        # If response´s length is equal to the correct reply format, return response
        time.sleep(1)
        availableChars = self.uart.any()
        if availableChars != 4:
            if availableChars == 5:
                response = self.uart.readall()
                error = -1 * response[2]
                return error
            else:
                error = -6
                return error
        else:
            response = self.uart.readall()
            return response

    def data2measures(self, data):
        '''
            This functions returns a vector with the 10 measures from the PZEM_100A_V3
            device.
            NOTE: IN CASE OF MODIFIYING THE "readData" FUNCTION OR REQUIRING A
            DIFFERENT BEHAVIOR, THIS FUNCTION WILL NEED TO BE MODIFIED
            COMPLETELLY OR PARTIALLY
        '''
        if len(data) == 1:
            values = [data[0], data[0], data[0], data[0], data[0], data[0], data[0]]
        else:
            '''
                NOTE: DECIMAL VALUES ARE RETURNED, FURTHER CONVERSION IS REQUIRED
            '''
            voltage = data[3] << 8 | data[4]
            current = data[7] << 24 | data[8] << 16 | data[5] << 8 | data[6]
            power = data[11] << 24 | data[12] << 16 | data[9] << 8 | data[10]
            energy = data[15] << 24 | data[16] << 16 | data[13] << 8 | data[14]
            frequency = data[17] << 8 | data[18]
            power_factor = data[19] << 8 | data[20]
            alarm = data[21] << 8 | data[22]

            values = [voltage, current, power, energy, frequency, power_factor, alarm]

        return values
