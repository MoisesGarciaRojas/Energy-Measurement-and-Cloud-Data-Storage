#####################################################################################################################
# File_name:            uart_cloud/main.py                                                                          #
# Creator:              Moises Daniel Garcia Rojas                                                                  #
# Created:              Sunday - July 7th, 2019                                                                     #
# Last editor:          Moises Daniel Garcia Rojas                                                                  #
# Last modification:    Tuesday - September 3rd, 2019                                                               #
# Description:          This code perform measurements, and check data correctness on the PZEM_100A_V3 device.      #
#                       Besides it uploads the data to pybytes and stores the readings in case the WLAN connectioin #
#                       is not available.                                                                           #
#####################################################################################################################
# First FYPY device is for testing purposes and it is named: subMeter_001
import pycom
import time
import os
from PZEM_100A_V3 import PZEM_V3
from CRC16 import CRC16
from machine import Timer
from machine import SD


SECONDS_TO_MEASURE = 300
RESET_ENERGY_AT = 9000000

# Disable blue blinking LED
pycom.heartbeat(False)

# Declare objects
# Initialize PZEM object with device´s address
# Initialize CRC16 object with polynomial calculator and seed value respectively
# Declare new sd object
device = PZEM_V3(0xF8)
crc = CRC16(0xA001, 0xFFFF)
sd = SD()

# Initialize chronometer
# Start chronometer
# mount sd memory and create "sd" directory
chrono = Timer.Chrono()
chrono.start()
os.mount(sd, '/sd')

#reset energy registries (used for first programming)
#device.resetEnergy()

#Initialize electrical variables
voltage = 0.0
current = 0.0
power = 0.0
energy = 0.0
frequency = 0.0
power_factor = 0.0
flg = 0
# Infinite loop
while True:
    if chrono.read() >= SECONDS_TO_MEASURE:     # If SECONDS_TO_MEASURE seconds have passed
        chrono.reset()          # Reset chronometer to 0
        """
        Read measures and check data correctness
        """
        result = device.readData()          #Read device result
        if len(result) == 1:            # If result´s len = 1 (error)
            values = device.data2measures(result)
            voltage = 1.0 * values[0]
            current = 1.0 * values[1]
            power = 1.0 * values[2]
            energy = 1.0 * values[3]
            frequency = 1.0 * values[4]
            power_factor = 1.0 * values[5]
            # BLink aqua-green LED
            pycom.rgbled(0x007F7F)
            time.sleep(1)
            pycom.rgbled(0x000000)
        else:                       # If response length is correct,  verify crc16 agains data to check if it is correct
            if crc.verification(result, crc.CRC16(result[0: len(result)-2])) == 1:           # If it is not correct, -6 being (Other Error)
                voltage = -6.0
                current = -6.0
                power = -6.0
                energy = -6.0
                frequency = -6.0
                power_factor = -6.0
                # Blink yellow LED
                pycom.rgbled(0x7F7F00)
                time.sleep(1)
                pycom.rgbled(0x000000)
                # alarm = -6            # Do not consider Alarm data
            else:           # If calculated CRC16 corresponds to the CRC in result
                values = device.data2measures(result)
                voltage = 0.1 * values[0]
                current = 0.001 * values[1]
                power = 0.1 * values[2]
                energy = 1.0 * values[3]
                frequency = 0.1 * values[4]
                power_factor = 0.01 * values[5]
                # Blink blue LED
                pycom.rgbled(0x0000FF)
                time.sleep(1)
                pycom.rgbled(0x000000)
            # If response length was correct or wrong increment number of measures
        """
        Send data to pybytes or store it in the SD
        """
        """
        NOTE:
        Further functionalities are needed in the following lines in order to
        send data to pybytes once connection is restablished. Also, the flag "flg"
        will need to be reset in order to start recordings in a blank file, this
        in case the connection is again lost. Another problem would be if the
        connection is lost while uploading the recorded data, therefore a backup
        plan will be needed
        """
        if pybytes.is_connected():
            """
            NOTE:
            Once connection is restablished - A function to upload data is needed
            here, in case that the upload is completed it will return 0, if it is
            not completed it will return 1 and will not update the flg. In this
            case it will continue saving the data and will not delete the file
            previously created
            """
            pybytes.send_signal(1, voltage)
            pybytes.send_signal(2, current)
            pybytes.send_signal(3, power)
            pybytes.send_signal(4, energy)
            pybytes.send_signal(5, frequency)
            pybytes.send_signal(6, power_factor)
        else:
            if flg == 0:
                f = open('/sd/data.txt', 'w')
            else:
                f = open('/sd/data.txt', 'a')
            flg = 1
            f.write("{},{},{},{},{},{}".format(voltage, current, power, energy, frequency, power_factor) + '\r\n')
            f.close()

        """
        # THE FOLLOWING LINES WORK IN STANDARD PYTHON 2.7
        # THEY ARE USED TO READ LINE BY LINE FROM THE TXT FILE, THEY ALSO
        # SEPARATE THE LINES INTO THE DIFFERENT SIGNALS/VARIABLES
        # WHICH THEN COULD BE UPLOADED. IN CASE THAT DOESN´T WORK IN MICROPYTHON,
        # FIND ANOTHER SOLUTION WITH THE READALL() INSTRUCTION
        f = open('/sd/data.txt', 'r')
        f1 = f.readlines()
        for x in f1:
            b = x.replace("\n", "")
            voltage, current, power, energy, frequency, power_factor = b.split(",")
        data = f.readall()
        """
        """
        Reset energy registries
        """
        # If energy is more than RESET_ENERGY_AT, clear energy registries
        if energy >= RESET_ENERGY_AT:    # Indented one tab back
            reply = device.resetEnergy()
            if len(reply) == 4:
                # Blink green LED
                pycom.rgbled(0x00FF00)
                time.sleep(1)
                pycom.rgbled(0x000000)
            else:
                # BLink red LED
                pycom.rgbled(0xFF0000)
                time.sleep(1)
                pycom.rgbled(0x000000)
        # syntactically required else
        else:
            # If RESET_ENERGY_AT is not reached, then do nothing
            pass
    # Else statement required syntactically when checking the chronometer
    else:
        # If less than SECONDS_TO_MEASURE have passed, then do nothing
        pass
