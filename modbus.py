from pymodbus.client.sync import ModbusTcpClient
import time
import struct
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

class ModbusClient:
    def __init__(self, host="localhost", port=5502):
        """
        Initialise le client Modbus TCP
        """
        self.client = ModbusTcpClient(host, port)
        if not self.client.connect():
            raise ConnectionError(f"Impossible de se connecter à {host}:{port}")
        print(f"Connecté à {host}:{port}")

    # --- Lecture ---
    def read_coils(self, address, count=1, unit=1):
        """Lit des coils (bits)"""
        result = self.client.read_coils(address, count, unit=unit)
        if not result.isError():
            return result.bits
        else:
            print(f"Erreur lecture coils à {address}")
            return None

    def read_discrete_inputs(self, address, count=1, unit=1):
        """Lit des inputs discrets (bits en lecture seule)"""
        result = self.client.read_discrete_inputs(address, count, unit=unit)
        if not result.isError():
            return result.bits
        else:
            print(f"Erreur lecture discrete inputs à {address}")
            return None

    def read_holding_registers(self, address, count=1, unit=1):
        """Lit des holding registers (16 bits)"""
        result = self.client.read_holding_registers(address, count, unit=unit)
        if not result.isError():
            return result.registers
        else:
            print(f"Erreur lecture holding registers à {address}")
            return None

    def read_input_registers(self, address, count=1, unit=1):
        """Lit des input registers (16 bits)"""
        result = self.client.read_input_registers(address, count, unit=unit)
        if not result.isError():
            return result.registers
        else:
            print(f"Erreur lecture input registers à {address}")
            return None

    # --- Écriture ---
    def write_coil(self, address, value, unit=1):
        """Écrit un coil (bit)"""
        result = self.client.write_coil(address, value, unit=unit)
        return not result.isError()

    def write_register(self, address, value, unit=1):
        """Écrit un holding register (16 bits)"""
        result = self.client.write_register(address, value, unit=unit)
        return not result.isError()

    # --- Exemple cycle d’écriture / lecture ---
    def cycle_holding_registers(self, start=0, stop=10, delay=2, address=0, unit=1):
        """Exemple : incrémente un register de start à stop en boucle"""
        a = start
        while True:
            self.write_register(address, a, unit)
            print(f"Écrit {a} dans le holding register {address}")
            a += 1
            if a > stop:
                a = start
            time.sleep(delay)
    
    def read_holding_int32(self, address, unit=1, byteorder='big'):
        """Lit un entier signé 32 bits sur deux registres consécutifs"""
        regs = self.read_holding_registers(address, count=2, unit=unit)
        if regs is None:
            return None
        # Convertit les deux registres en bytes
        if byteorder == 'big':
            b = struct.pack('>HH', regs[0], regs[1])  # Big-endian
        else:
            b = struct.pack('<HH', regs[0], regs[1])  # Little-endian
        return struct.unpack('>i' if byteorder=='big' else '<i', b)[0]

    def read_holding_uint32(self, address, unit=1, byteorder='big'):
        """Lit un entier non signé 32 bits sur deux registres consécutifs"""
        regs = self.read_holding_registers(address, count=2, unit=unit)
        if regs is None:
            return None
        # Convertit les deux registres en bytes
        if byteorder == 'big':
            b = struct.pack('>HH', regs[0], regs[1])
        else:
            b = struct.pack('<HH', regs[0], regs[1])
        return struct.unpack('>I' if byteorder=='big' else '<I', b)[0]

    def read_input_int32(self, address, unit=1, byteorder='big'):
        """Lit un entier signé 32 bits sur deux registres consécutifs"""
        regs = self.read_holding_registers(address, count=2, unit=unit)
        if regs is None:
            return None
        # Convertit les deux registres en bytes
        if byteorder == 'big':
            b = struct.pack('>HH', regs[0], regs[1])  # Big-endian
        else:
            b = struct.pack('<HH', regs[0], regs[1])  # Little-endian
        return struct.unpack('>i' if byteorder=='big' else '<i', b)[0]

    def read_input_uint32(self, address, unit=1, byteorder='big'):
        """Lit un entier non signé 32 bits sur deux registres consécutifs"""
        regs = self.read_holding_registers(address, count=2, unit=unit)
        if regs is None:
            return None
        # Convertit les deux registres en bytes
        if byteorder == 'big':
            b = struct.pack('>HH', regs[0], regs[1])
        else:
            b = struct.pack('<HH', regs[0], regs[1])
        return struct.unpack('>I' if byteorder=='big' else '<I', b)[0]

    def write_int32(self, address, value, unit=1):
        """Écrit un int32 (32 bits signé) dans deux registres"""
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_int(value)
        payload = builder.to_registers()
        result = self.client.write_registers(address, payload, unit=unit)
        return not result.isError()
