class CRC16:
    """
        Communication with the device PZEM-004T-100A(V3.0)
    """
    def __init__(self, polynomial, seed):
        self.polynomial = polynomial
        self.seed = seed

    def CRC16(self, vector):
        '''
            CRC-16 Algorithm
        '''
        poly = 1 * self.polynomial
        crc = 1 * self.seed
        data = bytearray(vector)
        for b in data:
            crc ^= (0xFF & b)
            for _ in range(0, 8):
                if (crc & 0x0001):
                    crc = ((crc >> 1) & 0xFFFF) ^ poly
                else:
                    crc = ((crc >> 1) & 0xFFFF)

        return crc & 0xFFFF

    def verification(self, responseCRC, calculatedCRC):
        '''
            CRC Checker
        '''
        # As the CRC16 returned by the device switches the most significant byte
        # for the least significant byte, the CRC16 is switched 0xMMLL -> 0xLLMM
        aux = responseCRC[len(responseCRC)-1] << 8 | responseCRC[len(responseCRC)-2]
        # Check if the data is correct by comparing the response CRC16 and the
        # calculated CRC16
        if aux == calculatedCRC:
            # If correct, return 0
            return 0
        else:
            # If data is corrupted, return 1
            return 1
